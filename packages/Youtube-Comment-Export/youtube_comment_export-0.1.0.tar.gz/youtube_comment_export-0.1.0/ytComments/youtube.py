import yt_dlp
import polars as pl
import xlsxwriter
import time
from pathlib import Path
from colorama import Fore, init
from PySide6.QtCore import QThread, Signal
from .settingsManager import Settings

class yt_manager(QThread):
    """Download all comments from a YouTube channel,
    sorted by videos and export them in Excel files"""
    finished = Signal()
    
    def __init__(
        self, 
        channel_url: str | None = None, 
        dir: str | Path | None = None, 
        old_save: str | list[str] | None = None
        ):
        super().__init__()
        
        # Initialize the default values of parameters
        self.settings = Settings()
        self.settings.load()
        
        self.settings.channel_url = channel_url
        self.settings.directory = dir
        self._channel_data = None
        self.refresh()
            
        self.old_save = old_save
        self.old_comments = None
        self.progress = 0
        self.duration = None
        self.finish = False
            
    def __str__(self):
        init(autoreset=True)
        msg = f"{Fore.MAGENTA}Channel: {Fore.CYAN}{self.channel_title}\n"
        msg += f"{Fore.MAGENTA}Channel ID: {Fore.CYAN}{self.channel_id}\n"
        msg += f"\n{Fore.MAGENTA}{'Title':<80} {'Views':<10} {'URL'}\n"
        msg += f"{Fore.WHITE}-" * 140 + "\n"
        
        total_views = 0
        for video in self.channel_data['entries']:
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            video_title = video['title']
            video_views = video.get('view_count', 0)
            total_views += video_views
            msg += f"{Fore.YELLOW}{video_title[:80]:<80} {Fore.GREEN}{str(video_views)[:10]:<10} {Fore.CYAN}{video_url}\n"
        
        msg += f"\n{Fore.WHITE}{'-' * 140}\n"
        msg += f"{Fore.MAGENTA}Total Views for all videos: {Fore.GREEN}{total_views:,}"
        return msg
    
    def run(self):
        """Execution of the thread."""
        self.export_excel()
        self.finish = True
        # Emit finished signal
        self.finished.emit()
    
    @property
    def old_save(self) -> Path | list[Path]:
        """Returns the path of the old save."""
        return self._old_save
    
    @old_save.setter
    def old_save(self, value: str | Path | list[str | Path] | None):
        if value == None:
            return
        if isinstance(value, list):
            if all(isinstance(item, (str, Path)) for item in value):
                pass
            else:
                raise TypeError(
                    f"The list must only contain Path-like objects but is {type(value)}"
                    )
        elif isinstance(value, (str, Path)):
            value = [value]
        else:
            raise TypeError(
                f"The old save must be a Path-like object but is {type(value)}"
                )
        
        list_files = []
        for val in value:
            path = Path(val)
            if path.exists() and path.is_file():
                list_files.append(path)
            else:
                raise ValueError(
                    f"The file {val} does not exist"
                    )
        
        self._old_save = list_files
    
    @property
    def channel_data(self) -> pl.DataFrame:
        """Returns the data of the YouTube channel."""
        return self._channel_data
    
    @property
    def channel_title(self) -> str:
        """Returns the title of the YouTube channel."""
        channel_title = self.channel_data.get('title')
        if ' - Videos' in channel_title:
            channel_title = channel_title.replace(' - Videos', '')
        return channel_title

    @property
    def channel_id(self) -> str:
        """Returns the ID of the YouTube channel."""
        return self.channel_data.get('id')

    @property
    def channel_total_duration(self) -> str:
        """Returns the total duration of the channel videos in seconds."""
        total = self.channel_videos().select(pl.sum('duration')).to_series().item()

        # Convert total_seconds back to hh:mm:ss format if needed
        total_days = int(total // 86400)
        total_hours = int((total % 86400) // 3600)
        total_minutes = int((total % 3600) // 60)
        total_seconds = int(total % 60)
        
        formatted_time = f"{total_days:03}d:{total_hours:02}h:{total_minutes:02}m:{total_seconds:02}s"
        return formatted_time
    
    @property
    def channel_total_views(self) -> int:
        """Returns the total views of the channel videos."""
        return int(self.channel_videos().select('view_count').sum().item())
    
    @property
    def channel_number_videos(self) -> int:
        """Returns the number of videos of the channel."""
        return len(self.channel_videos())

    @property
    def videos_header(self) -> dict:
        """Returns the header row of the videos Excel sheet."""
        return {'row': 8, 'col': 0}

    @property
    def comments_header(self) -> dict:
        """Returns the header row of the comments Excel sheet."""
        return {'row': 6, 'col': 0}

    def refresh(self):
        """Refresh the channel data."""
        ydl_opts = {'quiet': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                self._channel_data = ydl.extract_info(self.settings.channel_url, download=False)
            except Exception as e:
                raise RuntimeError(f'Error fetching data: {e}')

    def channel_videos(self, include_comments: bool = False) -> pl.DataFrame:
        """Returns a pl.DataFrame with videos data of the channel."""
        
        df = pl.DataFrame(self.channel_data['entries'])
        df = df.select([
            'id', 
            'url', 
            'title', 
            'duration', 
            'view_count', 
            ])
        df = df.reverse() # from oldest to newest
        
        # Add a column with the comments
        total_videos = len(df)
        nb_video = 0
        comments = []
        comments_count = []
        upload_dates = []
        start = time.time()
        
        if include_comments:
            for video in df.iter_rows():
                nb_video += 1
                
                # Upload the new comments
                if self.finish == False:
                    info = self.dl_comments(video)
                    comment = info['comments']
                    upload_date = info['upload_date']
                # if the download window is cancelled early, add the saved untouched comments
                elif self.finish == True and self.old_comments:
                    comment = self.old_comments[0].get(video[0])
                    if comment is None: continue # if the video doesn't exist in the save, skip to the next loop
                    upload_date = self.old_comments[1].get(video[0])
                # if there isn't any save, finish the loop
                else:
                    break
                
                color_list = []
                current_color = 'color2'

                # Create a color column to switch color between each comment's thread
                # I failed to create it using polars expressions
                for value in comment['thread']:
                    if value == 'main':
                        if current_color == 'color1':
                            current_color = 'color2'
                        else:
                            current_color = 'color1'
                    color_list.append(current_color)

                comment = comment.with_columns(pl.Series('color', color_list))
                comments.append(comment)
                count = len(comment)
                comments_count.append(count)
                upload_dates.append(upload_date)
                
                # Update the progress bar
                self.progress = int(nb_video / total_videos * 100)
                self.duration = (time.time() - start) / nb_video * (total_videos - nb_video)
            
            # Add None values if not all videos are processed
            if len(comments) < total_videos:
                comments.extend([None] * (total_videos - len(comments)))

            # Add 0 values if not all videos are processed
            if len(comments_count) < total_videos:
                comments_count.extend([0] * (total_videos - len(comments_count)))

            # Add None values if not all videos are processed
            if len(upload_dates) < total_videos:
                upload_dates.extend([None] * (total_videos - len(upload_dates)))

            # Add the new columns
            df = df.with_columns(
                pl.Series(comments_count).alias('comments_count'),
                pl.Series(comments).alias('comments'),
                pl.Series(upload_dates).cast(pl.String).alias('upload_date')
                )
            
            # Convert upload_date from pl.String to pl.Date
            df = df.with_columns(
                pl.when(pl.col('upload_date').is_not_null())
                .then(pl.col('upload_date').str.strptime(pl.Date, format="%Y%m%d"))
                .otherwise(None)
                .alias('upload_date')
            )
        
        return df

    def dl_comments(self, video: tuple) -> pl.DataFrame:
        """Returns a pl.DataFrame with the comments of a YouTube video."""
        ydl_opts = {'getcomments': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video[1], download=False)
        
        upload_date = info.get('upload_date', None)
        
        # Create a dataframe from the comments
        df = pl.DataFrame(info['comments'])
        
        if len(df) != 0:
            # Add the columns date, id-parent, id-child
            df = df.with_columns(
                pl.from_epoch(pl.col('timestamp')).cast(pl.Date).alias('date'),
                pl.col('id')
                .str.split_exact('.', 1)
                .struct.rename_fields(['id-parent', 'id-child'])
                .alias('fields')
            ).unnest('fields')
            
            # Add the thread column
            df = df.with_columns(
                pl.when(pl.col('id-child').is_null())
                  .then(pl.lit('main'))
                  .otherwise(pl.lit('reply'))
                  .alias('thread')
            )
            
            df = df.select(['thread', 'author', 'date', 'text', 'id-parent', 'id-child'])
            # Add the new comments to the old comments
            if self.old_comments is not None:
                if video[0] in self.old_comments[0]:
                    comment = self.old_comments[0][video[0]].drop('color')
                    matching_df = comment.join(
                        df, 
                        on=['id-parent', 'id-child'], 
                        how='inner', 
                        join_nulls=True, 
                        maintain_order='left'
                        )
                    unmatching_df = df.join(
                        matching_df, 
                        on=['id-parent', 'id-child'], 
                        how='anti', 
                        join_nulls=True, 
                        maintain_order='left'
                        )
                    df = pl.concat([comment, unmatching_df])
                
            # Add the column oldest_date
            df = df.with_columns(
                pl.col('date').min().over('id-parent').alias('oldest_date')
            )

            df = df.sort(['oldest_date', 'id-parent'], descending=False, maintain_order=True)
            df = df.select(['thread', 'author', 'date', 'text', 'id-parent', 'id-child'])
        else:
            # Create an empty dataframe if the video doesn't have any comments
            df = pl.DataFrame({
                'thread': [],
                'author': [],
                'date': [],
                'text': [],
                'id-parent': [],
                'id-child': [],
            })
        return {'comments': df, 'upload_date': str(upload_date)}

    def export_excel(self):
        """Export the channel data to an Excel file."""
        
        df = self.channel_videos(include_comments=True)
        save_name = 'Export ' + self.channel_title
        nb = self.settings.max_sheets - 1
        total_files = (len(df) + nb - 1) // nb # round up
        
        # Create the fitting number of Excel files
        for i in range(1, total_files + 1):
            start = (i - 1) * nb + 1
            if i == total_files:
                end = len(df)
            else:
                end = i * nb
            filtered_df = df.slice(start - 1, end - start + 1)
            
            path = Path(self.settings.directory / (save_name + f' {i}.xlsx'))
            with xlsxwriter.Workbook(path) as wb:
                hlink = {'align': 'left', 'font_color': 'blue', 'underline': 1}
                video_col = {
                    'id': {'align': 'left'},
                    'url': hlink,
                    'title': {'align': 'left'},
                    'upload_date': {'align': 'center', 'num_format': self.settings.date_format},
                    'duration': {'align': 'center'},
                    'view_count': {'align': 'center'},
                    'comments_count': {'align': 'center'}
                }
                comments_col = {
                    'thread': {'align': 'center'},
                    'child': {'align': 'center'},
                    'author': {'align': 'center'},
                    'date': {'align': 'center', 'num_format': self.settings.date_format},
                    'text': {'align': 'left'}
                }
                video_header = self.videos_header
                comments_header = self.comments_header
                ws_video = wb.add_worksheet('videos')
                
                # Create some custom formats to use
                fmt_hyperlink = wb.add_format(hlink)
                fmt_left_align = wb.add_format({'align': 'left'})
                fmt_right_align = wb.add_format({'align': 'right'})
                fmt_center_align = wb.add_format({'align': 'center'})
                fmt_number_left = wb.add_format({'align': 'left', 'num_format': '#,##0'})
                fmt_number_center = wb.add_format({'align': 'center', 'num_format': '#,##0'})
                fmt_date_center = wb.add_format({'align': 'center', 'num_format': self.settings.date_format})
                fmt_channel_title = wb.add_format({
                    'align': 'center',
                    'valign': 'vcenter',
                    'bold': True,
                    'font_size': 20
                    })
                fmt_video_title = wb.add_format({
                    'align': 'left',
                    'bold': True,
                    'font_size': 14
                    })
                
                # Convert seconds to hh:mm:ss
                filtered_df = filtered_df.with_columns(
                    (pl.col('duration').cast(pl.Int64) // 3600).cast(pl.Utf8).str.zfill(2).alias('hh'),
                    (pl.col('duration').cast(pl.Int64) // 60 % 60).cast(pl.Utf8).str.zfill(2).alias('mm'),
                    (pl.col('duration').cast(pl.Int64) % 60).cast(pl.Utf8).str.zfill(2).alias('ss')
                )

                # Add a column with format hh:mm:ss
                filtered_df = filtered_df.with_columns(
                    (pl.concat_str([
                        pl.col('hh'), 
                        pl.lit('h:'), 
                        pl.col('mm'), 
                        pl.lit('m:'), 
                        pl.col('ss'),
                        pl.lit('s')
                        ])).alias('duration')
                )
                filtered_df = filtered_df.select([
                    'id', 
                    'url', 
                    'title',
                    'upload_date',
                    'duration', 
                    'view_count', 
                    'comments', 
                    'comments_count'
                ])
                
                # Export the videos summary
                filtered_df.drop(['comments']).write_excel(
                    workbook=wb,
                    worksheet=ws_video,
                    position=(video_header['row'], video_header['col']),
                    table_style='TableStyleMedium2',
                    column_formats=video_col,
                    header_format={'bold':True, 'align':'center'},
                    autofit=True,
                    freeze_panes=(video_header['row'] + 1, video_header['col']),
                    )
                
                # Add some custom values to the video sheet
                msg = f"Welcome to the YouTube channel of @{self.channel_title} !"
                ws_video.merge_range('A1:E1', 'Merged Cell')
                ws_video.write('A1', msg, fmt_channel_title)
                ws_video.write('B3', 'URL of the channel :', fmt_right_align)
                ws_video.write('B4', 'ID of the channel :', fmt_right_align)
                ws_video.write('B5', 'Total duration of the channel videos :', fmt_right_align)
                ws_video.write('B6', 'Total views of the channel :', fmt_right_align)
                ws_video.write('B7', 'Total number of videos of the channel :', fmt_right_align)
                ws_video.write('C3', self.settings.channel_url, fmt_hyperlink)
                ws_video.write('C4', self.channel_id, fmt_left_align)
                ws_video.write('C5', self.channel_total_duration, fmt_left_align)
                ws_video.write('C6', self.channel_total_views, fmt_number_left)
                ws_video.write('C7', self.channel_number_videos, fmt_left_align)
                
                filtered_df = filtered_df.with_row_index()
                # Export the comments of each video in a separate sheet
                for video in filtered_df.iter_rows():
                    comments = video[7]
                    if comments is not None:
                        ws_comment = wb.add_worksheet(video[1])
                         
                        # Add a hyperlink to each comments sheet in the summary
                        ws_video.write_url(
                            row=(video_header['row'] + int(video[0]) + 1), 
                            col=(video_header['col']), 
                            url=('internal:' + video[1] + '!A1'), 
                            cell_format=fmt_hyperlink, 
                            string=video[1]
                            )
                        
                        row = comments_header['row'] + 2
                        col = chr(comments_header['col'] + 65 + comments.shape[1] - 1)
                        cell = f'${col}{row}'
                        formula1 = f'=IF({cell}="color1", TRUE, FALSE)'
                        formula2 = f'=IF({cell}="color2", TRUE, FALSE)'
                        
                        if self.settings.bg_highlight:
                            conditional_col = {
                                ('thread', 'author', 'date', 'text'): [{
                                    'type': 'formula',
                                    'criteria': formula1,
                                    'format': {'bg_color': self.settings.bg_color[0]}
                                },
                                {
                                    'type': 'formula',
                                    'criteria': formula2,
                                    'format': {'bg_color': self.settings.bg_color[1]}
                                }]
                            }
                        else:
                            conditional_col = None
                        
                        # Export the comments of the current video
                        comments.write_excel(
                            workbook=wb,
                            worksheet=ws_comment,
                            position=(comments_header['row'], comments_header['col']),
                            column_formats=comments_col,
                            conditional_formats=conditional_col,
                            header_format={'bold':True, 'align':'center'},
                            autofit=True,
                            hidden_columns=['color', 'id-parent', 'id-child'],
                            freeze_panes=(comments_header['row'] + 1, comments_header['col'])
                        )
                                                
                        # Add some custom values to the comment sheet
                        ws_comment.write('A1', 'Title :', fmt_left_align)
                        ws_comment.write('A2', 'URL :', fmt_left_align)
                        ws_comment.write('A3', 'Upload :', fmt_left_align)
                        ws_comment.write('A4', 'Duration :', fmt_left_align)
                        ws_comment.write('A5', 'Views :', fmt_left_align)
                        ws_comment.write('B1', video[3], fmt_video_title)
                        ws_comment.write('B2', video[2])
                        ws_comment.write('B3', video[4], fmt_date_center)
                        ws_comment.write('B4', video[5], fmt_center_align)
                        ws_comment.write('B5', video[6], fmt_number_center)
                        ws_comment.write_url(
                            row=3, 
                            col=3, 
                            url='internal:videos!A1', 
                            cell_format=fmt_hyperlink, 
                            string='Back to the videos list'
                            )
    
    def import_excel(self):
        """Import old saved comments."""
        if self.old_save is None:
            raise ValueError(
                "An old_save value must be provided"
                )
        
        dict_data = {}
        for path in self.old_save:
            # Recover the upload date of each video
            upload_saved = pl.read_excel(
                path, 
                sheet_id=1, 
                read_options={"header_row": self.videos_header['row']}
                )
            upload_saved = upload_saved.with_columns(
                upload_saved["upload_date"].dt.strftime("%Y%m%d").alias("upload_date")
            )
            
            result_dict = upload_saved.select(['id', 'upload_date']).to_dict()
            upload_dict = {}
            for i in range(len(result_dict["id"])):
                upload_dict[result_dict["id"][i]] = result_dict["upload_date"][i]
            
            # Recover the comments of each video
            data_saved = pl.read_excel(
                path, 
                sheet_id=0, 
                read_options={"header_row": self.comments_header['row']}
                )
            
            if isinstance(data_saved, pl.DataFrame):
                raise TypeError(
                    f"The file {path} must contain more than one sheet"
                    )
            elif isinstance(data_saved, dict):
                data_saved.pop('videos', None)
                dict_data.update(data_saved)
                
        self.old_comments = (dict_data, upload_dict)
        

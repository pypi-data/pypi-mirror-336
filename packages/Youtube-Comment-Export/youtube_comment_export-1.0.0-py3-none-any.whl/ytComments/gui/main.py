from PySide6 import QtWidgets, QtCore
from .error import run_error
from ytComments.gui.progressbar import LoadingWindow

class MainWindow(QtWidgets.QFrame):
    """Main Window of the application."""
    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__(parent)
        self.app = parent
        layout = QtWidgets.QVBoxLayout(self)
        
        # Initialize the layout
        layout.addLayout(self.init_url())
        layout.addLayout(self.init_old_save())
        layout.addLayout(self.init_new_save())
        layout.addLayout(self.init_exe())
        
    def init_url(self):
        """Initialize the URL."""
        url_label = QtWidgets.QLabel("URL :")
        self.url_input = QtWidgets.QLineEdit()
        self.url_input.setText(self.app.yt.settings.channel_url)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(url_label)
        layout.addWidget(self.url_input)
        return layout

    def init_old_save(self):
        """Initialize the old save location."""
        old_save_label = QtWidgets.QLabel("Old save :")
        self.old_save_input = QtWidgets.QLineEdit()
        msg = "More than one save can be specified by separating them with a semicolon"
        self.old_save_input.setToolTip(msg)
        old_save_button = QtWidgets.QPushButton("Browse")
        old_save_button.clicked.connect(self.browse_file)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(old_save_label)
        layout.addWidget(self.old_save_input)
        layout.addWidget(old_save_button)
        return layout
    
    def init_new_save(self):
        """Initialize the new save directory."""
        directory_label = QtWidgets.QLabel("Save Directory :")
        self.directory_input = QtWidgets.QLineEdit()
        self.directory_input.setText(str(self.app.yt.settings.directory))
        directory_button = QtWidgets.QPushButton("Browse")
        directory_button.clicked.connect(self.browse_directory)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(directory_label)
        layout.addWidget(self.directory_input)
        layout.addWidget(directory_button)
        return layout
    
    def init_exe(self):
        """Initialize the execute button."""
        exe_button = QtWidgets.QPushButton("Execute")
        exe_button.clicked.connect(self.execute)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(exe_button)
        return layout

    def browse_file(self):
        """Open a file dialog to select files."""
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select the old saves", "", "Excel Files (*.xlsx)")
        # Add them in the old save input
        if files:
            self.old_save_input.setText(";".join(files))
    
    def browse_directory(self):
        """Open a file dialog to select a directory."""
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select a directory"
            )
        # Add them in the directory input
        if directory:
            self.directory_input.setText(directory)
            self.app.yt.settings.directory = directory
            self.app.yt.settings.save()
            
    def execute(self):
        """Execute the program."""
        self.app.yt.settings.channel_url = self.url_input.text()
        old_saves = self.old_save_input.text().split(";")
        directory = self.directory_input.text()
        
        # Check the validity of the old saves
        waste = ""
        for save in old_saves.copy():
            file = QtCore.QFile(save)
            
            # If the file does not exist, remove it from the list
            if not file.exists():
                old_saves.remove(save)
                waste += save
                
                # Check if the waste is a valid file (eg: a file with ";" in its path)
                file = QtCore.QFile(waste)
                if file.exists():
                    old_saves.append(waste)
                    waste = ""
                else:
                    waste += ";"
                    file = QtCore.QFile(waste)
                    if file.exists():
                        old_saves.append(waste)
                        waste = ""
            
            # Check if the file is a .xlsx file
            if file.exists() and QtCore.QFileInfo(file).suffix() != "xlsx":
                run_error(
                    "Invalid file extension detected",
                    f"The file {file.fileName()} is not a .xlsx file"
                    )
                return
        
        # If there isn't any old save, set it to None
        if len(old_saves) == 0:
            old_saves = None
        else:
            self.app.yt.old_save = old_saves
        
        # Check if the directory exists
        dir = QtCore.QFile(directory)
        if not dir.exists():
            run_error(
                "Invalid directory",
                f"The directory {directory} does not exist"
                )
            return
        else:
            self.app.yt.settings.directory = directory
        
        # Save the settings
        self.app.yt.settings.save()
        
        # Reset the finish value
        self.app.yt.finish = False
        
        # Show the loading window
        loading_window = LoadingWindow(countdown=True)
        loading_window.show()
        loading_window.update_progress(0)
        
        # Launch the program
        if old_saves is not None:
            try:
                self.app.yt.import_excel()
            except:
                run_error("Invalid save, choose a valid save")
                loading_window.close()
                return
        self.app.yt.start() # Execute the thread
        
        while self.app.yt.finish == False:
            QtWidgets.QApplication.processEvents()
            loading_window.update_progress(
                self.app.yt.progress, 
                self.app.yt.duration
                )

            # Terminate the download earlier if the loading window is closed
            if loading_window.closing:
                self.app.yt.finish = True
        
        loading_window.close()
        
            
            
import requests
import os
import sys
from PySide6.QtWidgets import QMessageBox
from packaging.version import Version
from .progressbar import LoadingWindow
import ytComments.metadata as metadata

class UpdateManager:
    """Update Downloader of the software"""
    def __init__(self, repo_owner, repo_name, parent=None):
        self.about = parent
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self._file_size = 0
        self._downloaded_size = 0
        self.dir_update = "update"

    @property
    def file_size(self):
        """Size of the file to download."""
        return self._file_size
    
    @file_size.setter
    def file_size(self, value:int):
        if not isinstance(value, int):
            msg = "The file size must be an integer"
            raise TypeError(
                msg
                )
        self._file_size = value

    @property
    def downloaded_size(self):
        """Size of the downloaded file."""
        return self._downloaded_size

    @downloaded_size.setter
    def downloaded_size(self, value:int):
        if not isinstance(value, int):
            msg = "The file size must be an integer"
            raise TypeError(
                msg
                )
        self._downloaded_size = value

    @property
    def progress(self):
        """Percentage of download."""
        if self.file_size == 0:
            return 0
        return int(self.downloaded_size / self.file_size * 100)

    def get_latest_release_info(self, extension=".exe"):
        """
        Retrieves the latest release information from GitHub, 
        including the tag and the URL of the .exe file.

        Returns:
            tuple: A tuple containing the latest version tag and 
            the URL of the .exe file, or (None, None) if an error occurs.
        """
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Throws an exception for HTTP error codes
            data = response.json()
            tag_name = data.get("tag_name")
            assets = data.get("assets", [])
            exe_url = None
            for asset in assets:
                if asset.get("name", "").lower().endswith(extension):
                    exe_url = asset.get("browser_download_url")
                    break
            return tag_name, exe_url
        except requests.exceptions.RequestException as e:
            print(f"Error while retrieving the latest version from GitHub : {e}")
            return None, None

    def check_updates(self):
        """
        Checks if an update is available.

        Returns:
            bool: True if an update is available, False otherwise.
        """
        latest_tag, exe_url = self.get_latest_release_info()
        
        if not latest_tag or not exe_url:
            return False
        
        latest_version = Version(latest_tag.lstrip('v'))
        current_version = Version(metadata.version)

        return latest_version > current_version

    def update_software(self):
        """Updates the software by downloading the .exe file from GitHub."""
        
        print("Updating software...")
        _, exe_url = self.get_latest_release_info()
        if not exe_url:
            print("No .exe file founded in the latest version.")
            return
        print(f"Downloading the new version from : {exe_url}")
        
        response = requests.get(exe_url, stream=True)
        response.raise_for_status()
        self.file_size = int(response.headers.get("content-length", 0))
        
        # Check if the program is an executable or a python file
        if hasattr(sys, 'frozen'):
            self.old_path = os.path.abspath(sys.executable) # .exe
        else:
            self.old_path = os.path.abspath(__file__) # .py
        
        # Define the directory and file path for the update
        new_filename = str(os.path.basename(exe_url))
        self.new_filedir = os.path.join(
            os.path.dirname(self.old_path), 
            self.dir_update
            )
        self.new_path = os.path.join(self.new_filedir, new_filename)
        
        # Create the directory if it doesn't exist
        os.makedirs(self.new_filedir, exist_ok=True)
        
        # Display the progress bar
        loading_window = LoadingWindow(self.about)
        loading_window.show()
        
        # Download the updated file
        with open(self.new_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                self.downloaded_size += len(chunk)
                loading_window.update_progress(self.progress)
                print(f"Progress update : {self.progress}%", end="\r")
        
        loading_window.close()
        print("Download of the update completed.")
    
    def show_file_location_message(self, file_path):
        """Shows a message to the user about the new version."""
        msg_box = QMessageBox()
        txt = f"""
        The update has been downloaded here :\n\n
        {file_path}\n
        You can delete the old version.
        """
        msg_box.setWindowTitle("Update completed")
        msg_box.setText(txt)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Display the message
        msg_box.exec()


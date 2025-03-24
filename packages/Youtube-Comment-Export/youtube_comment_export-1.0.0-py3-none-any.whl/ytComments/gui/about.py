import re
import ytComments.metadata as metadata
from PySide6 import QtWidgets, QtCore, QtGui
from .update import UpdateManager
from .error import run_error

class AboutWindow(QtWidgets.QDialog):
    """About menu of the application"""
    def __init__(self, parent):
        super().__init__(parent)
        self.menu = parent
        self.setWindowTitle("About")
        layout = QtWidgets.QVBoxLayout()

        self.init_version()
        layout.addLayout(self.layout_version)
        
        self.init_author()
        layout.addLayout(self.layout_author)
        
        self.init_license()
        layout.addLayout(self.layout_license)
        
        self.init_description()
        layout.addSpacing(10)
        layout.addLayout(self.layout_description)

        self.setLayout(layout)
        
    def init_version(self):
        """Version number and search update button."""
        self.layout_version = QtWidgets.QHBoxLayout()
        version_label = QtWidgets.QLabel("Version : ")
        version_text = QtWidgets.QLabel(metadata.version)

        # Add the button to check for updates
        self.check_update_button = QtWidgets.QPushButton("Check updates")
        self.check_update_button.setStyleSheet(self.style_link())
        self.check_update_button.clicked.connect(self.check_for_updates)
        
        self.layout_version.addWidget(version_label)
        self.layout_version.addWidget(version_text)
        self.layout_version.addWidget(self.check_update_button)
        self.layout_version.setAlignment(QtCore.Qt.AlignLeft)
        
    def init_author(self):
        """Program Author."""
        self.layout_author = QtWidgets.QHBoxLayout()
        author_label = QtWidgets.QLabel("Author : ")
        author_text = QtWidgets.QLabel(metadata.author)

        self.layout_author.addWidget(author_label)
        self.layout_author.addWidget(author_text)
        self.layout_author.setAlignment(QtCore.Qt.AlignLeft)

    def init_license(self):
        """License and code source url."""
        self.layout_license = QtWidgets.QHBoxLayout()
        license_label = QtWidgets.QLabel("License : ")
        license_text = QtWidgets.QLabel(metadata.license)
        
        url_button = QtWidgets.QPushButton("code source")
        url_button.setStyleSheet(self.style_link())
        url_button.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl(metadata.url))
            )

        self.layout_license.addWidget(license_label)
        self.layout_license.addWidget(license_text)
        self.layout_license.addWidget(url_button)
        self.layout_license.setAlignment(QtCore.Qt.AlignLeft)

    def init_description(self):
        """Software description."""
        self.layout_description = QtWidgets.QHBoxLayout()
        description_text = QtWidgets.QLabel(metadata.description)
        self.layout_description.addWidget(description_text)
        
    def style_link(self):
        """Style for links."""
        css = """
            QPushButton {
                border: none;  /* No border */
                background: none;  /* No background */
                color: DodgerBlue;  /* Text color */
                text-decoration: underline;  /* Underlined text to look like a link */
            }
            QPushButton:hover {
                color: RoyalBlue;  /* Text color on hover */
            }
        """
        return css

    def extract_repo_info(self, url: str):
        """Extracts the username and repository name from a GitHub URL."""
        pattern = r'https?://(?:www\.)?github\.com/([^/]+)/([^/]+)'
        match = re.match(pattern, url)

        if match:
            repo_owner = match.group(1)
            repo_name = match.group(2)
            return repo_owner, repo_name
        else:
            raise ValueError(
                "invalid URL"
                )

    def check_for_updates(self):
        """Check for update availability."""
        self.check_update_button.setEnabled(False)
        self.check_update_button.setText("Checking for updates...")
        QtWidgets.QApplication.processEvents()
        
        repo_owner, repo_name = self.extract_repo_info(metadata.url)
        updater = UpdateManager(repo_owner, repo_name, self)
        if updater.check_updates():
            self.check_update_button.setText("Downloading update...")
            QtWidgets.QApplication.processEvents()
            try:
                updater.update_software()
                self.check_update_button.setText("Update completed")
                updater.show_file_location_message(updater.new_filedir)
                self.menu.app.close()
            except Exception as e:
                msg = "An error occurred during the update"
                self.check_update_button.setText(msg)
                run_error(msg, details = e)
        else:
            self.check_update_button.setText("Software up to date")

        self.check_update_button.setEnabled(True)
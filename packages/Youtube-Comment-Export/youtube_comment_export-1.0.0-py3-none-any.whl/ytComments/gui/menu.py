from PySide6.QtWidgets import QMenuBar, QMainWindow
from .about import AboutWindow
from .settings import SettingsWindow

class MenuBar(QMenuBar):
    """Menu bar of the application."""
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.app = parent
        
        # Menu Settings
        self.settings_dialog = SettingsWindow(self)
        settings_menu = self.addAction("&Settings")
        settings_menu.triggered.connect(self.show_settings)
        
        # Menu About
        self.about_dialog = AboutWindow(self)
        help_menu = self.addAction("&About")
        help_menu.triggered.connect(self.about_dialog.exec)

    def show_settings(self):
        """Show the Settings window."""
        x = self.app.geometry().x() - 100
        y = self.app.geometry().y() - 100
        self.settings_dialog.setGeometry(x, y, 270, 200)
        self.settings_dialog.exec()
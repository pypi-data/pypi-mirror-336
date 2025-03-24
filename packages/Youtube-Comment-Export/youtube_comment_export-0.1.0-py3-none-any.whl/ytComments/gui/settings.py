from PySide6 import QtWidgets, QtGui, QtCore
from .error import run_error

class SettingsWindow(QtWidgets.QDialog):
    """Window for settings."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu = parent
        self.setWindowTitle("Settings")
        self.setModal(True)
        
        # Settings Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(self.init_color())
        layout.addLayout(self.init_highlight())
        layout.addLayout(self.init_max_sheets())
        layout.addLayout(self.init_date_format())
        layout.addLayout(self.init_auto_update())
        layout.addSpacing(10)
        layout.addLayout(self.init_buttons())
        
    def init_color(self):
        """Initialize Hex color code for the background of the comments on Excel."""
        msg = "Hex color code for the background of the comments on Excel"
        regex = QtCore.QRegularExpression(r'^#[0-9A-Fa-f]{6}$')
        validator = QtGui.QRegularExpressionValidator(regex)
        
        # Color Label
        color_label = QtWidgets.QLabel("Background color :")
        color_label.setToolTip(msg)
        
        # Color1 input
        self.color1_input = QtWidgets.QLineEdit()
        self.color1_input.setText(self.menu.app.yt.settings.bg_color[0])
        self.color1_input.setPlaceholderText("#C5D9F1")
        self.color1_input.setToolTip(msg)
        self.color1_input.setValidator(validator)
        
        # Color2 input
        self.color2_input = QtWidgets.QLineEdit()
        self.color2_input.setText(self.menu.app.yt.settings.bg_color[1])
        self.color2_input.setPlaceholderText("#FDE9D9")
        self.color2_input.setToolTip(msg)
        self.color2_input.setValidator(validator)
        
        # Color Layout
        color_layout = QtWidgets.QHBoxLayout()
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color1_input)
        color_layout.addWidget(self.color2_input)
        return color_layout

    def init_highlight(self):
        """Initialize the toggle for the background color."""
        msg = "Check to activate the background color"
        
        # Highlight label
        highlight_label = QtWidgets.QLabel("Background color :")
        highlight_label.setToolTip(msg)
        
        # Highlight toggle
        self.highlight_toggle = QtWidgets.QCheckBox()
        self.highlight_toggle.setChecked(self.menu.app.yt.settings.bg_highlight)
        self.highlight_toggle.setToolTip(msg)
        
        # Highlight layout
        highlight_layout = QtWidgets.QHBoxLayout()
        highlight_layout.addWidget(highlight_label)
        highlight_layout.addWidget(self.highlight_toggle)
        return highlight_layout
    
    def init_max_sheets(self):
        """Initialize the maximum number of sheets per file to export."""
        msg = "Maximum number of sheets per file to export"
        
        # Sheets label
        sheets_label = QtWidgets.QLabel("Sheets per file :")
        sheets_label.setToolTip(msg)
        
        # Sheets input
        self.sheets_input = QtWidgets.QLineEdit()
        self.sheets_input.setText(str(self.menu.app.yt.settings.max_sheets))
        self.sheets_input.setToolTip(msg)
        
        # Sheets layout
        sheets_layout = QtWidgets.QHBoxLayout()
        sheets_layout.addWidget(sheets_label)
        sheets_layout.addWidget(self.sheets_input)
        return sheets_layout
    
    def init_date_format(self):
        """Initialize the date format."""
        msg = "Format of the date in the comments"
        
        # Date label
        date_label = QtWidgets.QLabel("Date format :")
        date_label.setToolTip(msg)
        
        # Date input
        self.date_input = QtWidgets.QLineEdit()
        self.date_input.setText(self.menu.app.yt.settings.date_format)
        self.date_input.setToolTip(msg)
        
        # Date layout
        date_layout = QtWidgets.QHBoxLayout()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        return date_layout
    
    def init_auto_update(self):
        """Initialize the toggle for the automatic update."""
        msg = "Allow or not the program to search for software updates at startup"
        
        # Update label
        update_label = QtWidgets.QLabel("Search update at startup :")
        update_label.setToolTip(msg)
        
        # Update toggle
        self.update_toggle = QtWidgets.QCheckBox()
        self.update_toggle.setChecked(self.menu.app.yt.settings.auto_update)
        self.update_toggle.setToolTip(msg)
        
        # Update layout
        update_layout = QtWidgets.QHBoxLayout()
        update_layout.addWidget(update_label)
        update_layout.addWidget(self.update_toggle)
        return update_layout
    
    def init_buttons(self):
        """Initialize the OK and Cancel buttons."""
        # OK button
        ok_button = QtWidgets.QPushButton("OK")
        ok_button.clicked.connect(self.on_ok)
        
        # Cancel button
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.on_cancel)
        
        # Buttons layout
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        return buttons_layout
    
    def on_ok(self):
        """Manage the click on the OK button."""
        
        # Validate the color inputs
        try:
            color1 = str(self.color1_input.text()).upper()
            color2 = str(self.color2_input.text()).upper()
            if color1 == "":
                color1 = "#C5D9F1"
                self.color1_input.setText("#C5D9F1")
            if color2 == "":
                color2 = "#FDE9D9"
                self.color2_input.setText("#FDE9D9")
                
            self.menu.app.yt.settings.bg_color = (color1, color2)
        except ValueError as e:
            run_error(e)
            self.color1_input.setText(str(self.menu.app.yt.settings.bg_color[0]))
            self.color2_input.setText(str(self.menu.app.yt.settings.bg_color[1]))
            return
        
        # Validate the max sheets inputs
        try:
            max_sheets = int(self.sheets_input.text())
            self.menu.app.yt.settings.max_sheets = max_sheets
        except ValueError as e:
            run_error("The maximum number of sheets must be at least 2")
            self.sheets_input.setText(str(self.menu.app.yt.settings.max_sheets))
            return
        
        # Validate the other settings
        self.menu.app.yt.settings.bg_highlight = bool(self.highlight_toggle.isChecked())
        self.menu.app.yt.settings.date_format = str(self.date_input.text())
        self.menu.app.yt.settings.auto_update = bool(self.update_toggle.isChecked())
        self.menu.app.yt.settings.save()
        self.accept()
    
    def on_cancel(self):
        """Manage the click on the Cancel button."""
        self.reject()



import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QProgressBar, QLabel, QVBoxLayout, QPushButton
    )
from PySide6.QtCore import Qt

class LoadingWindow(QDialog):
    """Window to show the progress of a long-running operation."""
    def __init__(self, parent=None, countdown:bool = False):
        if QApplication.instance() is None:
                self.qapp = QApplication(sys.argv)
                
        super().__init__()
        self.setWindowTitle("Loading...")
        self.countdown = countdown
        
        if parent:
            self.parent = parent
            x = self.parent.app.geometry().x()
            y = self.parent.app.geometry().y()
        else:
            x = 100
            y = 100
        self.setGeometry(x, y, 300, 100)
        
        # Delete the Windows title buttons
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)

        # Initialize a close event
        self.closing = False

        # Create the progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #f0f0f0;  /* Background color */
                border: 2px solid #8f8f8f;   /* Border color */
                border-radius: 5px;          /* Rounded corners */
                height: 15px;                 /* Height of the progress bar */
                text-align: center;          /* Center the text */
                color: #000000;              /* Text color */
            }
            QProgressBar::chunk {
                background-color: #3c8dbc;   /* Background color of the filled chunk */
                border-radius: 5px;          /* Rounded corners of the filled chunk */
            }
        """)
        
        # Add an explanatory text
        self.label = QLabel("Downloading...", self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        # Add a countdown label
        if self.countdown:
            self.countdown_label = QLabel()
            self.countdown_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Add a cancel button
        msg = "Stop the download earlier, only the downloaded comments will be added to the old save"
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.terminate)
        self.cancel_button.setToolTip(msg)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.label)
        if self.countdown: layout.addWidget(self.countdown_label)
        layout.addWidget(self.cancel_button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def update_progress(self, value, duration:int | None = None):
        """Update the progress bar value."""
        self.progress_bar.setValue(value)
        
        # Update the countdown label
        if self.countdown and duration is not None: 
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            
            self.countdown_label.setText(
                f"Remaining estimated time : {hours:02}h:{minutes:02}m:{seconds:02}s"
                )
        
        QApplication.processEvents()
        
    def setText(self, text):
        """Update the window title."""
        self.label.setText(text)
        
    def terminate(self):
        """Close the window."""
        self.closing = True
        self.close()
        
        
        
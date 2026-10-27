import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QComboBox,
QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect)
from pathlib import Path

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # starts the smooth fade-in animation when the window opens
        self.setWindowOpacity(0.0)
        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(800)
        self.fade.setStartValue(0.0)
        self.fade.setEndValue(1.0)
        self.fade.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade.start()
        
        # window main properties
        self.setWindowTitle("Laboratory Portal Login")
        self.resize(360, 380)
        
        # text headings and title widgets
        self.title = QLabel("Laboratory Portal")
        self.subtitle = QLabel("Sign in to continue")
        
        # dropdown selection to let users pick their role in the system
        self.choose_role = QComboBox()
        self.choose_role.addItems(["Student", "Professor", "Laboratory Staff", "ITSO Maintenance"])
        
        # text input boxes for username and password
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # control checkboxes and action buttons
        self.show_password = QCheckBox("Show password")
        self.login_btn = QPushButton("Login")
        self.clear_btn = QPushButton("Clear")
        self.status = QLabel("")
        
        # shadow effects for clear button
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(4, 4)
        #accessing the X(right) and Y(down) coordinates layout of how far the is the shadow away from the each button
        shadow.setColor(QColor(0, 0, 0, 80))
        # controlling of how blur or sharp the edges of the shadows are
        shadow.setBlurRadius(15)
        # calling the setGraphicsEffect to display the customized widget
        self.clear_btn.setGraphicsEffect(shadow)
        
        # shadow effects for login button
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setColor(QColor(0, 0, 0, 80))
        #accessing the X(right) and Y(down) coordinates layout of how far the is the shadow away from the each button
        shadow2.setOffset(4, 4)
        # controlling of how blur or sharp the edges of the shadows are
        shadow2.setBlurRadius(15)
        # calling the setGraphicsEffect to display the customized widget
        self.login_btn.setGraphicsEffect(shadow2)
        
        # changes the mouse cursor to a pointer hand when hovering over buttons
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # assigns styling property tags for the stylesheet
        self.title.setObjectName("title")
        self.subtitle.setObjectName("subtitle")
        self.login_btn.setObjectName("loginBtn")
        self.clear_btn.setObjectName("clearBtn")
        self.status.setObjectName("status")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # arranges action buttons side by side in a row layout line
        buttons = QHBoxLayout()
        buttons.addWidget(self.clear_btn)
        buttons.addWidget(self.login_btn)
        
        # stacks all elements vertically straight down the page layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(self.choose_role)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.show_password)
        layout.addLayout(buttons)
        layout.addWidget(self.status)
        self.setLayout(layout)
        
        # signal buttons to toggle for login, clear and show password
        self.login_btn.clicked.connect(self.login)
        self.clear_btn.clicked.connect(self.clear)
        self.show_password.toggled.connect(self.toggle_password)
    
    # shows or hides password text depending on checkbox selection state
    def toggle_password(self, checked):
        if checked:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            
    # validates input details against fixed default system role logins database credentials
    def login(self):
        user = self.username.text().strip()
        password = self.password.text()
        role = self.choose_role.currentText()
        
        # setting up a default login validation rows check for each selected role type
        is_valid = False
        if role == "Student" and user == "student" and password == "1234":
            is_valid = True
        elif role == "Professor" and user == "professor" and password == "prof123":
            is_valid = True
        elif role == "Laboratory Staff" and user == "staff" and password == "staff123":
            is_valid = True
        elif role == "ITSO Maintenance" and user == "itso" and password == "itso123":
            is_valid = True
            
        # checks if the typed username and password match the selected role options
        if is_valid:
            self.set_style_property(self.username, "error", False)
            self.set_style_property(self.password, "error", False)
            self.set_style_property(self.status, "state", "success")
            self.status.setText(f"Welcome, {user} ({role})!")
        else:
            self.set_style_property(self.username, "error", True)
            self.set_style_property(self.password, "error", True)
            self.set_style_property(self.status, "state", "error")
            self.status.setText("Invalid username or password for this role.")
            self.shake()

    # resets login input text elements back to default states
    def clear(self):
        self.username.clear()
        self.password.clear()
        self.status.setText("")
        self.username.setFocus()
        self.set_style_property(self.username, "error", False)
        self.set_style_property(self.password, "error", False)
        self.set_style_property(self.status, "state", "")
        
    def set_style_property(self, widget, name, value):
        widget.setProperty(name, value)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        
    # shakes the window window frame left and right to signal a bad password attempt
    def shake(self):
        if hasattr(self, "shake_anim") and self.shake_anim.state() == QPropertyAnimation.State.Running:
            return
        
        start = self.pos()
        offsets = [0, -10, 10, -8, 8, -4, 4, 0]
        self.shake_anim = QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(400)
        for i, dx in enumerate(offsets):
            step = i / (len(offsets) - 1)
            self.shake_anim.setKeyValueAt(step, start + QPoint(dx, 0))
        self.shake_anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_file = Path(__file__).with_name("style.qss")
    if qss_file.exists():
        app.setStyleSheet(qss_file.read_text())
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

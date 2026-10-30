import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QComboBox,
QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect)
from pathlib import Path

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window fade-in animation
        self.setWindowOpacity(0.0)
        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(800)
        self.fade.setStartValue(0.0)
        self.fade.setEndValue(1.0)
        self.fade.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade.start()

        # Window setup
        self.setWindowTitle("Laboratory Portal Login")
        self.resize(360, 380)

        # Labels & input fields
        self.title = QLabel("Laboratory Portal")
        self.subtitle = QLabel("Sign in to continue")

        self.choose_role = QComboBox()
        self.choose_role.addItems(["Student", "Professor", "Laboratory Staff", "ITSO Maintenance"])

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_password = QCheckBox("Show password")
        self.login_btn = QPushButton("Login")
        self.clear_btn = QPushButton("Clear")
        self.status = QLabel("")

        # Drop shadows for buttons
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(4, 4)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setBlurRadius(15)
        self.clear_btn.setGraphicsEffect(shadow)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setColor(QColor(0, 0, 0, 80))
        shadow2.setOffset(4, 4)
        shadow2.setBlurRadius(15)
        self.login_btn.setGraphicsEffect(shadow2)

        # Styling properties & cursor shapes
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.title.setObjectName("title")
        self.subtitle.setObjectName("subtitle")
        self.login_btn.setObjectName("loginBtn")
        self.clear_btn.setObjectName("clearBtn")
        self.status.setObjectName("status")
        
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout setup
        buttons = QHBoxLayout()
        buttons.addWidget(self.clear_btn)
        buttons.addWidget(self.login_btn)

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
        
        # Signal connections
        self.login_btn.clicked.connect(self.login)
        self.clear_btn.clicked.connect(self.clear)
        self.show_password.toggled.connect(self.toggle_password)
    
    def toggle_password(self, checked):
        # Toggle password masking
        mode = QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        self.password.setEchoMode(mode)
            
    def login(self):
        user = self.username.text().strip()
        password = self.password.text()
        role = self.choose_role.currentText()
        
        # Credential validation
        is_valid = False
        if role == "Student" and user == "Student" and password == "student1234":
            is_valid = True
        elif role == "Professor" and user == "Professor" and password == "prof123":
            is_valid = True
        elif role == "Laboratory Staff" and user == "Staff" and password == "staff123":
            is_valid = True
        elif role == "ITSO Maintenance" and user == "ITSO" and password == "itso123":
            is_valid = True
            
        # Update UI feedback based on result
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

    def clear(self):
        # Reset input fields and style states
        self.username.clear()
        self.password.clear()
        self.status.setText("")
        self.username.setFocus()
        self.set_style_property(self.username, "error", False)
        self.set_style_property(self.password, "error", False)
        self.set_style_property(self.status, "state", "")
        
    def set_style_property(self, widget, name, value):
        # Force QSS style refresh after property change
        widget.setProperty(name, value)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        
    def shake(self):
        # Error shake animation
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
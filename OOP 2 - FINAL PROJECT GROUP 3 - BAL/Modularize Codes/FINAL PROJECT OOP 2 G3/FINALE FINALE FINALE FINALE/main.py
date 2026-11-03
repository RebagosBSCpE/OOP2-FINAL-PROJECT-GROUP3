import sys
import os
import ctypes
from datetime  import datetime
from pathlib import Path
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QMainWindow, QMessageBox)  
from PyQt6.QtCore import Qt
from Data_Model   import BorrowRequestData
from CSVFileReaderWriter  import CSVFileReaderWriter
from InventoryManager import InventoryManager
from LoginSystem  import LoginWindow
from Student   import StudentDashboard
from Prof import ProfessorDashboard
from Staff import StaffDashboard
from ITSO import ITSODashboard


# renamed from QMainWindow so it no longer replaces PyQt's QMainWindow class
class LabPortalApp:  # renamed from QMainWindow
    def __init__(self):
        # saved data that is shared between all screens
        self.shared_requests = []
        self.shared_announcements = []
        # inventory is loaded from inventory_data.csv and saved back whenever staff add, release or return items
        self.inventory =  InventoryManager()
        self.shared_inventory  = self.inventory.items

        self.csv_filepath  = "ITSO_Maintenance_data.csv"

        if os.path.exists (self.csv_filepath):
            try:
                csv_handler =  CSVFileReaderWriter()
                text_line =   csv_handler.read (self.csv_filepath)

                if text_line and str(text_line[0][0]).strip()   == "Request ID":
                    rows =  text_line[1:]
                else:
                    rows =   text_line

                for row in rows:
                    if not row or len(row)  < 10:
                        continue

                    try:
                        date_needed   = datetime.strptime(row[4], "%Y-%m-%d").date()
                    except:
                        date_needed  = datetime.now().date()

                    req =   BorrowRequestData(
                        request_id=int (row[0]),
                        student_id=str (row[1]),
                        name=str  (row[2]),
                        course_section=str (row[3]),
                        date_needed=date_needed,
                        items=str (row[5])
                    )

                    req.status   = str  (row[6])
                    req.lab_id = str (row[7])
                    req.timestamp_submitted  =  str(row[8])
                    req.timestamp_returned  = str(row[9])

                    self.shared_requests.append(req)
            except Exception as e:
                print(f"Could not load old data on startup: {e}")

        self.login_win   = LoginWindow()
        self.active_dashboard  = None
        self.master_container   = None  

        # disconnect and connect the login button action
        self.login_win.login_btn.clicked.disconnect()
        self.login_win.login_btn.clicked.connect(self.process_system_login)
        self.login_win.show()

    def process_system_login (self):
        # checks the login details and opens the correct dashboard
        user   = self.login_win.username.text().strip()
        password  = self.login_win.password.text()
        role  = self.login_win.choose_role.currentText()

        is_valid  = False
        if role   == "Student" and user  == "Student" and password == "student1234":
            is_valid = True
        elif role  == "Professor" and user   == "Professor" and password == "prof123":
            is_valid = True
        elif role  == "Laboratory Staff" and user == "Staff" and password   == "staff123":
            is_valid = True
        elif role == "ITSO Maintenance" and user   == "ITSO" and password  == "itso123":
            is_valid  = True

        if is_valid:
            self.login_win.set_style_property (self.login_win.username, "error", False)
            self.login_win.set_style_property  (self.login_win.password, "error", False)
            self.login_win.set_style_property (self.login_win.status, "state", "success")

            self.login_win.hide()
            self.launch_dashboard_workspace(role)
        else:
            self.login_win.set_style_property (self.login_win.username, "error", True)
            self.login_win.set_style_property  (self.login_win.password, "error", True)
            self.login_win.set_style_property (self.login_win.status, "state", "error")
            self.login_win.status.setText ("Invalid username or password for this role.")
            self.login_win.shake()

    def launch_dashboard_workspace ( self, role):
        # start the correct user role and pass the shared memory data
        if role   == "Student":
            self.active_dashboard  = StudentDashboard(
                shared_requests_list =self.shared_requests,
                shared_announcements  =self.shared_announcements,
                shared_inventory =self.shared_inventory
            )
        elif role  == "Professor":
            self.active_dashboard   = ProfessorDashboard(
                shared_requests_list =self.shared_requests,
                shared_announcement  =self.shared_announcements
            )
        elif role   == "Laboratory Staff":
            self.active_dashboard = StaffDashboard  (shared_requests_list=self.shared_requests, inventory_manager=self.inventory)
        elif role  == "ITSO Maintenance":
            self.active_dashboard  = ITSODashboard()

        # black pill that shows which account is logged in (white text)
        title_tag   = QLabel (f"Active Account: {role}")
        title_tag.setAlignment (Qt.AlignmentFlag.AlignCenter)
        title_tag.setFixedWidth( 230)  # (change this number to resize the pill)
        title_tag.setStyleSheet("""
            background-color: #000000;
            color: #ffffff;
            border-radius:  7px;
            padding: 3px 10px;
            font-size: 12px;
            font-weight: bold;
        """)

        # black pill button with yellow text to log out or switch role
        switch_btn  = QPushButton  ("Logout / Switch System Role")
        switch_btn.setCursor (Qt.CursorShape.PointingHandCursor)
        switch_btn.setFixedWidth(  230)  # (change this number to resize the pill)
        switch_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #fabb0d;
                border-radius: 7px;
                padding: 3px 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background   -  color: #fabb0d;
                color: #000000;
            }
        """)
        switch_btn.clicked.connect  (self.return_to_login_screen)

        # stacks the account tag on top of the logout button
        account_box = QVBoxLayout()
        account_box.setSpacing( 6)
        account_box.addWidget (title_tag)
        account_box.addWidget  (switch_btn)

        # finds the yellow title pill of the dashboard and puts the account box beside it
        dash_layout   = self.active_dashboard.layout()
        page_title  = self.active_dashboard.findChild(QLabel, "pageTitle")
        title_index  = dash_layout.indexOf(page_title)
        dash_layout.removeWidget (page_title)

        # header row = yellow title on the left, account box on the right
        header_row  = QHBoxLayout()
        header_row.addWidget (page_title, 1)
        header_row.addLayout  (account_box)
        dash_layout.insertLayout (title_index, header_row)

        # start: real Qt main window that holds the menu bar; the dashboard is its central widget
        self.master_container  = QMainWindow()
        self.master_container.setCentralWidget  (self.active_dashboard)

        # menu bar: File and About menus
        menu_bar =   self.master_container.menuBar()

        file_menu   = menu_bar.addMenu ("File")
        file_menu.addAction  ("Logout / Switch System Role", self.return_to_login_screen)
        file_menu.addSeparator()
        file_menu.addAction  ("Exit", QApplication.quit)

        about_menu = menu_bar.addMenu  ("About")
        about_menu.addAction ("Group 3 - CPE21S4", self.show_about)

        self.master_container.setWindowTitle (f"Laboratory System - {role} Dashboard")
        self.master_container.resize(  900 , 700)
        self.master_container.show()

    # whole method: dialog opened from About > Group 3
    def show_about (self):
        # dialog showing the group name and members
        QMessageBox.information(
            self.master_container, "About",
            "Laboratory Equipment Borrowing and Inventory Management System\n\n"
            "Group 3 - CPE21S4\n"
            "Developed by:\n"
            "Acelajado, John Vince D.\n"
            "Bal, Kevin Ranz J.\n\n"
            "Instructor: Engr. Jimlord M. Quejado"
        )

    def return_to_login_screen (self):
        # order changed: show the login screen first, then close the dashboard
        self.login_win.username.clear()
        self.login_win.password.clear()
        self.login_win.status.setText("")
        self.login_win.show()
        if self.master_container:
            self.master_container.close()


if __name__  == "__main__":
    if sys.platform   == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID  ("tip.laboratory.portal")

    app = QApplication  (sys.argv)
    app.setWindowIcon(QIcon(str(Path(__file__).with_name ("app_icon.ico"))))
    qss_filepath = Path(__file__).with_name("style.qss")
    if qss_filepath.exists():
        app.setStyleSheet (qss_filepath.read_text())

    window = LabPortalApp()  
    sys.exit(app.exec())
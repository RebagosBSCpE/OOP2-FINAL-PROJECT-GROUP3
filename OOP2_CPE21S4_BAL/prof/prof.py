import sys
from pathlib import Path
from datetime import datetime
from data_model_prof import Announcement
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidgetItem
from profui import ProfessorDashboardApp

class ProfessorDashboard(QWidget):
    def __init__(self, shared_requests_list=None, shared_announcement=None):
        super().__init__()
        
        # saves the student requests list if it exists, or makes a new empty list if it is missing
        self.shared_requests = shared_requests_list if shared_requests_list is not None else []
        # saves the professor announcements list if it exists, or makes a new empty list if it is missing
        self.shared_announcements = shared_announcement if shared_announcement is not None else []
        
        # creates an instance of the interface layout
        self.ui = ProfessorDashboardApp()
        self.ui.setupUi(self)
        
        # signals for approve and decline button
        self.ui.approve_btn.clicked.connect(self.process_approval)
        self.ui.reject_btn.clicked.connect(self.process_rejection)
        
        # signal for the announcement publish button
        self.ui.publish_btn.clicked.connect(self.publish_announcement)
        
        # automatically sizes the table columns to fit the text inside them
        self.ui.requests_table.resizeColumnsToContents()
        # locks the column widths permanently so they cannot be stretched or messed up to look neatly
        self.ui.requests_table.horizontalHeader().setSectionResizeMode(self.ui.requests_table.horizontalHeader().ResizeMode.Fixed)
        
        # loads all student requests into the table when the window opens
        self.load_requests_data()
    
    def publish_announcement(self):
        message = self.ui.announcement_input.text().strip()
        
        # stops the operation and shows a warning popup if the announcement text is empty
        if not message:
            QMessageBox.warning(self, "Input Error", "Please write an announcement message first.")
            return
            
        # new announcement record with the current date and time stamp
        current_time = datetime.now().strftime("%b %d, %I:%M %p")
        new_announcement = Announcement(author="Prof", message=message, time_posted=current_time)
        self.shared_announcements.insert(0, new_announcement)
        
        # displays a success alert window and clears out the announcement input line box
        QMessageBox.information(self, "Success", "Announcement has been published successfully to all students!")
        self.ui.announcement_input.clear()

    def load_requests_data(self):
        # clears out the table grid rows before reloading clean records
        self.ui.requests_table.setRowCount(0)
        
        # loops through the shared requests list array to build the grid table lines
        for req in self.shared_requests:
            row = self.ui.requests_table.rowCount()
            self.ui.requests_table.insertRow(row)
            self.ui.requests_table.setItem(row, 0, QTableWidgetItem(req.student_id))
            self.ui.requests_table.setItem(row, 1, QTableWidgetItem(req.name))
            self.ui.requests_table.setItem(row, 2, QTableWidgetItem(req.course_section))
            self.ui.requests_table.setItem(row, 3, QTableWidgetItem(str(req.date_needed))) # converts the date into plain text to prevent crashes
            self.ui.requests_table.setItem(row, 4, QTableWidgetItem(req.items))
            self.ui.requests_table.setItem(row, 5, QTableWidgetItem(req.status))
            
            # displays the exact time the request form arrived from the student
            time_text = getattr(req, 'timestamp_submitted', '')
            self.ui.requests_table.setItem(row, 6, QTableWidgetItem(time_text))

    def process_approval(self):
        row = self.ui.requests_table.currentRow()
        # stops the operation with a warning error alert if the instructor clicks approval without selecting a row
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a request from the table grid first.")
            return
        
        comment = self.ui.comment_input.toPlainText().strip()
        self.shared_requests[row].status = "Approved"
        
        # shows an alert card popup with details regarding the approval step
        QMessageBox.information(
            self, "Action Verified", 
            f"Request Approved.\nComment note attached: {comment if comment else 'None'}"
        )
        self.clear_workspace()

    def process_rejection(self):
        row = self.ui.requests_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a request from the table grid first.")
            return
            
        comment = self.ui.comment_input.toPlainText().strip()
        # stops the operation and triggers an alert if the feedback text area is blank
        if not comment:
            QMessageBox.warning(
                self, "Validation Error", 
                "You must provide a feedback comment explanation reason before executing a Rejection action step."
            )
            return

        self.shared_requests[row].status = "Rejected"
        # shows a popup warning window containing the typed decline reasons string note
        QMessageBox.warning(
            self, "Action Verified", 
            f"Request Declined.\nReason: {comment}"
        )
        self.clear_workspace()

    def clear_workspace(self):
        # resets the layout text fields and clears any selected rows inside the table grid
        self.ui.comment_input.clear()
        self.ui.requests_table.clearSelection()
        self.load_requests_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_filepath = Path(__file__).with_name("prof.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
        
    window = ProfessorDashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(650, 500)
    window.show()
    sys.exit(app.exec())

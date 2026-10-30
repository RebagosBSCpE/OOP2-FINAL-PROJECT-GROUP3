import sys
from pathlib import Path
from datetime import datetime
from data_model_prof import Announcement
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication, QTableWidgetItem
from profui import ProfessorDashboardApp

class ProfessorDashboard(QWidget):
    def __init__(self, shared_requests_list=None, shared_announcement=None):
        super().__init__()
        
        # Shared data storage
        self.shared_requests = shared_requests_list if shared_requests_list is not None else []
        self.shared_announcements = shared_announcement if shared_announcement is not None else []
        
        # UI setup
        self.ui = ProfessorDashboardApp()
        self.ui.setupUi(self)
        
        # Connect action buttons to handler slots
        self.ui.approve_btn.clicked.connect(self.process_approval)
        self.ui.reject_btn.clicked.connect(self.process_rejection)
        self.ui.publish_btn.clicked.connect(self.publish_announcement)
        
        # Format table headers
        self.ui.requests_table.resizeColumnsToContents()
        self.ui.requests_table.horizontalHeader().setSectionResizeMode(
            self.ui.requests_table.horizontalHeader().ResizeMode.Fixed
        )
        
        # Initial data load
        self.load_requests_data()
    
    def publish_announcement(self):
        message = self.ui.announcement_input.text().strip()
        
        # Input validation
        if not message:
            QMessageBox.warning(self, "Input Error", "Please write an announcement message first.")
            return
            
        # Create and prepend new announcement
        current_time = datetime.now().strftime("%b %d, %I:%M %p")
        new_announcement = Announcement(author="Prof", message=message, time_posted=current_time)
        self.shared_announcements.insert(0, new_announcement)
        
        QMessageBox.information(self, "Success", "Announcement has been published successfully to all students!")
        self.ui.announcement_input.clear()

    def load_requests_data(self):
        # Refresh table rows with active shared requests
        self.ui.requests_table.setRowCount(0)
        
        for req in self.shared_requests:
            row = self.ui.requests_table.rowCount()
            self.ui.requests_table.insertRow(row)
            self.ui.requests_table.setItem(row, 0, QTableWidgetItem(req.student_id))
            self.ui.requests_table.setItem(row, 1, QTableWidgetItem(req.name))
            self.ui.requests_table.setItem(row, 2, QTableWidgetItem(req.course_section))
            self.ui.requests_table.setItem(row, 3, QTableWidgetItem(str(req.date_needed)))
            self.ui.requests_table.setItem(row, 4, QTableWidgetItem(req.items))
            self.ui.requests_table.setItem(row, 5, QTableWidgetItem(req.status))
            
            time_text = getattr(req, 'timestamp_submitted', '')
            self.ui.requests_table.setItem(row, 6, QTableWidgetItem(time_text))

    def process_approval(self):
        row = self.ui.requests_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a request from the table grid first.")
            return
        
        comment = self.ui.comment_input.toPlainText().strip()
        self.shared_requests[row].status = "Approved"
        
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
        # Require reason on rejection
        if not comment:
            QMessageBox.warning(
                self, "Validation Error", 
                "You must provide a feedback comment explanation reason before executing a Rejection action step."
            )
            return

        self.shared_requests[row].status = "Rejected"
        QMessageBox.warning(
            self, "Action Verified", 
            f"Request Declined.\nReason: {comment}"
        )
        self.clear_workspace()

    def clear_workspace(self):
        # Reset input controls and table selection
        self.ui.comment_input.clear()
        self.ui.requests_table.clearSelection()
        self.load_requests_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load optional application stylesheet
    qss_filepath = Path(__file__).with_name("prof.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
        
    window = ProfessorDashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(650, 500)
    window.show()
    sys.exit(app.exec())
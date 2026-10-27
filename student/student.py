import os
import sys
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication
from studentui import StudentDashboardApp
from pathlib import Path
from data_model_student import BorrowRequestData
from CSVFileReaderWriiter import CSVFileReaderWriter
class StudentDashboard(QWidget):
    def __init__(self, shared_requests_list=None, shared_announcements=None):
        super().__init__()
        
        # to remember the shared list info links passed from the main application window
        self.shared_requests = shared_requests_list if shared_requests_list is not None else []
        self.shared_announcements = shared_announcements if shared_announcements is not None else []
        
        # creates an instance of the interface layout
        self.ui = StudentDashboardApp()
        self.ui.setupUi(self)
        
        #signals
        self.ui.add_item_btn.clicked.connect(self.add_item_to_table)
        self.ui.clear_items_btn.clicked.connect(self.clear_table_items)
        self.ui.submit_request_btn.clicked.connect(self.process_submission)
        
        # automatically updates the dashboard display items list on startup
        self.load_announcements_data()
        
    def load_announcements_data(self):
        # clears out the list view widget completely before showing fresh notes
        self.ui.announcements_list.clear()
                
        # loops through the shared announcements list to fill the display rows
        for info in self.shared_announcements:
            self.ui.announcements_list.addItem(f"[{info.time_posted}] {info.author}: {info.message}")

    def add_item_to_table(self):
        name = self.ui.material_name_input.text().strip()
        qty = str(self.ui.quantity_spin.value())
        
        # stops the action and shows a warning popup if the material name is blank
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please type a material name first.")
            return
            
        # gets the total rows, adds a new empty row, and adds the material name and quantity to the list
        row_idx = self.ui.items_table.rowCount()
        self.ui.items_table.insertRow(row_idx)
        self.ui.items_table.setItem(row_idx, 0, QTableWidgetItem(name))
        self.ui.items_table.setItem(row_idx, 1, QTableWidgetItem(qty))
        
        # reset the material bar inputs and sets the item count spinbox back to one
        self.ui.material_name_input.clear()
        self.ui.quantity_spin.setValue(1)

    def clear_table_items(self):
        self.ui.items_table.setRowCount(0)  # removes every added material item row from the display list table

    def process_submission(self):
        student_name = self.ui.student_name.text().strip()
        student_id = self.ui.student_id.text().strip()
        course_section = self.ui.course_section.text().strip()
        date_needed = self.ui.date_needed.date().toPyDate()
        
        # shows a warning message box if the name field or any personal information text lines are blank
        if not student_name or not student_id:
            QMessageBox.warning(self, "Validation Error", "Please provide your student ID and Name before submitting.")
            return
        
        # shows an error message if the student tries to submit a completely empty table
        if self.ui.items_table.rowCount() == 0:
            QMessageBox.warning(self, "Validation Error", "Your request list is empty. Add at least one item first.")
            return
        
        # collects all table item grid lines and bundles them into a single string
        collected_items = []
        for r in range(self.ui.items_table.rowCount()):
            item_name = self.ui.items_table.item(r, 0).text()
            item_qty = self.ui.items_table.item(r, 1).text()
            collected_items.append(f"{item_name} (x{item_qty})")
        items_summary = ", ".join(collected_items)
                
        # creates a new request object tracking code and adds it to the shared list data array
        request_id = len(self.shared_requests) + 1
        new_request = BorrowRequestData(request_id, student_id, student_name, course_section, date_needed, items_summary)
        self.shared_requests.append(new_request)
        
        #test feature
        csv_filepath = "itso_maintenance_dashboard.csv"
        csv_handler = CSVFileReaderWriter()
        # Verifies if the target backup file does not exist on your computer yet
        if not os.path.exists(csv_filepath):
            # Creates the text file tracking column titles as the very first line
            csv_handler.write(csv_filepath, ["Request ID", "Student ID", "Name", "Course Section", "Date Needed", "Items", "Status"])
            
        # Converts all structural fields into an array line to write to disk
        record_row = [
            str(new_request.request_id), new_request.student_id, new_request.name,
            new_request.course_section, str(new_request.date_needed), new_request.items, new_request.status
        ]
        # Invokes your polymorphic class writer to save rows into the sheet logs
        csv_handler.write(csv_filepath, record_row)
        #-------------------------------------------------------
        # displays a confirmation that the request form was submitted
        QMessageBox.information(self, "Success", f"Borrowing request submitted successfully for {student_name}!")
        self.clear_entire_form()

    def clear_entire_form(self):
        #clears out all text entry fields and empties the main table list
        self.ui.student_id.clear()
        self.ui.student_name.clear()
        self.ui.course_section.clear()
        self.clear_table_items()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # importing the student qss inside to merge the qss to the logic file
    qss_filepath = Path(__file__).with_name("student.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
        
    window = StudentDashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(600, 650)
    window.show()
    sys.exit(app.exec())

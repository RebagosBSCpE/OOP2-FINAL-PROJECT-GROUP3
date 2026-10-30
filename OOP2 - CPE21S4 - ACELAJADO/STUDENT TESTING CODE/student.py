import sys
import os
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication
from studentui import StudentDashboardApp
from data_model_student import BorrowRequestData
from CSVFileReaderWriter import CSVFileReaderWriter

class StudentDashboard(QWidget):
    def __init__(self, shared_requests_list=None, shared_announcements=None, shared_inventory=None):
        super().__init__()
        
        # Shared data storage
        self.shared_requests = shared_requests_list if shared_requests_list is not None else []
        self.shared_announcements = shared_announcements if shared_announcements is not None else []
        self.shared_inventory = shared_inventory if shared_inventory is not None else []
        
        # UI setup
        self.ui = StudentDashboardApp()
        self.ui.setupUi(self)
        
        # Connect signal handlers
        self.ui.add_item_btn.clicked.connect(self.add_item_to_table)
        self.ui.clear_items_btn.clicked.connect(self.clear_table_items)
        self.ui.submit_request_btn.clicked.connect(self.process_submission)
        self.ui.stock_search_input.textChanged.connect(self.search_stock)
        self.ui.program.currentTextChanged.connect(self.update_professor_list)
        
        # Initial loads
        self.load_announcements_data()
        self.update_professor_list()
        
    def load_announcements_data(self):
        # Refresh announcements list view
        self.ui.announcements_list.clear()
        for info in self.shared_announcements:
            self.ui.announcements_list.addItem(f"[{info.time_posted}] {info.author}: {info.message}")
    
    def search_stock(self):
        # Search and display available materials
        self.ui.stock_results.clear()
        text = self.ui.stock_search_input.text().strip().lower()
        if not text:
            return
        if not self.shared_inventory:
            self.ui.stock_results.addItem("No inventory data received yet.")
            return
        for stock in self.shared_inventory:
            if text in stock.material_name.lower():
                self.ui.stock_results.addItem(f"{stock.material_name} ({stock.quantity_available} available)")
        if self.ui.stock_results.count() == 0:
            self.ui.stock_results.addItem("No matching material found.")
            
    def update_professor_list(self):
        # Update professor dropdown based on selected program
        self.ui.professor.clear()
        program = self.ui.program.currentText()
        if "Computer Engineering" in program:
            self.ui.professor.addItems(["Engr. Jimlord Quejado", "Engr. Menchie Rosales", "Engr. Ji Han Gang", "Engr. Lloyd Pornobi"])
        elif "Electronics Engineering" in program:
            self.ui.professor.addItems(["Engr. Ryan Alimuin", "Engr. Oliver John Alajas"])
        elif "Electrical Engineering" in program:
            self.ui.professor.addItems(["Dr. Christine Ann Teodoro Alquero", "Engr. Vhander Ramos"])

    def add_item_to_table(self):
        name = self.ui.material_name_input.text().strip()
        qty = str(self.ui.quantity_spin.value())
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please type a material name first.")
            return
            
        # Add item row
        row_idx = self.ui.items_table.rowCount()
        self.ui.items_table.insertRow(row_idx)
        self.ui.items_table.setItem(row_idx, 0, QTableWidgetItem(name))
        self.ui.items_table.setItem(row_idx, 1, QTableWidgetItem(qty))
        
        self.ui.material_name_input.clear()
        self.ui.quantity_spin.setValue(1)

    def clear_table_items(self):
        # Clear items table
        self.ui.items_table.setRowCount(0)

    def process_submission(self):
        student_name = self.ui.student_name.text().strip()
        student_id = self.ui.student_id.text().strip()
        course_section = self.ui.course_section.text().strip()
        date_needed = self.ui.date_needed.date().toPyDate()
        
        # Validation checks
        if not student_name or not student_id:
            QMessageBox.warning(self, "Validation Error", "Please provide your student ID and Name before submitting.")
            return
        
        if self.ui.items_table.rowCount() == 0:
            QMessageBox.warning(self, "Validation Error", "Your request list is empty. Add at least one item first.")
            return
        
        # Format item list summary
        collected_items = []
        for r in range(self.ui.items_table.rowCount()):
            item_name = self.ui.items_table.item(r, 0).text()
            item_qty = self.ui.items_table.item(r, 1).text()
            collected_items.append(f"{item_name} (x{item_qty})")
        items_summary = ", ".join(collected_items)
            
        # Create request object
        request_id = len(self.shared_requests) + 1
        new_request = BorrowRequestData(request_id, student_id, student_name, course_section, date_needed, items_summary)
        new_request.timestamp_submitted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.shared_requests.append(new_request)
        
        # Export request entry to CSV file
        csv_filepath = "ITSO_maintenance_dashboard.csv"
        csv_handler = CSVFileReaderWriter()
        
        if not os.path.exists(csv_filepath):
            csv_handler.write(csv_filepath, ["Request ID", "Student ID", "Name", "Course Section", "Date Needed", "Items", "Status", "Lab ID", "Time Submitted", "Time Returned"])
            
        record_row = [
            str(new_request.request_id), new_request.student_id, new_request.name,
            new_request.course_section, str(new_request.date_needed), new_request.items, 
            new_request.status, new_request.lab_id, new_request.timestamp_submitted, new_request.timestamp_returned
        ]
        csv_handler.write(csv_filepath, record_row)
        
        QMessageBox.information(self, "Success", f"Borrowing request submitted successfully for {student_name}!")
        self.clear_entire_form()

    def clear_entire_form(self):
        # Reset form fields
        self.ui.student_id.clear()
        self.ui.student_name.clear()
        self.ui.course_section.clear()
        self.clear_table_items()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load optional stylesheet
    qss_filepath = Path(__file__).with_name("student.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
        
    window = StudentDashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(900, 200)
    window.show()
    sys.exit(app.exec())


from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication
from studentui import StudentDashboardApp
from pathlib import Path
import sys
class StudentDashboard(QWidget):
    def __init__(self):
        super().__init__()
        
        # creates an instance of the interface layout
        self.ui = StudentDashboardApp()
        self.ui.setupUi(self)
        
        #signals
        self.ui.add_item_btn.clicked.connect(self.add_item_to_table)
        self.ui.clear_items_btn.clicked.connect(self.clear_table_items)
        self.ui.submit_request_btn.clicked.connect(self.process_submission)

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
        
        # reset the material bar inputs
        self.ui.material_name_input.clear()
        self.ui.quantity_spin.setValue(1)

    def clear_table_items(self):
        self.ui.items_table.setRowCount(0)  # removes every added material item row from the display list table

    def process_submission(self):
        student_name = self.ui.student_name_input.text().strip()
        student_id = self.ui.student_id_input.text().strip()
        
        # shows a warning message box if the name field or identification field is blank
        if not student_name or not student_id:
            QMessageBox.warning(self, "Validation Error", "Please provide your student ID and Name before submitting.")
            return
        
        # shows an error message if the student tries to submit a completely empty table
        if self.ui.items_table.rowCount() == 0:
            QMessageBox.warning(self, "Validation Error", "Your request list is empty. Add at least one item first.")
            return
        
        # displays a confirmation that the request form was submitted
        QMessageBox.information(self, "Success", f"Borrowing request submitted successfully for {student_name}!")
        self.clear_entire_form()

    def clear_entire_form(self):
        #clears out all text entry fields and empties the main table list
        self.ui.student_id_input.clear()
        self.ui.student_name_input.clear()
        self.ui.course_sec_input.clear()
        self.clear_table_items()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # importing the student qss inside to merge the qss to the logic file
    qss_filepath = Path(__file__).with_name("student.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
        
    window = StudentDashboard()
    window.setWindowTitle("Lab Borrowing System")
    window.resize(600, 650)
    window.show()
    sys.exit(app.exec())
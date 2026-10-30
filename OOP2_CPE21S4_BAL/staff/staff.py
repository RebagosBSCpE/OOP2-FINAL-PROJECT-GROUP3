from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QPushButton, QApplication
from staffui import StaffDashboardApp
from pathlib import Path
import sys
class StaffDashboard(QWidget):
    def __init__(self, shared_requests_list=None):
        super().__init__()
        # saves the student requests list if it exists, or makes a new empty list if it is missing
        self.shared_requests = shared_requests_list if shared_requests_list is not None else []
        
        self.ui = StaffDashboardApp()
        self.ui.setupUi(self)
        
        # to fix the sizes so the text on the column would fit in the inventory table
        self.ui.inventory_table.resizeColumnsToContents()
        self.ui.inventory_table.horizontalHeader().setStretchLastSection(True)
        
        # fix sizes for the student requests table
        self.ui.orders_table.resizeColumnsToContents()
        # signal button for stock function
        self.ui.add_stock_btn.clicked.connect(self.add_inventory_stock)
        
        # fill up the tables with data when the program opens
        self.initialize_default_stock()
        self.display_student_requests()
        
    def initialize_default_stock(self):
        default_items = [("Resistors Combo Assortment", "250"), ("NPN Transistors 2N2222", "85"), ("Digital Multimeter Fluke", "14")]
        for item_name, quantity in default_items:
            row = self.ui.inventory_table.rowCount()
            self.ui.inventory_table.insertRow(row)
            self.ui.inventory_table.setItem(row, 0, QTableWidgetItem(item_name))
            self.ui.inventory_table.setItem(row, 1, QTableWidgetItem(quantity))

    def add_inventory_stock(self):
        item_name = self.ui.item_name_input.text().strip()
        quantity = str(self.ui.item_qty_spin.value())
        
        if not item_name:
            QMessageBox.warning(self, "Input Error", "Please provide a valid material component name identifier.")
            return

        # check if item exists to add, otherwise it create new row entry line
        for r in range(self.ui.inventory_table.rowCount()):
            if self.ui.inventory_table.item(r, 0).text().lower() == item_name.lower():
                current_qty = int(self.ui.inventory_table.item(r, 1).text())
                self.ui.inventory_table.setItem(r, 1, QTableWidgetItem(str(current_qty + int(quantity))))
                self.ui.item_name_input.clear()
                self.ui.item_qty_spin.setValue(1)
                return
        # if it's a brand new item model
        row = self.ui.inventory_table.rowCount()
        self.ui.inventory_table.insertRow(row)
        self.ui.inventory_table.setItem(row, 0, QTableWidgetItem(item_name))
        self.ui.inventory_table.setItem(row, 1, QTableWidgetItem(quantity))
        self.ui.item_name_input.clear()
        self.ui.item_qty_spin.setValue(1)

    def display_student_requests(self):
        # gets the list of student requests and shows it on the screen
        self.ui.orders_table.setRowCount(0)
        
        for idx, req in enumerate(self.shared_requests):
            row = self.ui.orders_table.rowCount()
            self.ui.orders_table.insertRow(row)
            self.ui.orders_table.setItem(row, 0, QTableWidgetItem(req.student_id))
            self.ui.orders_table.setItem(row, 1, QTableWidgetItem(req.name))
            self.ui.orders_table.setItem(row, 2, QTableWidgetItem(req.items))
            self.ui.orders_table.setItem(row, 3, QTableWidgetItem(req.status))
            
            # trigger action button
            action_btn = QPushButton("Release Items")
            action_btn.setObjectName("releaseBtn")
            
            # check the status to see if the button should be turned off if the request is not approved yet
            if req.status != "Approved":
                action_btn.setEnabled(False)
                if req.status == "Pending Approval":
                    action_btn.setText("Awaiting Approval")
                elif req.status == "Releases by Laboratory Staff":
                    action_btn.setText("Release")
                else:
                    action_btn.setText("Rejected Sheet")
                
            # saves the current row index inside the button so we know which row was clicked
            action_btn.setProperty("row_index", idx)
            # buttons and signals
            action_btn.clicked.connect(self.handle_release_click)
            self.ui.orders_table.setCellWidget(row, 4, action_btn)
        # to refresh the column widths after loading text rows
        self.ui.orders_table.resizeColumnsToContents()
    def release_items(self, target_request_idx):
        # changes the request status to show that items were given to the student
        req = self.shared_requests[target_request_idx]
        req.status = "Releases by Laboratory Staff"
        QMessageBox.information(self, "Inventory Released", f"Materials safely assigned and handed out to {req.name}.")
        self.display_student_requests()
        
    def handle_release_click(self):
        # identifies which button was clicked and reads its row number
        button = self.sender()
        if button:
            target_row = button.property("row_index")
            self.release_items(target_row)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # importing the staff qss inside to merge the qss to the logic file
    qss_filepath = Path(__file__).with_name("staff.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
        
    window = StaffDashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(600, 650)
    window.show()
    sys.exit(app.exec())
import sys
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QPushButton, QApplication
from staffui import StaffDashboardApp

class StaffDashboard(QWidget):
    def __init__(self, shared_requests_list=None):
        super().__init__()
        # Shared request data storage
        self.shared_requests = shared_requests_list if shared_requests_list is not None else []
        
        # UI setup
        self.ui = StaffDashboardApp()
        self.ui.setupUi(self)
        
        # Table column sizing
        self.ui.inventory_table.resizeColumnsToContents()
        self.ui.inventory_table.horizontalHeader().setStretchLastSection(True)
        self.ui.orders_table.resizeColumnsToContents()
        
        # Connect signals
        self.ui.add_stock_btn.clicked.connect(self.add_inventory_stock)
        
        # Populate initial table data
        self.initialize_default_stock()
        self.display_student_requests()
        
    def initialize_default_stock(self):
        # Initial stock records
        default_items = [
            ("Resistors Combo Assortment", "250"), 
            ("NPN Transistors 2N2222", "85"), 
            ("Digital Multimeter Fluke", "14")
        ]
        for item_name, quantity in default_items:
            row = self.ui.inventory_table.rowCount()
            self.ui.inventory_table.insertRow(row)
            self.ui.inventory_table.setItem(row, 0, QTableWidgetItem(item_name))
            self.ui.inventory_table.setItem(row, 1, QTableWidgetItem(quantity))

    def add_inventory_stock(self):
        item_name = self.ui.item_name_input.text().strip()
        quantity = str(self.ui.item_qty_spin.value())
        
        # Input validation
        if not item_name:
            QMessageBox.warning(self, "Input Error", "Please provide a valid material component name identifier.")
            return

        # Update existing item quantity
        for r in range(self.ui.inventory_table.rowCount()):
            if self.ui.inventory_table.item(r, 0).text().lower() == item_name.lower():
                current_qty = int(self.ui.inventory_table.item(r, 1).text())
                self.ui.inventory_table.setItem(r, 1, QTableWidgetItem(str(current_qty + int(quantity))))
                self.ui.item_name_input.clear()
                self.ui.item_qty_spin.setValue(1)
                return

        # Add new item row
        row = self.ui.inventory_table.rowCount()
        self.ui.inventory_table.insertRow(row)
        self.ui.inventory_table.setItem(row, 0, QTableWidgetItem(item_name))
        self.ui.inventory_table.setItem(row, 1, QTableWidgetItem(quantity))
        self.ui.item_name_input.clear()
        self.ui.item_qty_spin.setValue(1)

    def display_student_requests(self):
        # Refresh student requests table
        self.ui.orders_table.setRowCount(0)
        
        for idx, req in enumerate(self.shared_requests):
            row = self.ui.orders_table.rowCount()
            self.ui.orders_table.insertRow(row)
            self.ui.orders_table.setItem(row, 0, QTableWidgetItem(req.student_id))
            self.ui.orders_table.setItem(row, 1, QTableWidgetItem(req.name))
            self.ui.orders_table.setItem(row, 2, QTableWidgetItem(req.items))
            self.ui.orders_table.setItem(row, 3, QTableWidgetItem(req.status))
            
            # Action button setup
            action_btn = QPushButton("Release Items")
            action_btn.setObjectName("releaseBtn")
            
            # Status check and button state
            if req.status != "Approved":
                action_btn.setEnabled(False)
                if req.status == "Pending Approval":
                    action_btn.setText("Awaiting Approval")
                elif req.status == "Releases by Laboratory Staff":
                    action_btn.setText("Release")
                else:
                    action_btn.setText("Rejected Sheet")
                
            action_btn.setProperty("row_index", idx)
            action_btn.clicked.connect(self.handle_release_click)
            self.ui.orders_table.setCellWidget(row, 4, action_btn)

        self.ui.orders_table.resizeColumnsToContents()

    def release_items(self, target_request_idx):
        # Update request status to released
        req = self.shared_requests[target_request_idx]
        req.status = "Releases by Laboratory Staff"
        QMessageBox.information(self, "Inventory Released", f"Materials safely assigned and handed out to {req.name}.")
        self.display_student_requests()
        
    def handle_release_click(self):
        # Identify clicked button's row index
        button = self.sender()
        if button:
            target_row = button.property("row_index")
            self.release_items(target_row)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load optional application stylesheet
    qss_filepath = Path(__file__).with_name("staff.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
        
    window = StaffDashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(600, 650)
    window.show()
    sys.exit(app.exec())
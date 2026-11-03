from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QPushButton, QInputDialog
import os
from CSVFileReaderWriter import CSVFileReaderWriter
from InventoryManager import InventoryManager  
from Staff_UI import StaffDashboardApp
class StaffDashboard(QWidget):
    def __init__(self, shared_requests_list=None, inventory_manager=None):  
        super().__init__()
        # saves  the student requests list if it  exists, or  makes a  new empty list  if it is missing
        self.shared_requests  =  shared_requests_list if shared_requests_list is not None else []
        # inventory  that is saved in inventory_data.csv (shared  with the student  search box)
        self.inventory = inventory_manager if inventory_manager is not None else InventoryManager()  

        self.ui = StaffDashboardApp()
        self.ui.setupUi(self)
        
        # to  fix the  sizes so the text  on the  column  would fit in the inventory table
        self.ui.inventory_table.resizeColumnsToContents()
        self.ui.inventory_table.horizontalHeader().setStretchLastSection(True)
        
        # fix sizes for  the student  requests  table
        self.ui.orders_table.resizeColumnsToContents()
        # signal  button for  stock function
        self.ui.add_stock_btn.clicked.connect(self.add_inventory_stock)
        
        # fill up the tables  with data  when the program opens
        self.display_inventory()  
        self.display_student_requests()

    # whole function
    def display_inventory(self):
        # shows the live inventory (the same list that is saved  in  inventory_data.csv)
        self.ui.inventory_table.setRowCount(0)
        for stock in self.inventory.items:
            row   =   self.ui.inventory_table.rowCount()
            self.ui.inventory_table.insertRow(row)
            self.ui.inventory_table.setItem(row, 0, QTableWidgetItem(stock.material_name))
            self.ui.inventory_table.setItem(row, 1, QTableWidgetItem(str(stock.quantity_available)))
        self.ui.inventory_table.resizeColumnsToContents()

    def add_inventory_stock(self):
        item_name = self.ui.item_name_input.text().strip() 
        quantity  =   self.ui.item_qty_spin.value()  # (now a number instead of text)

        if not item_name:
            QMessageBox.warning(self, "Input Error", "Please provide a valid material component name identifier.")
            return

        # adds to the existing  item  or creates a new one, then saves inventory_data.csv
        try:
            self.inventory.add_stock(item_name, quantity)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Stock was added but Inventory_data.csv could not be saved (is it open in another program?):\n{e}")
        self.display_inventory()
        self.ui.item_name_input.clear()
        self.ui.item_qty_spin.setValue(1)

    def display_student_requests(self):
        # gets the  list  of student requests and  shows it on  the  screen
        self.ui.orders_table.setRowCount(0)
        
        for idx, req in enumerate(self.shared_requests):
            row = self.ui.orders_table.rowCount()
            self.ui.orders_table.insertRow(row)
            self.ui.orders_table.setItem(row, 0, QTableWidgetItem(req.student_id))
            self.ui.orders_table.setItem(row, 1, QTableWidgetItem(req.name))
            self.ui.orders_table.setItem(row, 2, QTableWidgetItem(req.items))
            self.ui.orders_table.setItem(row, 3, QTableWidgetItem(req.status))
            self.ui.orders_table.setItem(row, 4, QTableWidgetItem(req.lab_id if req.lab_id else "Not Assigned"))
            
            # trigger  action  button
            release_btn = QPushButton("Release Items") 
            release_btn.setObjectName("releaseBtn")
            
            # check the status to see  if the button should be turned off  if the request  is  not approved  yet
            if req.status ==  "Approved":   
                release_btn.setEnabled(True)
            else:
                release_btn.setEnabled(False)
                if req.status in ["Released by Laboratory Staff", "Pending Return Confirmation", "Returned / Completed"]:  
                    release_btn.setText("Released")
                else:
                    release_btn.setText("Unavailable")
                
            # saves the current  row index  inside  the button so  we know  which row was  clicked
            release_btn.setProperty("row_index", idx)
            # buttons  and signals
            release_btn.clicked.connect(self.handle_release_click)
            self.ui.orders_table.setCellWidget(row, 5, release_btn)
            
            confirm_return_btn = QPushButton("Confirm Return")
            confirm_return_btn.setObjectName("addStockBtn")

           
            if req.status == "Pending Return Confirmation":
                confirm_return_btn.setEnabled(True)
            else:
                confirm_return_btn.setEnabled(False)
                if req.status == "Returned / Completed":
                    confirm_return_btn.setText("Cleared")
                else:
                    confirm_return_btn.setText("Awaiting Return")
                    
            confirm_return_btn.setProperty("row_index", idx)
            confirm_return_btn.clicked.connect(self.handle_release_return_click)
            self.ui.orders_table.setCellWidget(row, 6, confirm_return_btn)
        
        # to refresh the column  widths after  loading  text  rows
        self.ui.orders_table.resizeColumnsToContents()
        
    def release_items(self, target_request_idx):
        # changes the request status to  show  that items were given to the  student
        req = self.shared_requests[target_request_idx]

        # makes sure every  requested  item exists in  the inventory and has  enough units  before releasing
        allocations, problems = self.inventory.check_request(req.items)
        if problems:
            QMessageBox.warning(self, "Cannot Release", "This request cannot be released:\n\n" + "\n".join(problems))
            return

        lab_id, confirm   =  QInputDialog.getText(self, "Lab Ticket ID", f"Enter the Lab Ticket ID for {req.name}'s request:")
        if not confirm or not lab_id.strip(): 
            QMessageBox.warning(self, "Action Cancelled", "A valid Lab ID Ticket Number assignment is required to release physical inventory items.")
            return
        req.lab_id = lab_id.strip()
        req.status = "Released by Laboratory Staff"
        self.save_to_csv()  # save the updated request status to the CSV file

        # takes the borrowed units out of the available  stock and saves inventory_data.csv
        try:
            self.inventory.borrow(allocations)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Inventory_data.csv could not be saved (is it open in another program?):\n{e}")
        self.display_inventory()
        QMessageBox.information(self, "Inventory Released", f"Materials safely assigned and handed out to {req.name}.")
        self.display_student_requests()
        
    def handle_release_click(self):
        button  = self.sender()
        if button:
            target_row = button.property("row_index")
            self.release_items(target_row)
        
    def handle_release_return_click(self):
        # identifies  which button was clicked and reads its  row  number
        button =  self.sender()
        if button:
            target_row =  button.property("row_index")
            req = self.shared_requests[target_row]

            req.status = "Returned / Completed" 
            self.save_to_csv()

            # puts the returned units back into  the available stock and  saves  inventory_data.csv
            try:
                self.inventory.return_items(req.items)
            except Exception as e:
                QMessageBox.warning(self, "Save Error", f"Inventory_data.csv could not be saved (is it open in another program?):\n{e}")
            self.display_inventory()
            QMessageBox.information(self, "Return Completed", f"Ticket [{req.lab_id}] cleared! Materials successfully verified and returned to storage shelves layout.")
            self.display_student_requests()
    
    def save_to_csv(self):
        csv_filepath = "ITSO_Maintenance_data.csv"
        csv_handler = CSVFileReaderWriter()  
        containers = ["Request ID", "Student ID", "Name", "Course Section", "Date Needed", "Items", "Status", "Lab ID", "Time Submitted", "Time Returned"]
        if os.path.exists(csv_filepath):
            os.remove(csv_filepath)
        csv_handler.write(csv_filepath, containers)
        for req in self.shared_requests:
            record_row  = [
                str(req.request_id), req.student_id, req.name, req.course_section,
                str(req.date_needed), req.items, req.status, req.lab_id,
                req.timestamp_submitted, req.timestamp_returned
            ]
            csv_handler.write(csv_filepath, record_row)
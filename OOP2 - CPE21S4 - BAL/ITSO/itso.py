import sys
import os
# importing the shutil to handle file operations like copying or deleting
# complete folder trees instead of rmdir because of limited usage and restrictions when deleting a data
from pathlib import Path
import shutil 
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QApplication, QFileDialog
from itsoui import ITSODashboardApp
from CSVFileReaderWriiter import CSVFileReaderWriter

class ITSODashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = ITSODashboardApp()
        self.ui.setupUi(self)
        self.csv_filepath = "itso_maintenance_dashboard.csv"
        self.csv_handler = CSVFileReaderWriter()
        
        self.ui.refresh_btn.clicked.connect(self.sync_csv_data)
        self.ui.gen_folder_btn.clicked.connect(self.generate_backup_folder)
        self.ui.del_folder_btn.clicked.connect(self.delete_backup_folder)
        
        # automatically sizes the table columns to fit the text inside them
        self.ui.log_table.resizeColumnsToContents()
        # locks the column widths permanently so they cannot be stretched or messed up to look neatly
        self.ui.log_table.horizontalHeader().setSectionResizeMode(self.ui.log_table.horizontalHeader().ResizeMode.Fixed)
        
        self.sync_csv_data()

    def sync_csv_data(self):
        self.ui.log_table.setRowCount(0)
        # checks if the log file exists before trying to read it
        if not os.path.exists(self.csv_filepath):
            # stops tops the function right here if the file is missing
            return
        try:
            self.new_data = self.csv_handler.read(self.csv_filepath)
            
            # checks if the loaded data matches the title header list
            # and adding index [0] to check if the first row matches to the 10 list of columns
            if self.new_data and self.new_data[0] == ["Request ID", "Student ID", "Name", "Course Section", "Date Needed", "Items", "Status", "Lab ID", "Time Submitted", "Time Returned"]:
                # skips the first row so it does not add column titles to the table cells
                rows_to_turn = self.new_data[1:] # runs only if the file matches, it cuts off the very first row (the column with titles) and passes the rest of the student data lines down to be loaded into the table grid slots
            # runs if the file does not have a title line at the top
            else:
                # keeps the full list because no header lines need to be skipped
                rows_to_turn = self.new_data

            # loops through each separate row line in the data file list
            for row_data in rows_to_turn:
                # discards blank rows to avoid empty spaces on the screen
                if not row_data or len(row_data) == 0:
                    continue # skips this line completely and moves to the next one
                row_idx = self.ui.log_table.rowCount()
                self.ui.log_table.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    # sets all columns limit to fit in the table width
                    if col_idx < 10: # access 3 more slots, allowing the program to read and display all 10 tracking columns 
                        # changes data to normal text and puts it directly into table cells
                        self.ui.log_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                # refreshes the column width after loading the new texts
                self.ui.log_table.resizeColumnsToContents() # adjusts the column boxes so that long timestamp strings fit and looks neat
                        
        except Exception as e:
            QMessageBox.critical(self, "File Error", f"Failed to load the file data:\n{e}")

    def generate_backup_folder(self):
        try:
            # opens a popup window so the user can select a folder on the computer
            path = QFileDialog.getExistingDirectory(self, "Select or Create Location for Backup", "")
            # makes sure the user actually clicked a folder instead of closing the popup
            if path:
                backup_dir = os.path.join(path, "ITSO_Backups")
                # checks if the backup folder does not exist on the computer yet
                if not os.path.exists(backup_dir):
                    # creates a brand new backup folder on the hard drive path
                    os.mkdir(backup_dir)
                
                # verifies if the current data log file is inside the project folder
                if os.path.exists(self.csv_filepath):
                    destination_file = os.path.join(backup_dir, "backup_log.csv")
                    # uses shutil.copy to safely clone the live csv file over into the backup folder location
                    shutil.copy(self.csv_filepath, destination_file)
                    QMessageBox.information(self, "Success", f"Backup folder has created and file saved at:\n{destination_file}")
                # if the log file cannot be found 
                else:
                    QMessageBox.warning(self, "Info", "Backup folder created, but no active student CSV log was found to copy.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot create backup system folder:\n{e}")

    def delete_backup_folder(self):
        try:
            # opens a popup window so the user can select which folder to erase
            folder = QFileDialog.getExistingDirectory(self, "Select ITSO_Backups Folder to Delete", "")
            # ensures a folder was chosen and checks that it actually exists on disk
            if folder and os.path.exists(folder):
                # uses shutil.rmtree to force delete the selected backup folder and all contents inside it
                shutil.rmtree(folder)
                QMessageBox.information(self, "Success", "Backup directory and all its logs removed successfully.")
            # activates if the folder path selection was left empty or cancelled
            else:
                QMessageBox.warning(self, "Error", "No folder was selected or the specific location does not exist.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Folder deletion process failed:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_filepath = Path(__file__).with_name("itso.qss")
    if qss_filepath.exists():
        app.setStyleSheet(qss_filepath.read_text())
    window = ITSODashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(1000, 650)
    window.show()
    sys.exit(app.exec())

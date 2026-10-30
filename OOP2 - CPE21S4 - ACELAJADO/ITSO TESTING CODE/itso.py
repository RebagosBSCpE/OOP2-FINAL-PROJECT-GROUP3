import sys
import os
# Importing shutil to handle advanced file operations like copying files 
# or deleting complete folder trees recursively (shutil.rmtree)
from pathlib import Path
import shutil 

# Importing PyQt6 UI widgets and core application modules
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QApplication, QFileDialog

# Importing custom user interface and helper file-handling classes
from itsoui import ITSODashboardApp
from CSVFileReaderWriiter import CSVFileReaderWriter

class ITSODashboard(QWidget):
    """
    Main application dashboard class for managing laboratory borrowing logs,
    refreshing log views, and generating/deleting backup folders.
    """
    def __init__(self):
        super().__init__()
        
        # Initialize and setup the UI components generated from Qt Designer / custom UI layout
        self.ui = ITSODashboardApp()
        self.ui.setupUi(self)
        
        # Default filename for storing active maintenance log records
        self.csv_filepath = "itso_maintenance_dashboard.csv"
        
        # Instantiate custom CSV handler to manage reading and writing operations
        self.csv_handler = CSVFileReaderWriter()
        
        # Connect UI button click signals to their respective handler functions
        self.ui.refresh_btn.clicked.connect(self.sync_csv_data)
        self.ui.gen_folder_btn.clicked.connect(self.generate_backup_folder)
        self.ui.del_folder_btn.clicked.connect(self.delete_backup_folder)
        
        # Automatically load and display CSV data when the dashboard launches
        self.sync_csv_data()

    def sync_csv_data(self):
        """
        Reads the CSV data file and populates the QTableWidget with maintenance records.
        """
        # Clear all existing table rows before loading fresh data
        self.ui.log_table.setRowCount(0)
        
        # Checks if the log CSV file exists on the system before attempting to read it
        if not os.path.exists(self.csv_filepath):
            # Terminate execution early if the file is missing
            return

        try:
            # Read all rows from the target CSV file using the custom file reader helper
            self.raw_data = self.csv_handler.read(self.csv_filepath)
            
            # Verify if raw_data is non-empty and check whether the first entry contains the header labels
            if self.raw_data and self.raw_data[0] == ["Request ID", "Student ID", "Name", "Course Section", "Date Needed", "Items", "Status"]:
                # Exclude the header row so column titles aren't added as table data cells
                rows_to_render = self.raw_data[1:]
            else:
                # If no header row exists, process the entire raw dataset directly
                rows_to_render = self.raw_data

            # Iterate through each data row parsed from the CSV file
            for row_data in rows_to_render:
                # Discard blank or empty rows to prevent blank spaces on the table UI
                if not row_data or len(row_data) == 0:
                    continue
                
                # Fetch current row count to append the new row index at the bottom of the table
                row_idx = self.ui.log_table.rowCount()
                self.ui.log_table.insertRow(row_idx)
                
                # Loop through each individual field/column value in the row entry
                for col_idx, value in enumerate(row_data):
                    # Enforce a maximum column boundary limit (7 columns) to match table constraints
                    if col_idx < 7:
                        # Convert data entry to string and place it in the matching table cell
                        self.ui.log_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                        
        except Exception as e:
            # Display a pop-up error dialog if an unhandled exception occurs during file reading
            QMessageBox.critical(self, "File Error", f"Failed to load the file data:\n{e}")

    def generate_backup_folder(self):
        """
        Prompts user to select a base directory, creates an 'ITSO_Backups' directory, 
        and copies the active CSV log file into it.
        """
        try:
            # Open a file dialog enabling the user to choose a target parent folder on disk
            path = QFileDialog.getExistingDirectory(self, "Select or Create Location for Backup", "")
            
            # Verify that the user selected a valid directory path rather than cancelling
            if path:
                # Construct path for the dedicated backup directory inside chosen location
                backup_dir = os.path.join(path, "ITSO_Backups")
                
                # Check whether the backup folder already exists; create it if missing
                if not os.path.exists(backup_dir):
                    os.mkdir(backup_dir)
                
                # Verify that the active live CSV log file exists before attempting to copy it
                if os.path.exists(self.csv_filepath):
                    dest_file = os.path.join(backup_dir, "backup_log.csv")
                    
                    # Copy the live CSV log file into the newly specified backup directory location
                    shutil.copy(self.csv_filepath, dest_file)
                    
                    # Notify user of successful backup operation
                    QMessageBox.information(self, "Success", f"Backup folder created and file saved at:\n{dest_file}")
                else:
                    # Alert user if backup folder was created but no log file was available to copy
                    QMessageBox.warning(self, "Info", "Backup folder created, but no active student CSV log was found to copy.")
        except Exception as e:
            # Notify user if any filesystem or permission error occurs during execution
            QMessageBox.warning(self, "Error", f"Cannot create backup system folder:\n{e}")

    def delete_backup_folder(self):
        """
        Prompts user to select an existing 'ITSO_Backups' folder and permanently deletes it 
        and all its contained files using recursive directory removal.
        """
        try:
            # Open file selection dialog allowing user to choose directory to erase
            folder = QFileDialog.getExistingDirectory(self, "Select ITSO_Backups Folder to Delete", "")
            
            # Ensure path string is not empty and verify that directory exists on local disk
            if folder and os.path.exists(folder):
                # Recursively delete target folder and all subdirectories/files contained within it
                shutil.rmtree(folder)
                
                # Notify user of successful removal operation
                QMessageBox.information(self, "Success", "Backup directory and all its logs removed successfully.")
            else:
                # Trigger error popup if no valid folder was selected or folder path doesn't exist
                QMessageBox.warning(self, "Error", "No folder was selected or target location does not exist.")
        except Exception as e:
            # Handle unexpected errors during folder deletion process
            QMessageBox.warning(self, "Error", f"Folder deletion process failed:\n{e}")

# Application Entry Point
if __name__ == "__main__":
    # Initialize the main Qt Application instance
    app = QApplication(sys.argv)
    
    # Locate optional Qt Style Sheet (.qss) file in the same directory as this script
    qss_filepath = Path(__file__).with_name("itso.qss")
    if qss_filepath.exists():
        # Apply visual stylesheet rules to the application instance
        app.setStyleSheet(qss_filepath.read_text())
        
    # Instantiate, configure, and exhibit the main dashboard window widget
    window = ITSODashboard()
    window.setWindowTitle("Laboratory Borrowing System")
    window.resize(850, 500)
    window.show()
    
    # Start the application loop and pass system exit status upon termination
    sys.exit(app.exec())
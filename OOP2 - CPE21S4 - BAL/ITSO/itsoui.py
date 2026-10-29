from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget

class ITSODashboardApp(object):
    def setupUi(self, widget):
        
        widget.setObjectName("ITSODashboard")
        
        self.main_layout = QVBoxLayout(widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)

        self.title = QLabel("ITSO Maintenance Dashboard")
        self.title.setObjectName("pageTitle")

        self.subtitle = QLabel("Checks student request files that are saved automatically in the table.")
        self.subtitle.setObjectName("pageSubtitle")
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.subtitle)

        self.controls_layout = QHBoxLayout()
        self.table_label = QLabel("Synchronized ITSO Network Device Records:")
        self.table_label.setObjectName("sectionLabel")
        
        self.refresh_btn = QPushButton("Sync / Refresh CSV Log")
        self.refresh_btn.setObjectName("refreshBtn")
        self.gen_folder_btn = QPushButton("Generate Backup Folder")
        self.gen_folder_btn.setObjectName("refreshBtn")
        self.del_folder_btn = QPushButton("Delete Backup Folder")
        self.del_folder_btn.setObjectName("refreshBtn")
        
        self.controls_layout.addWidget(self.table_label)
        
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.refresh_btn)
        self.controls_layout.addWidget(self.gen_folder_btn)
        self.controls_layout.addWidget(self.del_folder_btn)
        self.main_layout.addLayout(self.controls_layout)

        self.log_table = QTableWidget(0, 10)
        self.log_table.setHorizontalHeaderLabels([
            "Request ID", "Student ID", "Student Name", "Course & Sec", "Date Needed", "Requested Items", "System Status", "Lab ID", "Time Submitted", "Time Returned"
        ])
        self.log_table.setMinimumHeight(350)
        self.main_layout.addWidget(self.log_table)
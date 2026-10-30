from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QDateEdit, QSpinBox, QPushButton, 
    QTableWidget, QFormLayout, QListWidget, QWidget
)
from PyQt6.QtCore import QDate, Qt

class StudentDashboardApp(QWidget):
    def setupUi(self, widget):
        # Set main widget object name for stylesheet selectors
        widget.setObjectName("StudentDashboard")
        
        # Main vertical layout setup
        self.main_layout = QVBoxLayout(widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)

        # Title & Subtitle labels
        self.title = QLabel("Student Request Form Dashboard")
        self.title.setObjectName("pageTitle")

        self.subtitle = QLabel("Submit a material request and follow its approval status.")
        self.subtitle.setObjectName("pageSubtitle")
        
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.subtitle)

        # Form layout for student info input
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)

        # Input fields setup
        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("Input your studen number here e.g. 289298213")

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Input your name here e.g. Alex Dela Cruz")

        self.year_combo = QComboBox()
        self.year_combo.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"])

        self.course_section = QLineEdit()
        self.course_section.setPlaceholderText("Input your section here e.g. CPE21S4")

        self.program = QComboBox()
        self.program.addItems(["BS Computer Engineering", "BS Electronics Engineering", "BS Electrical Engineering"])

        self.date_needed = QDateEdit(QDate.currentDate())
        self.date_needed.setCalendarPopup(True)
        self.date_needed.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.professor = QComboBox()
        self.professor.addItems(["Engr. Jimlord Quejado", "Engr. Menchie Rosales", "Engr. Ji Han Gang"])

        # Populate form layout rows
        self.form_layout.addRow("Student ID:", self.student_id)
        self.form_layout.addRow("Student Name:", self.student_name)
        self.form_layout.addRow("Year Level:", self.year_combo)
        self.form_layout.addRow("Course & Section:", self.course_section)
        self.form_layout.addRow("Academic Program:", self.program)
        self.form_layout.addRow("Date Needed:", self.date_needed)
        self.form_layout.addRow("Assigned Professor:", self.professor)
        self.main_layout.addLayout(self.form_layout)
        
        # Announcements section
        self.announcements_label = QLabel("Active Bulletins & Professor Announcements:")
        self.announcements_label.setObjectName("sectionLabel")
        self.main_layout.addWidget(self.announcements_label)
        
        self.announcements_list = QListWidget()
        self.announcements_list.setMinimumHeight(80)
        self.main_layout.addWidget(self.announcements_list)
        
        # Search stock section
        self.stock_search_label = QLabel("Search Material Availability:")  
        self.stock_search_label.setObjectName("sectionLabel")  
        self.main_layout.addWidget(self.stock_search_label)  
        
        self.stock_search_input = QLineEdit()  
        self.stock_search_input.setPlaceholderText("Search a material here e.g. Resistor")  
        self.main_layout.addWidget(self.stock_search_input)  
        
        self.stock_results = QListWidget()  
        self.stock_results.setMinimumHeight(80)  
        self.main_layout.addWidget(self.stock_results)
        
        # Material addition controls section
        self.material_label = QLabel("Add Materials to Request:")
        self.material_label.setObjectName("sectionLabel")
        self.main_layout.addWidget(self.material_label)
        
        self.material_entry_layout = QHBoxLayout()
        self.material_name_input = QLineEdit()
        self.material_name_input.setPlaceholderText("Material Name (e.g. Trasistor, Resistor, etc.)")
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 99)
        self.quantity_spin.setValue(1)
        
        self.add_item_btn = QPushButton("Add Item")
        self.add_item_btn.setObjectName("addItemBtn")
        
        self.material_entry_layout.addWidget(self.material_name_input, 4)
        self.material_entry_layout.addWidget(QLabel("Quantity:"))
        self.material_entry_layout.addWidget(self.quantity_spin, 1)
        self.material_entry_layout.addWidget(self.add_item_btn, 1)
        self.main_layout.addLayout(self.material_entry_layout)
        
        # Table list section for added materials
        self.section_label = QLabel("Materials that have been added")
        self.section_label.setObjectName("boldSectionLabel")
        self.main_layout.addWidget(self.section_label)
        
        self.items_table = QTableWidget(0, 2)
        self.items_table.setHorizontalHeaderLabels(["Material Name", "Quantity"])
        self.items_table.setMinimumHeight(120)
        self.main_layout.addWidget(self.items_table)
        
        # Bottom action buttons layout
        self.actions_layout = QHBoxLayout()
        self.clear_items_btn = QPushButton("Clear Items")
        self.clear_items_btn.setObjectName("clearItemsBtn")
        
        self.submit_request_btn = QPushButton("Submit Borrowing Request")
        self.submit_request_btn.setObjectName("submitRequestBtn")
        
        self.actions_layout.addWidget(self.clear_items_btn)
        self.actions_layout.addStretch()
        self.actions_layout.addWidget(self.submit_request_btn)
        self.main_layout.addLayout(self.actions_layout)
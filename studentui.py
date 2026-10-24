from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QDateEdit, QSpinBox, QPushButton, 
    QTableWidget, QFormLayout
)
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import QDate, Qt

class StudentDashboardApp(object):
    def setupUi(self, widget):
        
        #include the main widget container name so it matches the style sheet selectors
        widget.setObjectName("StudentDashboard")
        
        # vertical layout to stack elements straight down from top to bottom
        self.main_layout = QVBoxLayout(widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)

        # puts the main header text label for the top of the dashboard
        self.title = QLabel("Student Dashboard Workspace")
        self.title.setObjectName("pageTitle")

        # display a smaller subtitle text explanation block below the main title
        self.subtitle = QLabel("Submit a material request and follow its approval status.")
        self.subtitle.setObjectName("pageSubtitle")
        # puts both header text lines into the main vertical layout stack
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.subtitle)

        # form layout that automatically lines up input fields with labels
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)

        # input line box for typing a student's ID
        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("e.g. 289298213")

        # input line box for typing the full name of the student
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("e.g. Alex Dela Cruz")

        # drop down menu list for picking a school year level
        self.year_combo = QComboBox()
        self.year_combo.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"])

        # input line box for typing a course name and section
        self.course_section = QLineEdit()
        self.course_section.setPlaceholderText("e.g. BSCpE 3-1")

        # drop down menu list for choosing program
        self.program = QComboBox()
        self.program.addItems(["BS Computer Engineering", "BS Electronics Engineering", "BS Electrical Engineering"])

        # choosing a date that starts on the current calendar day
        self.date_needed = QDateEdit(QDate.currentDate())
        self.date_needed.setCalendarPopup(True)
        # aligns the date text cleanly to the left edge of the entry box
        self.date_needed.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # drop down menu list for selecting an approving laboratory instructor
        self.professor = QComboBox()
        self.professor.addItems(["Engr. Jimlord Quejado", "Engr. Menchie Rosales", "Engr. Ji Han Gang"])

        # to pair each description string side by side with its matching input box
        self.form_layout.addRow("Student ID:", self.student_id)
        self.form_layout.addRow("Student Name:", self.student_name)
        self.form_layout.addRow("Year Level:", self.year_combo)
        self.form_layout.addRow("Course & Section:", self.course_section)
        self.form_layout.addRow("Academic Program:", self.program)
        self.form_layout.addRow("Date Needed:", self.date_needed)
        self.form_layout.addRow("Assigned Professor:", self.professor)
        self.main_layout.addLayout(self.form_layout)

        # horizontal material entry row
        self.material_label = QLabel("Add Materials to Request:")
        self.material_label.setObjectName("sectionLabel")
        # inserts the completed double column form block into the vertical main layout
        self.main_layout.addWidget(self.material_label)
        
        # horizontal row layout to line up item addition tools from left to right
        self.material_entry_layout = QHBoxLayout()
        # text entry box for typing equipment and component names
        self.material_name_input = QLineEdit()
        self.material_name_input.setPlaceholderText("Material Name (e.g. Trasistor, Resistor, etc.)")
        
        # creates a number box with up and down arrow adjusters for the quantity
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 99)
        self.quantity_spin.setValue(1)
        
        # buttons to click add items into the display list
        self.add_item_btn = QPushButton("Add Item")
        self.add_item_btn.setObjectName("addItemBtn")
        
        # arranges the text field, quantity number box, and add button in a single row
        self.material_entry_layout.addWidget(self.material_name_input, 4)
        self.material_entry_layout.addWidget(QLabel("Quantity:"))
        
        self.material_entry_layout.addWidget(self.quantity_spin, 1)
        self.material_entry_layout.addWidget(self.add_item_btn, 1)
        self.main_layout.addLayout(self.material_entry_layout)
        
        # section title label and applies a custom identifier name to it
        self.section_label = QLabel("<b>Add Materials to Request:</b>")
        self.section_label.setObjectName("boldSectionLabel")
        # adds the item section label and the horizontal tool row to the page 
        self.main_layout.addWidget(self.section_label)
        self.main_layout.addLayout(self.material_entry_layout)
        
        # table grid with zero starting rows and two labeled columns
        self.items_table = QTableWidget(0, 2)
        self.items_table.setHorizontalHeaderLabels(["Material Name", "Quantity"])
        self.items_table.setMinimumHeight(120)
        
        # puts the grid view table right under the horizontal material entry line
        self.main_layout.addWidget(self.items_table)
        
        # horizontal row layout for the action buttons at the bottom
        self.actions_layout = QHBoxLayout()
        # button to clear out all rows from the table display
        self.clear_items_btn = QPushButton("Clear Items")
        self.clear_items_btn.setObjectName("clearItemsBtn")
        
        # button to submit the final borrowing list to the instructor
        self.submit_request_btn = QPushButton("Submit Borrowing Request")
        self.submit_request_btn.setObjectName("submitRequestBtn")
        
        # adds an empty space that pushes the clear button to the left and submit to the right.
        self.actions_layout.addWidget(self.clear_items_btn)
        self.actions_layout.addStretch()
        self.actions_layout.addWidget(self.submit_request_btn)
        self.main_layout.addLayout(self.actions_layout)
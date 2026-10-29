from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QTextEdit, QPushButton, QTableWidget, QLineEdit)

class ProfessorDashboardApp(QWidget):
    def setupUi(self, widget):
        
        # to identify the layout container box name so it matches style sheet rules
        widget.setObjectName("ProfessorDashboard")
        
        # layout that stacks widgets straight down from top to bottom
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # main display title text label
        title = QLabel("Professor Dashboard")
        title.setObjectName("pageTitle")
        
        # smaller secondary explanation text line label
        subtitle = QLabel("Review student requests, log decision parameters, and update status.")
        subtitle.setObjectName("pageSubtitle")
        
        # adds both header elements down into the vertical layout stack
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # creates a structural section descriptor text label widget
        table_label = QLabel("Incoming Material Requests Awaiting Review:")
        table_label.setObjectName("sectionLabel")
        main_layout.addWidget(table_label)

        # creates a grid view presentation table with zero rows and six columns
        self.requests_table = QTableWidget(0, 7)
        self.requests_table.setHorizontalHeaderLabels([
            "Request Student ID", "Student Name", "Course & Section", "Date Needed", "Requested Items", "Status", "Time Submitted"
        ])
        self.requests_table.setMinimumHeight(220)
        main_layout.addWidget(self.requests_table)

        #announcement feature
        # text label header for the announcement writing section
        announcement_label = QLabel("Publish New Announcement to Students:")
        announcement_label.setObjectName("sectionLabel")
        main_layout.addWidget(announcement_label)

        # text box row layout to align the input field and publish button horizontally
        announcement_row = QHBoxLayout()
        
        # text entry box for typing out lab announcement text
        self.announcement_input = QLineEdit()
        self.announcement_input.setPlaceholderText("e.g. Lab items must be returned before 4:00 PM today.")
        
        # clickable action button to publish the announcement text
        self.publish_btn = QPushButton("Publish")
        self.publish_btn.setObjectName("publishBtn")
        
        # arranges the announcement box and send button side by side in the row
        announcement_row.addWidget(self.announcement_input, 4)
        announcement_row.addWidget(self.publish_btn, 1)
        main_layout.addLayout(announcement_row)
        
        # text label header for the decision feedback section
        comment_label = QLabel("Decision Comment / Rejection Reason (Required if Rejecting):")
        comment_label.setObjectName("sectionLabel")
        main_layout.addWidget(comment_label)

        # multi line comment box with helpful instructional hint text
        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText("Enter feedback note here, e.g., 'Approved. Return before 5:00 PM.'")
        self.comment_input.setMaximumHeight(80)
        main_layout.addWidget(self.comment_input)

        # horizontal strip layout row for the main action buttons
        actions_layout = QHBoxLayout()
        
        # decline button action trigger component
        self.reject_btn = QPushButton("Decline Request")
        self.reject_btn.setObjectName("rejectBtn")
        
        # approval button action trigger component
        self.approve_btn = QPushButton("Approve Request")
        self.approve_btn.setObjectName("approveBtn")
        
        # adds an empty space that pushes the reject button to the left and approve to the right
        actions_layout.addWidget(self.reject_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(self.approve_btn)
        
        # inserts the completed button strip row down into the page layout
        main_layout.addLayout(actions_layout)
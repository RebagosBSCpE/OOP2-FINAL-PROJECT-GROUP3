from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QTableWidget

class StaffDashboardApp(QWidget):
    def setupUi(self, widget):
        widget.setObjectName("StaffDashboard")
        
        self.main_layout = QVBoxLayout(widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)

        self.title = QLabel("Laboratory Stockroom & Staff Dashboard")
        self.title.setObjectName("pageTitle")

        self.subtitle = QLabel("Manage physical hardware count tracking and release verified inventory.")
        self.subtitle.setObjectName("pageSubtitle")
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.subtitle)

        # inventory adjustment for updating stock row controls
        self.inv_label = QLabel("Item Stock Procurement Adjuster:")
        self.inv_label.setObjectName("sectionLabel")
        self.main_layout.addWidget(self.inv_label)

        self.entry_layout = QHBoxLayout()
        self.item_name_input = QLineEdit()
        self.item_name_input.setPlaceholderText("Component Name (e.g. Oscilloscope, Arduino)")
        
        self.item_qty_spin = QSpinBox()
        self.item_qty_spin.setRange(1, 999)
        
        self.add_stock_btn = QPushButton("Update / Add Stock")
        self.add_stock_btn.setObjectName("addStockBtn")

        self.entry_layout.addWidget(self.item_name_input, 4)
        self.entry_layout.addWidget(QLabel("Qty:"))
        self.entry_layout.addWidget(self.item_qty_spin, 1)
        self.entry_layout.addWidget(self.add_stock_btn, 1)
        self.main_layout.addLayout(self.entry_layout)

        # table of showing the current items in the stock
        self.stock_label = QLabel("Current On-Hand Stock Inventory Ledger:")
        self.stock_label.setObjectName("sectionLabel")
        self.main_layout.addWidget(self.stock_label)

        self.inventory_table = QTableWidget(0, 2)
        self.inventory_table.setHorizontalHeaderLabels(["Material/Hardware Model", "Units Available"])
        self.inventory_table.setMinimumHeight(150)
        self.main_layout.addWidget(self.inventory_table)

        # label for student requests section
        self.student_req = QLabel("Verified Request Release:")
        self.student_req.setObjectName("sectionLabel")
        self.main_layout.addWidget(self.student_req)

        # table showing active student requests and their tracking status
        self.orders_table = QTableWidget(0, 5)
        self.orders_table.setHorizontalHeaderLabels(["Student ID", "Borrower", "Requested Items", "Approval Status", "Releases"])
        self.orders_table.setMinimumHeight(180)
        self.main_layout.addWidget(self.orders_table)
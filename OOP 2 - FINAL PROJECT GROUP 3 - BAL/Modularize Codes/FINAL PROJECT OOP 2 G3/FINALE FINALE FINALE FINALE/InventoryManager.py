# whole file: keeps the stock list and  saves it to inventory_data.csv
import os
import re
from datetime import datetime
from CSVFileReaderWriter import CSVFileReaderWriter
from Data_Model import StockMaterials

# column titles of the  inventory csv  file
INVENTORY_HEADER = ["Material Name", "Total Stock", "Available", "Borrowed", "Last Updated"]

# starting  stock used only when the inventory csv does  not  exist  yet
DEFAULT_STOCK = [
    ("Resistors Combo Assortment", 250),
    ("NPN Transistors 2N2222", 85),
    ("Digital Multimeter Fluke", 14),
]

class InventoryManager:
    # keeps the  stockroom  list in memory and  mirrors every change into  inventory_data.csv
    def __init__(self , filepath = "Inventory_data.csv"):
        self.filepath = filepath
        self.csv_handler =  CSVFileReaderWriter()
        # this  list is shared  with the  other dashboards, so it is only ever  changed in place
        self.items = []
        self.load()

    # file handling
    def load(self):
        loaded = []
        if os.path.exists (self.filepath):
            try:
                rows = self.csv_handler.read (self.filepath)
                for row in rows:
                    if not row or len(row) < 3 or str(row[0]).strip()  == "Material Name":
                        continue
                    loaded.append(StockMaterials(
                        item_name=str(row[0]).strip() ,
                        total=int(row[1]) ,
                        available=int(row[2]) ,
                        borrowed=int(row[3]) if len(row) > 3 and row[3] != "" else 0,
                        last_updated=row[4] if len(row) > 4 else ""))
            except Exception as e:
                print(f"Could not read inventory file, using default stock: {e}")
                loaded = []

        if not loaded:
            stamp =  self.now()
            loaded = [StockMaterials(n , q , last_updated = stamp) for n, q in DEFAULT_STOCK]

        self.items[:] = loaded
        # creates  the  file on first run  so it always exists next to the program
        if not os.path.exists (self.filepath):
            self.save()

    def save(self):
        # writes to a temporary file first, then swaps it in, so a crash  never  leaves a  half  written file
        temp_path = self.filepath +  ".tmp"
        if os.path.exists (temp_path):
            os.remove (temp_path)
        self.csv_handler.write (temp_path , INVENTORY_HEADER)
        for s in self.items:
            self.csv_handler.write(temp_path, [
                s.material_name, str(s.total_stock), str(s.quantity_available),
                str(s.quantity_borrowed), s.last_updated])
        os.replace( temp_path , self.filepath)

    @staticmethod
    def now():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    # staff adds stock 
    def add_stock(self, name, qty):
        # adds  to  an existing item (same name, any  capitalisation) or  creates a brand new one
        stamp = self.now()
        for s in self.items:
            if s.material_name.lower() == name.lower():
                s.total_stock += qty
                s.quantity_available +=  qty
                s.last_updated  =  stamp
                self.save()
                return s
        new_item = StockMaterials(name , qty , last_updated  =  stamp)
        self.items.append(new_item)
        self.save()
        return new_item

    # borrowing / returning
    @staticmethod
    def parse_items(items_text):
        # turns "resistor (x3), transistor (x4)" into [("resistor", 3), ("transistor", 4)]
        return [(n.strip(), int(q)) for n, q in re.findall(r"([^,]+?)\s*\(x(\d+)\)", items_text)]
    def find_item(self, requested_name):
        # exact  name  first, then a  name  that contains / is contained  in what the  student  typed
        key = requested_name.strip().lower()
        for s in self.items:
            if s.material_name.lower() == key: 
                return s
        matches = [s for s in self.items
                   if key in s.material_name.lower() or s.material_name.lower() in key]
        return matches[0] if len (matches) == 1  else None

    def resolve_request(self, items_text):
        # matches  every  requested  line  to  a  stock item; returns ([(stock, qty)], [problem messages])
        wanted = {}
        problems  = []
        parsed =  self.parse_items(items_text) 
        if not parsed:
            problems.append ("The request items could not be read.")
        for name, qty in parsed:
            stock = self.find_item (name)
            if stock is None:
                problems.append (f"'{name}' is not in the inventory (or matches more than one item).")
            else:
                entry = wanted.setdefault(id(stock), [stock, 0])
                entry[1]  += qty
        return [tuple(e) for e in wanted.values()] , problems

    def check_request( self, items_text):
        # same as resolve_request but  also reports items that do not have  enough units left
        allocations , problems = self.resolve_request (items_text)
        for stock , qty in allocations:
            if qty > stock.quantity_available:
                problems.append(f"{stock.material_name}: needs {qty} , only {stock.quantity_available} available.")
        return allocations , problems

    def borrow( self, allocations):
        # takes  the  borrowed  units  out  of  available
        stamp   = self.now()
        for stock, qty in allocations:
            stock.quantity_available -= qty
            stock.quantity_borrowed +=  qty
            stock.last_updated =  stamp
        self.save()

    def return_items( self , items_text):
        # puts  returned  units  back  into  available (never more  than  what is  recorded  as  borrowed)
        allocations, problems = self.resolve_request (items_text)
        stamp = self.now()
        for stock, qty in allocations:
            back = min( qty , stock.quantity_borrowed)
            stock.quantity_available += back  
            stock.quantity_borrowed -= back
            stock.last_updated = stamp
        self.save()
        return problems    
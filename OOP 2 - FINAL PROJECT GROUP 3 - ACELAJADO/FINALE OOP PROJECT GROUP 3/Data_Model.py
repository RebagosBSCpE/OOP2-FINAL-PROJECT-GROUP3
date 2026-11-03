from datetime import date

class BorrowRequestData:
    def __init__(self, request_id: int, student_id: str, name: str, course_section: str, date_needed: date, items: str):
        # to keep track  of  all data  each  inside  a single borrowing request  object
        self.request_id = request_id
        self.student_id = student_id
        self.name = name
        self.course_section = course_section
        self.date_needed = date_needed
        self.items = items  
        self.status   = "Pending Approval"
        # to  store  the laboratory tracking  number  assigned  when  staff releases  items
        self.lab_id = ""
        # records the exact date  and time when the student sends  the form
        self.timestamp_submitted   =  ""
        # records the exact date and time when the  materials  are brought  back
        self.timestamp_returned = ""

# moved here from main.py and extended  with total / borrowed / last updated
class StockMaterials:
    def __init__(self, item_name: str, total: int, available: int = None, borrowed: int = 0, last_updated: str = ""):
        # one line of the stockroom  inventory
        self.material_name = item_name
        self.total_stock = int(total)
        # units currently on the  shelf (total minus the ones borrowed)
        self.quantity_available = int(total) if available is None else int(available)
        # units currently with  students
        self.quantity_borrowed = int(borrowed)
        self.last_updated = last_updated

class Announcement:
    def __init__(self, author: str, message: str, time_posted: str):
        # keeps  track of a single announcement  message published by  a  laboratory instuctor
        self.author = author
        self.message = message
        self.time_posted = time_posted
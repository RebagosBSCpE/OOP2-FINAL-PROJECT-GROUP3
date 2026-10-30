from datetime import date

class BorrowRequestData:
    """Data model representing an individual student borrowing request."""
    def __init__(self, request_id: int, student_id: str, name: str, course_section: str, date_needed: date, items: str):
        # Unique identifier and student credentials
        self.request_id = request_id
        self.student_id = student_id
        self.name = name
        self.course_section = course_section
        self.date_needed = date_needed
        self.items = items
        
        # Request status and tracking metadata
        self.status = "Pending Approval"
        self.lab_id = ""
        self.timestamp_submitted = ""
        self.timestamp_returned = ""

class Announcement:
    """Data model representing a broadcast announcement from an instructor."""
    def __init__(self, author: str, message: str, time_posted: str):
        self.author = author
        self.message = message
        self.time_posted = time_posted
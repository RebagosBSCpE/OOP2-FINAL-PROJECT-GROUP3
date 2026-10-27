from FileReader import FileReaderWriter
import csv

    # this file and function is used for converting the borrowing slip of the student
    # from the student dashboard into CSV file and received to the ITSO dashboard
    
class CSVFileReaderWriter(FileReaderWriter):
    def read(self, filepath):
        with open(filepath, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',', quotechar='|')
            return list(data)
        
    def write(self, filepath, data):
        # Open in append 'a' mode so new student requests accumulate without deleting old rows
        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data)
# create our parent class
class FileReaderWriter():
    # base layout for reading files that returns an empty list if not changed
    def read(self):
        print("This is the default read method")
    # returns an empty list as a safety backup to prevent the program from crashing if no data is found
        return[]
    # base layout for writing data into files
    def write(self):
        print("This is the default write method")
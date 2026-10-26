# create our parent class
class FileReaderWriter():
    def read(self):
        print("This is the default read method")
        # returns an empty list as a safety backup to prevent the program from crashing if no data is found
        return[]
    def write(self):
        print("This is the default write method")
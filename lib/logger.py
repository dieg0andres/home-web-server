from datetime import datetime
from lib.config import LOG_FILENAME


class Logger:

    def __init__(self, filename=None):

        if filename == None:
            self.filename = LOG_FILENAME
        else:
            self.filename = filename

    def log(self, author, message):
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")

        with open(self.filename, "a") as file_object:
            file_object.write(now + ' ' + author + ' ' + message + '\n')

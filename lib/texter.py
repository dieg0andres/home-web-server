import smtplib

from lib.config import GMAIL_SMTP


class Texter:

    def __init__(self, EMAIL, PSSWD, PHONE_NUMBER):
        self.EMAIL = EMAIL
        self.PSSWD = PSSWD
        self.PHONE_NUMBER = PHONE_NUMBER


    def text(self, message):
        server = smtplib.SMTP(GMAIL_SMTP, 587)
        server.starttls()
        server.login(self.EMAIL, self.PSSWD)
        server.sendmail(self.EMAIL, self.PHONE_NUMBER, message)

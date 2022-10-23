import requests

from flask import render_template, redirect, request
from lib.config import *
from lib.helpers import *
from lib.logger import Logger
from lib.secrets import *
from lib.texter import Texter


class Request_Manager:

    def __init__(self, MAIL, PSSWD, PHONE_NUMBER, LOG_FILE_NAME):
        self.texter = Texter(MAIL, PSSWD, PHONE_NUMBER)
        self.logger = Logger(LOG_FILE_NAME)
        set_door_status(UNKNOWN)


    def handle_home(self):
        door_status = get_door_status()
        return render_template(HOME, door_status=door_status)


    def handle_log(self, author, message):
        self.logger.log(author, message)
        return "message added to log"


    def handle_garage_door_controller(self, command):
        response = ''

        if command == OPEN_CLOSE_DOOR:
            print('HOME_SERVER sent GARAGE_DOOR_CONTROLLER command to OPEN_CLOSE_DOOR')
            response = requests.get(GARAGE_DOOR_CONTROLLER + '/' + OPEN_CLOSE_DOOR)

            if response.text == 'success':
                response = 'GARAGE_DOOR_CONTROLLER successfully received command to OPEN_CLOSE_DOOR'

            else:
                response = response.text

        elif command == SET_DOOR_STATUS:
            print('HOME_SERVER received SET_DOOR_STATUS command')
            door_status = request.args.get('door_status')
            set_door_status(door_status)
            self.texter.text('Garage door '+door_status)
            response = SUCCESS

            return door_status


        print('Response is: ', response)

        return redirect(HOME_SERVER, code=302)

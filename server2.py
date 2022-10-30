import RPi.GPIO as GPIO

from lib.config import *
from lib.secrets import *
from flask import Flask
from lib.request_manager import Request_Manager


app = Flask(__name__)
app.debug = True

rm = Request_Manager(EMAIL, PSSWD, PHONE_NUMBER, LOG_FILENAME)


def des():
	GPIO.cleanup()


@app.route('/')
def home():
	return rm.handle_home()


@app.route('/ip/<device>/<ip>')
def ip(device, ip):
	return rm.handle_ip(device, ip)


@app.route('/garage_door_controller/<command>')
def garage_door_controller(command):
	return rm.handle_garage_door_controller(command)


@app.route('/log/<author>/<message>')
def log(author, message):
	return rm.handle_log(author, message)


if __name__ == "__main__":

	try:
		app.run(host='0.0.0.0', port=8080)
	except KeyboardInterrupt:
		des()

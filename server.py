import pickle
import requests
import smtplib
import RPi.GPIO as GPIO

from lib.config import *
from datetime import datetime
from flask import Flask, redirect, request, render_template
from lib.secrets import *


app = Flask(__name__)
app.debug = True

def text_door_status(door_status):
	msg = 'Garage door '+door_status
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(EMAIL, PSSWD)
	server.sendmail(EMAIL, PHONE_NUMBER, msg)


def set_door_status(status):
	with open('door_status.pickle', 'wb') as handle:
		pickle.dump(status, handle)


def get_door_status():
	with open('door_status.pickle', 'rb') as handle:
		door_status = pickle.load(handle)
	return door_status


def des():
	GPIO.cleanup()


@app.route('/')
def home():
	door_status = get_door_status()
	return render_template('home.html', door_status=door_status)


@app.route('/log/<_from>/<message>')
def log(_from, message):
	now = datetime.now()
	now = now.strftime("%d/%m/%Y %H:%M:%S")

	with open("log.txt", "a") as file_object:
		file_object.write(now + ' ' + _from + ' ' + message + '\n')

	return 'message added to log'


@app.route('/garage_door_controller/<command>')
def garage_door_controller(command):

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
		text_door_status(door_status)
		response = SUCCESS

		return door_status


	print('Response is: ', response)

	return redirect(HOME_SERVER, code=302)


if __name__ == "__main__":

	set_door_status(UNKNOWN)

	try:
		app.run(host='0.0.0.0', port=8080)
	except KeyboardInterrupt:
		des()

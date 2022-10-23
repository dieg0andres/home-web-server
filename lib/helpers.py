import pickle

from lib.config import DOOR_STATUS_FILENAME


def set_door_status(status):
	with open(DOOR_STATUS_FILENAME, 'wb') as handle:
		pickle.dump(status, handle)


def get_door_status():
	with open(DOOR_STATUS_FILENAME, 'rb') as handle:
		door_status = pickle.load(handle)
	return door_status

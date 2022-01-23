# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore

# Другие
import server as Server
import datetime
import json
import time

class MuteTime(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		while True:
			for user in Server.find_all("SELECT * FROM Users"):
				mute = json.loads(user[5])
				if mute['Value'] == True:
					now = datetime.datetime.now()
					now = f'{now.day - 1}:{now.hour}:{now.minute}:{now.second}'
					now_time = datetime.datetime.strptime(now, '%d:%H:%M:%S')
					mute_time = datetime.datetime.strptime(mute['Time'], '%d:%H:%M:%S')
					result_time = now_time - mute_time
					result = result_time.days * 24 + result_time.seconds / 3600
					if result >= 2.0:
						Server.edit_database(f"UPDATE Users SET mute = '{json.dumps({'Value': False, 'Time': None, 'Time Left': None})}' WHERE id = '{user[0]}'")
					else:
						Server.edit_database(f"UPDATE Users SET mute = '{json.dumps({'Value': True, 'Time': mute['Time'], 'Time Left': mute['Time Left'] - 1})}' WHERE id = '{user[0]}'")
			time.sleep(60)
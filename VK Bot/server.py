# -*- coding: utf-8 -*-

# GUI
from message_box import MessageBox

# Другие
import config as Config
import requests
import json

def find(sqlite3_command):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/find', json = {
			'SQLite3_Command': sqlite3_command,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 200:
		return server_answer_text['Result']
	else:
		message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
		message_box.signalButton.connect(lambda: message_box.close())
		message_box.show()

def find_all(sqlite3_command):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/find_all', json = {
			'SQLite3_Command': sqlite3_command,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 200:
		return server_answer_text['Result']
	else:
		message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
		message_box.signalButton.connect(lambda: message_box.close())
		message_box.show()

def edit_database(sqlite3_command, values = ()):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/edit_database', json = {
			'SQLite3_Command': sqlite3_command,
			'Unique_Key': Config.UNIQUE_KEY,
			'Values': values
		} if values != () else {
			'SQLite3_Command': sqlite3_command,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 400:
		message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
		message_box.signalButton.connect(lambda: message_box.close())
		message_box.show()
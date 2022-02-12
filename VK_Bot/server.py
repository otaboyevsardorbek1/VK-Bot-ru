# -*- coding: utf-8 -*-

# GUI
from message_box import MessageBox

# Другие
import config as Config
import requests
import json

def update_bot_settings(bot_settings):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/bot_settings/update', json = {
			'Bot_Settings': bot_settings,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	if server_answer.status_code == 400:
		server_answer_text = json.loads(server_answer.text)
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

def get_bot_settings():
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/bot_settings/get', json = {
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 200:
		return server_answer_text['Bot_Settings']
	else:
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

def update_user_commands(user_commands):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/user_commands/update', json = {
			'User_Commands': user_commands,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	if server_answer.status_code == 400:
		server_answer_text = json.loads(server_answer.text)
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

def get_user_commands():
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/user_commands/get', json = {
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 200:
		return server_answer_text['User_Commands']
	else:
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

def update_log(log):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/log/update', json = {
			'Log': log,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	if server_answer.status_code == 400:
		server_answer_text = json.loads(server_answer.text)
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

def get_log():
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/log/get', json = {
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 200:
		return server_answer_text['Log']
	else:
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

def find_in_database(sqlite3_command):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/find', json = {
			'SQLite3_Command': sqlite3_command,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 200:
		return server_answer_text['Result']
	else:
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

def find_all_in_database(sqlite3_command):
	server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/find_all', json = {
			'SQLite3_Command': sqlite3_command,
			'Unique_Key': Config.UNIQUE_KEY
		}
	)
	server_answer_text = json.loads(server_answer.text)
	if server_answer.status_code == 200:
		return server_answer_text['Result']
	else:
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')

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
	if server_answer.status_code == 400:
		server_answer_text = json.loads(server_answer.text)
		MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
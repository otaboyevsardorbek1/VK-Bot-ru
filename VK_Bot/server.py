# -*- coding: utf-8 -*-

# GUI
from message_box import MessageBox

# Другие
import config as Config
import requests
import json

# Функция для создания аккаунта на сервере
def create_new_account(login, password):
	try:
		data = {
			'Login': login,
			'Password': password
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/registration', json = data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
		else:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
			MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для авторизации аккаунта на сервере
def authorization_in_account(login, password):
	try:
		data = {
			'Login': login,
			'Password': password
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/authorization', json = data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
			Config.LOGIN = login
			Config.PASSWORD = password
			Config.UNIQUE_KEY = server_answer_text['Unique_Key']
		else:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для получения настроек бота от сервере
def get_bot_settings():
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/bot_settings/get', json = {
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Bot_Settings']
		else:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для обновления настроек бота на сервере
def update_bot_settings(bot_settings):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/bot_settings/update', json = {
				'Bot_Settings': bot_settings,
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для получения пользоватских команд от сервере
def get_user_commands():
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/user_commands/get', json = {
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['User_Commands']
		else:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для обновления пользоватских команд на сервере
def update_user_commands(user_commands):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/user_commands/update', json = {
				'User_Commands': user_commands,
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для получения логов от сервере
def get_log():
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/log/get', json = {
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Log']
		else:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для обновления логов на сервере
def update_log(log):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/log/update', json = {
				'Log': log,
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для получения одной записи из DB от сервере
def find_in_database(sqlite3_command):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/find', json = {
				'SQLite3_Command': sqlite3_command,
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Result']
		else:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для получения нескольких записей из DB от сервере
def find_all_in_database(sqlite3_command):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/find_all', json = {
				'SQLite3_Command': sqlite3_command,
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Result']
		else:
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')

# Функция для выполения SQLite3 команд на сервере
def edit_database(sqlite3_command, values = ()):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/files/database/edit_database', json = {
				'SQLite3_Command': sqlite3_command,
				'Values': values,
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			} if values != () else {
				'SQLite3_Command': sqlite3_command,
				'Login': Config.LOGIN,
				'Password': Config.PASSWORD,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text = 'Отсутствует подключение к интернету', button_2 = 'Окей')
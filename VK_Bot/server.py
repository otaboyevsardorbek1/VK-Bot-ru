# -*- coding: utf-8 -*-

# GUI
from message_box import MessageBox

# Другие
import config as Config
import global_variables as GlobalVariables
import requests
import json

# Функция для создания аккаунта на сервере
def create_new_account(login, password):
	try:
		data = {
			'Login': login,
			'Password': password
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/registration_account', json=data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
			MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для авторизации аккаунта на сервере
def authorization_in_account(login, password):
	try:
		data = {
			'Login': login,
			'Password': password
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/authorization_at_account', json=data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
			GlobalVariables.login = login
			GlobalVariables.password = password
			GlobalVariables.unique_key = server_answer_text['Unique_Key']
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для создания бота на сервере
def create_user_bot(bot_name, bot_settings):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/create_user_bot', json={
				'Bot_Name': bot_name,
				'Bot_Settings': bot_settings,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer.status_code
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения списка ботов на сервере
def get_user_bot_list():
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/get_user_bot_list', json={
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['User_Bot_List']
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для удаления бота на сервере
def delete_user_bot(bot_name):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/delete_user_bot', json={
				'Bot_Name': bot_name,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer.status_code
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения настроек бота от сервере
def get_bot_settings(bot_name):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/bot_settings/get', json={
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Bot_Settings']
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для обновления настроек бота на сервере
def update_bot_settings(bot_name, bot_settings):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/bot_settings/update', json={
				'Bot_Settings': bot_settings,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения пользоватских команд от сервере
def get_user_commands(bot_name):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/user_commands/get', json={
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['User_Commands']
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для обновления пользоватских команд на сервере
def update_user_commands(bot_name, user_commands):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/user_commands/update', json={
				'User_Commands': user_commands,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения логов от сервере
def get_log(bot_name):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/log/get', json={
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Log']
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для обновления логов на сервере
def update_log(bot_name, log):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/log/update', json={
				'Log': log,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения одной записи из DB от сервере
def find_in_database(bot_name, sqlite3_command):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/database/find', json={
				'SQLite3_Command': sqlite3_command,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Result']
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения нескольких записей из DB от сервере
def find_all_in_database(bot_name, sqlite3_command):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/database/find_all', json={
				'SQLite3_Command': sqlite3_command,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Result']
		else:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для выполения SQLite3 команд на сервере
def edit_database(bot_name, sqlite3_command, values = ()):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/database/edit_database', json={
				'SQLite3_Command': sqlite3_command,
				'Values': values,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			} if values != () else {
				'SQLite3_Command': sqlite3_command,
				'Password': GlobalVariables.password,
				'Unique_Key': GlobalVariables.unique_key
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')
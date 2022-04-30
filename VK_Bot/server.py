# -*- coding: utf-8 -*-

# GUI
from message_box import MessageBox

# Другие
import global_variables as GlobalVariables
import config as Config
import requests
import json

# Функция для подтверждения почты на сервере
def mail_confirmation(gunique_code: str):
	try:
		server_answer = requests.get(f'{Config.SERVER}/vk_bot/mail_confirmation/{gunique_code}')
		server_answer_text = json.loads(server_answer.text)
		MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для создания аккаунта на сервере
def register_account(login: str, mail: str, password_1: str, password_2: str):
	try:
		data = {
			'Login': login,
			'Mail': mail,
			'Password_1': password_1,
			'Password_2': password_2
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/register_account', json=data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code != 200:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
			MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для авторизации аккаунта на сервере
def authorize_in_account(login: str, password: str):
	try:
		data = {
			'Login': login,
			'Password': password
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/authorize_in_account', json=data)
		server_answer_text = json.loads(server_answer.text)
		MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		if server_answer.status_code == 200:
			GlobalVariables.login = login
			GlobalVariables.password = password
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для создания бота на сервере
def create_user_bot(bot_name: str, bot_settings: dict):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/create_bot', json={
				'Bot_Name': bot_name,
				'Bot_Settings': bot_settings,
				'Password': GlobalVariables.password
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code != 200:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения списка ботов на сервере
def get_user_bots_list():
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/get_bots_list', json={
				'Password': GlobalVariables.password
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
def delete_user_bot(bot_name: str):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/delete_bot', json={
				'Bot_Name': bot_name,
				'Password': GlobalVariables.password
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code != 200:
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения настроек бота от сервере
def get_bot_settings(bot_name: str):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/get_bot_settings', json={
				'Password': GlobalVariables.password
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
def update_bot_settings(bot_name: str, bot_settings: dict):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/update_bot_settings', json={
				'Bot_Settings': bot_settings,
				'Password': GlobalVariables.password
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения пользоватских команд от сервере
def get_bot_commands_list(bot_name: str):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/get_bot_commands_list', json={
				'Password': GlobalVariables.password
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
def update_bot_commands_list(bot_name: str, user_commands: list):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/update_bot_commands_list', json={
				'User_Commands': user_commands,
				'Password': GlobalVariables.password
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
		return server_answer.status_code
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения логов от сервере
def get_bot_log(bot_name: str):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/get_bot_log', json={
				'Password': GlobalVariables.password
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
def update_bot_log(bot_name: str, log: list):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/update_bot_log', json={
				'Log': log,
				'Password': GlobalVariables.password
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')

# Функция для получения одной записи из DB от сервере
def bot_database_fetchone(bot_name: str, sqlite3_command: str):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/database/fetchone', json={
				'SQLite3_Command': sqlite3_command,
				'Password': GlobalVariables.password
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
def bot_database_fetchall(bot_name: str, sqlite3_command: str):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/database/fetchall', json={
				'SQLite3_Command': sqlite3_command,
				'Password': GlobalVariables.password
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
def bot_database_edit(bot_name: str, sqlite3_command: str, values: tuple = ()):
	try:
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/{GlobalVariables.login}/{bot_name}/database/edit', json={
				'SQLite3_Command': sqlite3_command,
				'Values': values,
				'Password': GlobalVariables.password
			} if values != () else {
				'SQLite3_Command': sqlite3_command,
				'Password': GlobalVariables.password
			}
		)
		if server_answer.status_code == 400:
			server_answer_text = json.loads(server_answer.text)
			MessageBox(text=server_answer_text['Answer'], button_2='Окей')
	except requests.exceptions.ConnectionError:
		MessageBox(text='Отсутствует подключение к интернету', button_2='Окей')
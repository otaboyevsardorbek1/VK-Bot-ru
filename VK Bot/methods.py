# -*- coding: utf-8 -*-

# Другое
import json
import os

# Функция возврата настроек бота
def get_bot_settings():
	with open('Bot-Settings.json', 'r') as file:
		bot_settings = json.loads(file.read())
	return bot_settings

# Функция возврата пользоватский команд для бота
def get_user_commands():
	with open('User-Commands.json', 'r') as file:
		user_commands = json.loads(file.read())
	return user_commands

# Функция для поиска файлов
def find_file(find_name, path = None):
	file_find = False
	if path == None:
		listdir = os.listdir()
	else:
		listdir = os.listdir(path)
	for file in listdir:
		if file == find_name:
			file_find = True
	return file_find
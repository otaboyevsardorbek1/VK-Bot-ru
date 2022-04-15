# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui

# GUI
import Main_Window.User_Bot_Menu_Window.User_Command_Widnow.user_command_window as user_command_window
from db_variable_window import DBVariableWindow
from message_box import MessageBox

# Другое
import methods as Method
import server as Server
import logging

# Окно пользоватской команды
class UserCommandWindow(Method.CreateFormWindow):
	signalAddNewUserCommand = QtCore.pyqtSignal(dict)

	def __init__(self, button_text, bot_name, item=None, parent=None):
		super().__init__(parent)
		self.ui = user_command_window.Ui_Form()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug(f'{bot_name} - Окно пользоватской команды.')

		# Все нужные переменные
		self.message_for_new_user = False
		self.message_for_up_level = False
		self.show_command_in_commands_list = False
		self.button_text = button_text
		self.bot_name = bot_name
		self.item = item

		# Запуск потока
		self.widget_settings_theard = WidgetSettingsTheard(self.bot_name)
		self.widget_settings_theard.signalWidgetSettings.connect(self.widget_settings)
		self.widget_settings_theard.start()

		# Обработчики основных кнопок
		self.ui.OtherUserVariable.clicked.connect(self.other_user_variable_button)
		self.ui.DBVariableButton.clicked.connect(self.db_variable_button)
		self.ui.OtherDBVariableButton.clicked.connect(self.other_db_variable_button)
		self.ui.AllCommandsVariableButton.clicked.connect(self.all_commands_variable_button)
		self.ui.TakeUserIDVariableButton.clicked.connect(self.take_user_id_variable_button)
		self.ui.NewUserButton.clicked.connect(self.new_user_button)
		self.ui.LevelUPButton.clicked.connect(self.level_up_button)
		self.ui.ShowCommandInCommandsListButton.clicked.connect(self.show_command_in_commands_list_button)
		self.ui.UserVariableButton.clicked.connect(self.user_variable_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Логика основной кнопки
	# ==================================================================
	def user_variable_button(self):
		command_answer = self.ui.CommandAnsweTextEdit.toPlainText()
		command_answer += '{user}'
		self.ui.CommandAnsweTextEdit.setText(command_answer)

	def other_user_variable_button(self):
		command = self.ui.CommandlineEdit.text()
		if command.find('{take_user_id}') == -1:
			command += '{take_user_id}'
			self.ui.CommandlineEdit.setText(command)

		command_answer = self.ui.CommandAnsweTextEdit.toPlainText()
		command_answer += '{other_user}'
		self.ui.CommandAnsweTextEdit.setText(command_answer)

	def db_variable_button(self):
		logging.debug(f'{self.bot_name} - Переход в окно выбора значения DB.')
		self.db_variable_window = DBVariableWindow(self.bot_name, 'db')
		self.db_variable_window.signalReturnDBVariable.connect(self.db_or_other_db_variable)
		self.db_variable_window.show()

	def other_db_variable_button(self):
		logging.debug(f'{self.bot_name} - Переход в окно выбора значения DB.')
		self.db_variable_window = DBVariableWindow(self.bot_name, 'other_db')
		self.db_variable_window.signalReturnDBVariable.connect(self.db_or_other_db_variable)
		self.db_variable_window.show()

	def all_commands_variable_button(self):
		command_answer = self.ui.CommandAnsweTextEdit.toPlainText()
		command_answer += 'Список команд:\n{all_commands}'
		self.ui.CommandAnsweTextEdit.setText(command_answer)

	def take_user_id_variable_button(self):
		command = self.ui.CommandlineEdit.text()
		if command.find('{take_user_id}') == -1:
			command += '{take_user_id}'
			self.ui.CommandlineEdit.setText(command)
		else:
			MessageBox(text = '{take_user_id} можно использовать только один раз!', button_1 = 'Окей')

	def create_new_or_edit_user_command_button(self):
		command_name = self.ui.CommandNameLineEdit.text()
		command = self.ui.CommandlineEdit.text()
		command_answer = self.ui.CommandAnsweTextEdit.toPlainText()

		find_command_name = False
		find_command = False

		for user_command in self.user_commands:
			if self.button_text == 'Редактировать команду':
				if self.user_commands[self.user_command_value]['Command_Name'] == user_command['Command_Name']:
					continue
				elif self.user_commands[self.user_command_value]['Command'] == user_command['Command']:
					continue

			if user_command['Command_Name'] == command_name:
				find_command_name = True
				break
			elif user_command['Command'] == command:
				find_command = True
				break

		if find_command_name == False and find_command == False:
			data = {
				'Command_Name': command_name,
				'Command': command,
				'Flags': {
					'Message_For_New_User': self.message_for_new_user,
					'Message_For_Up_Level': self.message_for_up_level,
					'Show_Command_In_Commands_List': self.show_command_in_commands_list
				},
				'Command_Answer': command_answer
			}
			if self.button_text == 'Создать команду':
				self.user_commands.append(data)
				Server.update_user_commands(self.bot_name, self.user_commands)

				self.signalAddNewUserCommand.emit(data)
				logging.debug(f'{self.bot_name} - Успешное создания команды {command_name}.')
				MessageBox(text = 'Вы успешно создали команду.', button_1 = 'Окей')

				self.close()
			elif self.button_text == 'Редактировать команду':
				self.user_commands[self.user_command_value] = data
				Server.update_user_commands(self.bot_name, self.user_commands)

				self.item.setText(command_name)
				logging.debug(f'{self.bot_name} - Успешное изменения команды.')
				MessageBox(text = 'Вы успешно изменили команду.', button_1 = 'Окей')

				self.close()
		else:
			if find_command_name == True and find_command == True:
				text = f'Команда "{command}" и команда с именем "{command_name}" уже существует!'
			elif find_command_name == True:
				text = f'Команда с именем "{command_name}" уже существует!' 
			elif find_command == True:
				text = f'Команда "{command}" уже существует!'

			MessageBox(text = text, button_1 = 'Щас исправлю...')

	def new_user_button(self):
		Method.on_or_off_func(self.message_for_new_user, self.ui.NewUserButton)
		self.message_for_new_user = True

	def level_up_button(self):
		Method.on_or_off_func(self.message_for_up_level, self.ui.LevelUPButton)
		self.message_for_up_level = True

	def show_command_in_commands_list_button(self):
		Method.on_or_off_func(self.show_command_in_commands_list, self.ui.ShowCommandInCommandsListButton)
		self.show_command_in_commands_list = True
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def widget_settings(self, user_commands: list):
		self.user_commands = user_commands
		if self.button_text == 'Создать команду':
			self.ui.UserCommandButton.setText(self.button_text)
			self.ui.UserCommandButton.clicked.connect(self.create_new_or_edit_user_command_button)
		if self.button_text == 'Редактировать команду':
			self.user_command_value = 0
			for user_command in self.user_commands:
				if user_command['Command_Name'] == self.item.text():
					break
				self.user_command_value += 1

			self.ui.CommandNameLineEdit.setText(self.user_commands[self.user_command_value]['Command_Name'])
			self.ui.CommandlineEdit.setText(self.user_commands[self.user_command_value]['Command'])
			self.ui.CommandAnsweTextEdit.setText(self.user_commands[self.user_command_value]['Command_Answer'])

			if self.user_commands[self.user_command_value]['Flags']['Message_For_New_User'] == True:
				self.message_for_new_user = True
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("../Icons/iconOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.ui.NewUserButton.setIcon(icon)
			if self.user_commands[self.user_command_value]['Flags']['Message_For_Up_Level'] == True:
				self.message_for_up_level = True
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("../Icons/iconOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.ui.LevelUPButton.setIcon(icon)
			if self.user_commands[self.user_command_value]['Flags']['Show_Command_In_Commands_List'] == True:
				self.show_command_in_commands_list = True
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("../Icons/iconOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.ui.ShowCommandInCommandsListButton.setIcon(icon)

			self.ui.UserCommandButton.setText(self.button_text)
			self.ui.UserCommandButton.clicked.connect(self.create_new_or_edit_user_command_button)

	def db_or_other_db_variable(self, text: str):
		command = self.ui.CommandAnsweTextEdit.toPlainText() + text
		self.ui.CommandAnsweTextEdit.setText(command)

		if text.find('other_db') != -1:
			command = self.ui.CommandlineEdit.text()
			if command.find('{take_user_id}') == -1:
				command += '{take_user_id}'
				self.ui.CommandlineEdit.setText(command)
	# ==================================================================

# Поток для настрйоки виджетов
class WidgetSettingsTheard(QtCore.QThread):
	signalWidgetSettings = QtCore.pyqtSignal(list)

	def __init__(self, bot_name):
		QtCore.QThread.__init__(self)

		self.bot_name = bot_name

	def run(self):
		user_commands = Server.get_user_commands(self.bot_name)
		self.signalWidgetSettings.emit(user_commands)
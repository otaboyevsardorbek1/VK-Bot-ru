# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtWidgets

# GUI
import Main_Window.User_Command_Widnow.user_command_window as user_command_window
from db_variable_window import DBVariableWindow
from message_box import MessageBox

# Другое
import server as Server

# Окно для пользоватских команд
class UserCommandWindow(QtWidgets.QMainWindow):
	signalAddNewUserCommand = QtCore.pyqtSignal(dict)

	def __init__(self, button_text, item = None, parent = None):
		super().__init__(parent, QtCore.Qt.Window)
		self.ui = user_command_window.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Все нужные переменные
		self.button_text = button_text
		self.item = item

		# Запуск потоков
		self.widget_settings_theard = WidgetSettingsTheard()
		self.widget_settings_theard.signalWidgetSettings.connect(self.widget_settings)
		self.widget_settings_theard.start()

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Перетаскивание безрамочного окна
	# ==================================================================
	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		try:
			delta = QtCore.QPoint(event.globalPos() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPos()
		except AttributeError:
			pass
	# ==================================================================

	# Логика основной кнопки
	# ==================================================================
	def create_new_or_edit_user_command_button(self):
		command_name = self.ui.CommandNameLineEdit.text()
		command = self.ui.CommandlineEdit.text()
		command_answer = self.ui.CommandAnsweTextEdit.toPlainText()

		find_command_name = False
		find_command = False

		if self.button_text == 'Создать команду':
			for user_command in self.user_commands:
				if user_command['Command_Name'] == command_name:
					find_command_name = True
					break
				elif user_command['Command'] == command:
					find_command = True
					break
		elif self.button_text == 'Редактировать команду':
			for user_command in self.user_commands:
				if user_command['Command_Name'] == command_name and self.user_commands[self.user_command_value]['Command_Name'] != user_command['Command_Name']:
					find_command_name = True
					break
				elif user_command['Command'] == command and self.user_commands[self.user_command_value]['Command'] != user_command['Command']:
					find_command = True
					break

		if find_command_name == False and find_command == False:
			if self.button_text == 'Создать команду':
				data = {
					'Command_Name': command_name,
					'Command': command,
					'Command_Answer': command_answer
				}
				self.user_commands.append(data)
				Server.update_user_commands(self.user_commands)

				self.signalAddNewUserCommand.emit(data)
				MessageBox(text = 'Вы успешно создали команду.', button_1 = 'Окей')

				self.close()
			elif self.button_text == 'Редактировать команду':
				self.user_commands[self.user_command_value] = {
					'Command_Name': command_name,
					'Command': command,
					'Command_Answer': command_answer
				}
				Server.update_user_commands(self.user_commands)

				self.item.setText(command_name)
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
		self.db_variable_window = DBVariableWindow('db')
		self.db_variable_window.signalReturnDBVariable.connect(self.db_or_other_db_variable)
		self.db_variable_window.show()

	def other_db_variable_button(self):
		self.db_variable_window = DBVariableWindow('other_db')
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
	# ==================================================================

	# Обычные функции
	# ==================================================================
	def widget_settings(self, user_commands):
		# Настройка виджетов
		self.user_commands = user_commands

		if self.button_text == 'Создать команду':
			self.ui.UserCommandButton.setText(self.button_text)
			self.ui.UserCommandButton.clicked.connect(self.create_new_or_edit_user_command_button)
		if self.button_text == 'Редактировать команду':
			old_user_command = self.item.text().replace('Команда: ', '').strip()

			self.user_command_value = 0
			for user_command in self.user_commands:
				if user_command['Command_Name'] == old_user_command:
					break
				self.user_command_value += 1

			self.ui.CommandNameLineEdit.setText(self.user_commands[self.user_command_value]['Command_Name'])
			self.ui.CommandlineEdit.setText(self.user_commands[self.user_command_value]['Command'])
			self.ui.CommandAnsweTextEdit.setText(self.user_commands[self.user_command_value]['Command_Answer'])

			self.ui.UserCommandButton.setText(self.button_text)
			self.ui.UserCommandButton.clicked.connect(self.create_new_or_edit_user_command_button)

		# Обработчики основных кнопок
		self.ui.UserVariableButton.clicked.connect(self.user_variable_button)
		self.ui.OtherUserVariable.clicked.connect(self.other_user_variable_button)
		self.ui.DBVariableButton.clicked.connect(self.db_variable_button)
		self.ui.OtherDBVariableButton.clicked.connect(self.other_db_variable_button)
		self.ui.AllCommandsVariableButton.clicked.connect(self.all_commands_variable_button)
		self.ui.TakeUserIDVariableButton.clicked.connect(self.take_user_id_variable_button)
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def db_or_other_db_variable(self, text):
		command = self.ui.CommandAnsweTextEdit.toPlainText()
		command += text
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

	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		user_commands = Server.get_user_commands()
		self.signalWidgetSettings.emit(user_commands)
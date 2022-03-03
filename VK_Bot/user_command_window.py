# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtWidgets

# GUI
import Main_Window.Settings_Window.User_Command_Widnow.user_command_window as user_commandl_window
from message_box import MessageBox

# Другое
import server as Server

class UserCommandWindow(QtWidgets.QMainWindow):
	signalAddNewUserCommand = QtCore.pyqtSignal(dict)

	def __init__(self, button_text, item = None, parent = None):
		super().__init__(parent, QtCore.Qt.Window)
		self.ui = user_commandl_window.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		self.user_commands = Server.get_user_commands()
		self.button_text = button_text

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Обработчик основной кнопки
		if self.button_text == 'Создать команду':
			self.ui.UserCommandButton.setText(self.button_text)
			self.ui.UserCommandButton.clicked.connect(self.create_new_or_edit_user_command_button)
		if self.button_text == 'Редактировать команду':
			self.item = item

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

				self.item.setText(f'Команда: {command_name}')
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
	# ==================================================================
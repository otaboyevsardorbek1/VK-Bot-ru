# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Bot_Panel.Settings_Panel.settings_panel as settings_panel
from user_command_panel import UserCommandPanel
from message_box import MessageBox

# Другое
from methods import *
import json

# Окно настроек бота
class SettingsPanel(QtWidgets.QMainWindow):
	def __init__(self, login, password, parent = None):
		super().__init__(parent, QtCore.Qt.Window)
		self.ui = settings_panel.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		self.login = login
		self.password = password

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		self.automati_authorizaton_button_status = False
		self.automati_save_log_button_status = False
		self.user_commands_button_status = False

		self.bot_settings = get_bot_settings()
		self.ui.VKTokenLineEdit.setText(self.bot_settings['VK_Token'])
		self.ui.IDBotLineEdit.setText(self.bot_settings['Group_ID'])
		if self.bot_settings['User_Commands'] == True:
			self.user_commands_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.UserCommandsButton.setIcon(icon)
		if self.bot_settings['Automati_Authorizaton'] == True:
			self.automati_authorizaton_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiAuthorizatonButton.setIcon(icon)
		if self.bot_settings['Automati_Save_Log'] == True:
			self.automati_save_log_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiSaveLogButton.setIcon(icon)

		user_commands = get_user_commands()
		for user_command in user_commands:
			item = QtWidgets.QListWidgetItem()
			item.setTextAlignment(QtCore.Qt.AlignLeft)
			item.setText(f"Команда: {user_command['Command_Name']}")
			self.ui.UserCommandsListWidget.addItem(item)

		# Обработчики основных кнопок
		self.ui.AutomatiAuthorizatonButton.clicked.connect(self.automati_authorizaton)
		self.ui.AutomatiSaveLogButton.clicked.connect(self.automati_save_log)
		self.ui.UserCommandsButton.clicked.connect(self.user_commands)
		self.ui.AddUserCommandButton.clicked.connect(self.add_new_user_command_panel)
		self.ui.EditUserCommandButton.clicked.connect(self.edit_user_command_panel)
		self.ui.DeleteUserCommandButton.clicked.connect(self.remove_user_command)
		self.ui.ShowVKTokenButton.clicked.connect(self.show_vk_token)
		self.ui.SaveBotSettingsButton.clicked.connect(self.save_bot_settings)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window)
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

	# Логика основных кнопок
	# ==================================================================
	def automati_authorizaton(self):
		if self.automati_authorizaton_button_status == True:
			self.automati_authorizaton_button_status = False
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/Off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiAuthorizatonButton.setIcon(icon)
		else:
			self.automati_authorizaton_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiAuthorizatonButton.setIcon(icon)

	def automati_save_log(self):
		if self.automati_save_log_button_status == True:
			self.automati_save_log_button_status = False
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/Off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiSaveLogButton.setIcon(icon)
		else:
			self.automati_save_log_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiSaveLogButton.setIcon(icon)

	def user_commands(self):
		if self.user_commands_button_status == True:
			self.user_commands_button_status = False
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/Off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.UserCommandsButton.setIcon(icon)
		else:
			self.user_commands_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.UserCommandsButton.setIcon(icon)

	def add_new_user_command_panel(self):
		add_user_command_panel = UserCommandPanel(button_text = 'Создать команду')
		add_user_command_panel.signalAddNewUserCommand.connect(self.add_new_user_command)
		add_user_command_panel.show()

	def edit_user_command_panel(self):
		item = self.ui.UserCommandsListWidget.selectedItems()
		if len(item) == 0:
			message_box = MessageBox(text = 'Вы не выбрали команду, которую хотите изменить!', button_1 = 'Щас исправлю...')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()
		elif len(item) == 1:
			item = item[0]
			edit_user_command_panel = UserCommandPanel(button_text = 'Редактировать команду', item = item)
			edit_user_command_panel.show()

	def remove_user_command(self):
		item = self.ui.UserCommandsListWidget.selectedItems()
		if len(item) == 0:
			message_box = MessageBox(text = 'Вы не выбрали команду, которую хотите удалить!', button_1 = 'Щас исправлю...')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()
		elif len(item) == 1:
			item = item[0]

			old_user_command = item.text().replace('Команда: ', '').strip()
			user_commands = get_user_commands()
	
			user_command_value = 0
			for user_command in user_commands:
				if user_command['Command_Name'] == old_user_command: 
					break
				user_command_value += 1
			del user_commands[user_command_value]

			with open('User-Commands.json', 'wb') as file:
				file.write(json.dumps(user_commands, ensure_ascii = False, indent = 2).encode('UTF-8'))

			self.ui.UserCommandsListWidget.takeItem(self.ui.UserCommandsListWidget.row(item))

			message_box = MessageBox(text = 'Вы успешно удалили пользоватскую команду.', button_1 = 'Окей')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()

	def signalButton(self, button):
		if button == 'Да':
			self.save_bot_settings()
		self.message_box.close()

	def close_window(self):
		different_settings = False
		if self.bot_settings['Automati_Authorizaton'] != self.automati_authorizaton_button_status:
			different_settings = True
		elif self.bot_settings['User_Commands'] != self.user_commands_button_status:
			different_settings = True
		elif self.bot_settings['VK_Token'] != self.ui.VKTokenLineEdit.text():
			different_settings = True
		elif self.bot_settings['Group_ID'] != self.ui.IDBotLineEdit.text():
			different_settings = True

		if different_settings == True:
			self.message_box = MessageBox(text = 'Вы изменили настройки, хотите их сохранить?', button_1 = 'Да', button_2 = 'нет')
			self.message_box.signalButton.connect(self.signalButton)
			self.message_box.show()

		self.close()

	def show_vk_token(self):
		if self.ui.VKTokenLineEdit.echoMode() == 2:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowVKTokenButton.setIcon(icon)
			self.ui.VKTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
		else:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowVKTokenButton.setIcon(icon)
			self.ui.VKTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def save_bot_settings(self):
		with open('Bot-Settings.json', 'wb') as file:
			self.bot_settings = {
				'Automati_Authorizaton': self.automati_authorizaton_button_status,
				'Automati_Save_Log': self.automati_save_log_button_status,
				'User_Commands': self.user_commands_button_status,
				'VK_Token': self.ui.VKTokenLineEdit.text(),
				'Group_ID': self.ui.IDBotLineEdit.text()
			}
			if self.automati_authorizaton_button_status == True:
				self.bot_settings.update(
					{
						'Login': self.login,
						'Password': self.password
					}
				)
			file.write(json.dumps(self.bot_settings, ensure_ascii = False, indent = 2).encode('UTF-8'))

		message_box = MessageBox(text = 'Успешное сохранение настроек бота', button_2 = 'Окей')
		message_box.signalButton.connect(lambda: message_box.close())
		message_box.show()
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def add_new_user_command(self, new_command):
		item = QtWidgets.QListWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignLeft)
		item.setText(new_command['Command_Name'])
		self.ui.UserCommandsListWidget.addItem(item)
    # ==================================================================
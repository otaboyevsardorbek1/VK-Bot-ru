# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore

# GUI
import Main_Window.Add_New_User_Bot_Window.add_new_user_bot_window as add_new_user_bot_window
from message_box import MessageBox

# Другое
import methods as Method
import server as Server
import logging

# Окно добавления бота
class AddNewUserBotWindow(Method.CreateFormWindow):
	signalReturnNewUserBot = QtCore.pyqtSignal(str)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = add_new_user_bot_window.Ui_Form()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Окно добавления бота.')

		# Настройка основной кнопки
		self.ui.AddNewUserBotButton.setText('Добавить бота')

		# Обработчики основных кнопок
		self.ui.ShowVKTokenButton.clicked.connect(lambda: Method.show_or_hide_text(self.ui.VKTokenLineEdit, self.ui.ShowVKTokenButton))
		self.ui.AddNewUserBotButton.clicked.connect(self.add_new_user_bot_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Логика основных кнопок
	# ==================================================================
	def close_window_button(self):
		def create_new_user_bot_button_signal(self, message_box, text):
			message_box.close()
			if text == 'Да':
				self.create_new_user_bot_button()
			else:
				logging.debug('Выход из окна добавления бота.')
				self.close()

		message_box = MessageBox(text='Вы не создали бота, хотите его создать?', button_1='Да', button_2='Нет')
		message_box.message_box.signalButton.connect(lambda text: create_new_user_bot_button_signal(self, message_box.message_box, text))

	def add_new_user_bot_button(self):
		bot_name = self.ui.UserBotNameLineEdit.text()
		server_answer_status_code = Server.create_user_bot(bot_name, {
				'Automati_Save_Log': False,
				'VK_Token': self.ui.VKTokenLineEdit.text(),
				'Group_ID': self.ui.IDBotLineEdit.text()
			}
		)
		if server_answer_status_code == 200:
			logging.debug(f'Успешное добавления бота {bot_name}.')
			self.signalReturnNewUserBot.emit(bot_name)
			self.close()
	# ==================================================================
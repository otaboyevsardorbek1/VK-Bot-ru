# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Main_Window.Add_New_User_Bot_Window.add_new_user_bot_window as add_new_user_bot_window
from message_box import MessageBox

# Другое
import server as Server
import logging

# Окно добавления бота
class AddNewUserBotWindow(QtWidgets.QMainWindow):
	signalReturnNewUserBot = QtCore.pyqtSignal(str)

	def __init__(self, parent=None):
		super().__init__(parent, QtCore.Qt.Window)
		self.ui = add_new_user_bot_window.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		# Запись в логи программы
		logging.debug('Окно добавления бота.')

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Настройка основной кнопки
		self.ui.AddNewUserBotButton.setText('Добавить бота')

		# Обработчики основных кнопок
		self.ui.ShowVKTokenButton.clicked.connect(self.show_vk_token_button)
		self.ui.AddNewUserBotButton.clicked.connect(self.create_new_user_bot_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
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

	def show_vk_token_button(self):
		icon = QtGui.QIcon()
		if self.ui.VKTokenLineEdit.echoMode() == 2:
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowVKTokenButton.setIcon(icon)
			self.ui.VKTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
		else:
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowVKTokenButton.setIcon(icon)
			self.ui.VKTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def create_new_user_bot_button(self):
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
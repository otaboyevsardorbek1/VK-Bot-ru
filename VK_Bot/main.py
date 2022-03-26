# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Registration_Window.registration_window as registration_window
import Authorization_Window.authorization_window as authorization_window
from main_window import MainWindow

# Другое
import server as Server
import logging
import sys
import os

# Глобальная функция
# ==================================================================
def show_password(self):
	icon = QtGui.QIcon()
	if self.ui.PasswordLineEdit.echoMode() == 2:
		icon.addPixmap(QtGui.QPixmap("../Icons/eyeOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.ShowPasswordButton.setIcon(icon)
		self.ui.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
	else:
		icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.ShowPasswordButton.setIcon(icon)
		self.ui.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
# ==================================================================

# Графический интерфейс программы
# ==================================================================
class RegistrationWindow(QtWidgets.QMainWindow): # Окно регистрации
	def __init__(self, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = registration_window.Ui_MainWindow()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Окно регистрации.')

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Обработчики основных кнопок
		self.ui.ShowPasswordButton.clicked.connect(lambda: show_password(self))
		self.ui.CreateAccountButton.clicked.connect(self.create_new_account)
		self.ui.LoginLineEdit.returnPressed.connect(self.create_new_account)
		self.ui.PasswordLineEdit.returnPressed.connect(self.create_new_account)
		self.ui.AskButton.clicked.connect(self.authorization_window_button)

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
		logging.debug('Выход из окна регистрации.')
		self.close()

	def create_new_account(self):
		login = self.ui.LoginLineEdit.text()
		password = self.ui.PasswordLineEdit.text()

		server_answer_status_code = Server.create_new_account(login, password)
		if server_answer_status_code == 200:
			logging.debug('Успешное создания нового аккаунта.')
			logging.debug('Переход в окно авторизации.')
			self.auth = AuthorizationWindow()
			self.auth.show()
			self.close()

	def authorization_window_button(self):
		logging.debug('Переход в окно авторизации.')
		self.authorization_window = AuthorizationWindow()
		self.authorization_window.show()
		self.close()

class AuthorizationWindow(QtWidgets.QMainWindow): # Окно авторизации
	def __init__(self, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = authorization_window.Ui_MainWindow()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Окно авторизации.')

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Обработчики основных кнопок
		self.ui.ShowPasswordButton.clicked.connect(lambda: show_password(self))
		self.ui.AuthorizationButton.clicked.connect(self.authorization_in_account)
		self.ui.LoginLineEdit.returnPressed.connect(self.authorization_in_account)
		self.ui.PasswordLineEdit.returnPressed.connect(self.authorization_in_account)
		self.ui.AskButton.clicked.connect(self.registration_window_button)

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
		logging.debug('Выход из окна авторизации.')
		self.close()

	def authorization_in_account(self):
		login = self.ui.LoginLineEdit.text()
		password = self.ui.PasswordLineEdit.text()

		server_answer_status_code = Server.authorization_in_account(login, password)
		if server_answer_status_code == 200:
			logging.debug('Успешная авторизация в аккаунт.')
			logging.debug('Переход в главное окно.')
			self.main_window = MainWindow()
			self.main_window.show()
			self.close()

	def registration_window_button(self):
		logging.debug('Переход в окно регистрации.')
		self.registration_window = RegistrationWindow()
		self.registration_window.show()
		self.close()
# ==================================================================

if __name__ == '__main__':
	# Настройка библиотеки "logging"
	try:
		os.mkdir('Log')
	except FileExistsError:
		pass
	logging.basicConfig(filename='Log/app.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

	# Запуск GUI
	app = QtWidgets.QApplication(sys.argv)
	myapp = AuthorizationWindow()
	myapp.show()
	sys.exit(app.exec_())
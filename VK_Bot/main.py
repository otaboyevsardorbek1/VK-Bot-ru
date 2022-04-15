# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtWidgets

# GUI
import Registration_Window.registration_window as registration_window
import Authorization_Window.authorization_window as authorization_window
from main_window import MainWindow

# Другое
import methods as Method
import server as Server
import logging
import sys
import os

# Графический интерфейс программы
# ==================================================================
class RegistrationWindow(Method.CreateMainWindow): # Окно регистрации
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = registration_window.Ui_MainWindow()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Окно регистрации.')

		# Обработчики основных кнопок
		widgets = [self.ui.LoginLineEdit, self.ui.PasswordLineEdit_1, self.ui.ShowPasswordButton_1, self.ui.PasswordLineEdit_2, self.ui.ShowPasswordButton_2]
		for widget in widgets:
			if widget in [self.ui.LoginLineEdit, self.ui.PasswordLineEdit_1, self.ui.PasswordLineEdit_2]:
				widget.returnPressed.connect(self.create_new_account)
			elif widget  == self.ui.ShowPasswordButton_1:
				widget.clicked.connect(lambda: Method.show_or_hide_text(self.ui.PasswordLineEdit_1, self.ui.ShowPasswordButton_1))
			elif widget == self.ui.ShowPasswordButton_2:
				widget.clicked.connect(lambda: Method.show_or_hide_text(self.ui.PasswordLineEdit_2, self.ui.ShowPasswordButton_2))
		self.ui.CreateAccountButton.clicked.connect(self.create_new_account)
		self.ui.AskButton.clicked.connect(self.authorization_window_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Логика основных кнопок
	# ==================================================================
	def close_window_button(self):
		logging.debug('Выход из окна регистрации.')
		self.close()

	def create_new_account(self):
		login = self.ui.LoginLineEdit.text()
		password_1 = self.ui.PasswordLineEdit_1.text()
		password_2 = self.ui.PasswordLineEdit_2.text()

		server_answer_status_code = Server.create_new_account(login, password_1, password_2)
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

class AuthorizationWindow(Method.CreateMainWindow): # Окно авторизации
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = authorization_window.Ui_MainWindow()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Окно авторизации.')

		# Обработчики основных кнопок
		self.ui.LoginLineEdit.returnPressed.connect(self.authorization_in_account)
		self.ui.PasswordLineEdit.returnPressed.connect(self.authorization_in_account)
		self.ui.ShowPasswordButton.clicked.connect(lambda: Method.show_or_hide_text(self.ui.PasswordLineEdit, self.ui.ShowPasswordButton))
		self.ui.AuthorizationButton.clicked.connect(self.authorization_in_account)
		self.ui.AskButton.clicked.connect(self.registration_window_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

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
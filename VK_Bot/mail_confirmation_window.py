# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore

# GUI
import Mail_Confirmation_Window.mail_confirmation_window as mail_confirmation_window

# Другое
import methods as Method
import server as Server
import logging

# Окно подтверждения почты
class MailConfirmationWindow(Method.CreateFormWindow):
	signalMailConfirmed = QtCore.pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = mail_confirmation_window.Ui_Form()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Окно подтверждения почты.')

		# Обработчики основных кнопок
		self.ui.MailConfirmationButton.clicked.connect(self.mail_confirmation_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Логика основных кнопок
	# ==================================================================
	def close_window_button(self):
		logging.debug('Выход из окна подтверждения почты.')
		self.close()

	def mail_confirmation_button(self):
		gunique_code = self.ui.QuniqueCodeLineEdit.text()
		server_answer_status_code = Server.mail_confirmation(gunique_code)
		if server_answer_status_code == 200:
			logging.debug('Успешное подтверждение почты.')
			self.signalMailConfirmed.emit()
			self.close()
	# ==================================================================
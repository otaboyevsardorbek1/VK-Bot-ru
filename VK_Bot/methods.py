# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# Функция для показа/скрывания текста в LineEdit
def show_or_hide_text(lineEdit: QtWidgets.QLineEdit, eyeButton: QtWidgets.QPushButton):
	icon = QtGui.QIcon()
	if lineEdit.echoMode() == 2:
		icon.addPixmap(QtGui.QPixmap("../Icons/eyeOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		eyeButton.setIcon(icon)
		lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
	else:
		icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		eyeButton.setIcon(icon)
		lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

# Функция для включения/выключения определённой функции
def on_or_off_func(button_value: bool, funcButton: QtWidgets.QPushButton):
	icon = QtGui.QIcon()
	if button_value == True:
		icon.addPixmap(QtGui.QPixmap("../Icons/iconOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		funcButton.setIcon(icon)
		button_value = False
	else:
		icon.addPixmap(QtGui.QPixmap("../Icons/iconOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		funcButton.setIcon(icon)
		button_value = True
	return button_value

# Класс для создания основы для MainWindow
class CreateMainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

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

# Класс для создания основы для FormWindow
class CreateFormWindow(QtWidgets.QMainWindow):
	def __init__(self, parent):
		super().__init__(parent, QtCore.Qt.Window)
		self.setWindowModality(2)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

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
# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Message_Box.message_box as message_box

# Другое
import methods as Method

# Всплывающее окно
class MyMessageBox(Method.CreateFormWindow):
	signalButton = QtCore.pyqtSignal(str)

	def __init__(self, text, button_1, button_2, font_size, parent=None):
		super().__init__(parent)
		_translate = QtCore.QCoreApplication.translate
		self.ui = message_box.Ui_Form()
		self.ui.setupUi(self)

		self.ui.Label.setText(text)

		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		style = """
QPushButton{
	color: white;
	border-radius: 8px;
	background-color: #595F76;
}

QPushButton:hover{
	background-color: #50566E;
}

QPushButton:pressed{
	background-color: #434965;
}
"""
		if button_1 != '' and button_2 != '':
			self.Button_1 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_1.setGeometry(QtCore.QRect(20, 70, 171, 41))
			self.Button_1.setFont(font)
			self.Button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_1.setStyleSheet(style)

			self.Button_2 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_2.setGeometry(QtCore.QRect(210, 70, 171, 41))
			self.Button_2.setFont(font)
			self.Button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_2.setStyleSheet(style)

			self.Button_1.setText(_translate('Form', button_1))
			self.Button_2.setText(_translate('Form', button_2))

			self.Button_1.clicked.connect(lambda: self.signalButton.emit(button_1))
			self.Button_2.clicked.connect(lambda: self.signalButton.emit(button_2))
		elif button_1 != '':
			self.Button_1 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_1.setGeometry(QtCore.QRect(120, 70, 161, 41))
			self.Button_1.setFont(font)
			self.Button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_1.setStyleSheet(style)
			self.Button_1.setText(_translate('Form', button_1))
			self.Button_1.clicked.connect(lambda: self.signalButton.emit(button_1))
		elif button_2 != '':
			self.Button_2 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_2.setGeometry(QtCore.QRect(120, 70, 161, 41))
			self.Button_2.setFont(font)
			self.Button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_2.setStyleSheet(style)
			self.Button_2.setText(_translate('Form', button_2))
			self.Button_2.clicked.connect(lambda: self.signalButton.emit(button_2))

		font.setPointSize(font_size)
		self.ui.Label.setFont(font)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

class MessageBox:
	def __init__(self, text='', button_1='', button_2='', font_size=11):
		self.message_box = MyMessageBox(text, button_1, button_2, font_size)
		self.message_box.signalButton.connect(lambda: self.message_box.close())
		self.message_box.show()
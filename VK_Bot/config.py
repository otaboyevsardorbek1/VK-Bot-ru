# -*- coding: utf-8 -*-

SERVER = 'http://exg1o.pythonanywhere.com' # Глобальный сервер
# SERVER = 'http://127.0.0.1:5000/' # Локальный сервер

# Для отслеживание версии программы
VERSION = 'v1.0.9'

# Стили для кнопки вкл. и выкл. бота
ON_BUTTON = """\
	QPushButton{
		border-radius: 8px;
		background-color: #EA4100;
	}

	QPushButton:hover{
		background-color: #DF3E00;
	}

	QPushButton:pressed{
		background-color: #CA3700;
	}
"""

OFF_BUTTON = """\
	QPushButton{
		border-radius: 8px;
		background-color: #92E604;
	}

	QPushButton:hover{
		background-color: #8BDC03;
	}

	QPushButton:pressed{
		background-color: #7DC802;
	}
"""

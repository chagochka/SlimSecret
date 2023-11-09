import sqlite3
import sys

from PyQt5.QtWidgets import QApplication

from main_form import MainForm
from registration_form import RegistrationForm

con = sqlite3.connect('database.db')
cur = con.cursor()

user_flag = cur.execute('''SELECT EXISTS(SELECT * FROM User WHERE name LIKE '%')''').fetchone()
con.close()


def except_hook(cls, exception, traceback):
	"""Функция для отслеживания ошибок PyQt5"""
	sys.excepthook(cls, exception, traceback)


def main(form):
	"""
 	Открытие нужной формы
 	:return:
 	"""
	app = QApplication(sys.argv)
	ex = form()
	ex.show()
	sys.excepthook = except_hook
	sys.exit(app.exec())


if __name__ == '__main__':
	if user_flag[0]:
		main(MainForm)
	else:
		main(RegistrationForm)

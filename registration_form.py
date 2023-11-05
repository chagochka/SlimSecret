import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from calculate_ccal import calculate_calories
from main_form import MainForm


class RegistrationForm(QMainWindow):
	"""
	Класс для создания формы регистрации.
	"""

	def __init__(self):
		"""
		Инициализирует форму регистрации.
		"""
		super().__init__()
		uic.loadUi('designs/registr.ui', self)
		self.setWindowTitle('Регистрация')

		self.Button.clicked.connect(self.registration)

	def registration(self):
		"""
		Обработка данных формы и добавление пользователя в базу данных.
        После коммита изменений и закрытия соединения с базой данных, метод закрывает форму регистрации
        и открывает MainForm.
		:return:
		"""
		params = [self.weight.value(), self.height.value(), self.age.value(), self.male.currentText(),
		          self.activity.currentText(), self.target.currentText()]

		if calculate_calories(*params)[1] < 18.5:
			QMessageBox.warning(self, "Предупреждение",
			                    '''Ваш индекс массы тела ниже нормы, если введёные данные верны, \
								то вам следует обратиться к врачу''')

		params.append(calculate_calories(*params)[0])
		params.insert(0, self.name.text())
		params.insert(0, 1)

		con = sqlite3.connect('database.db')
		cur = con.cursor()

		cur.execute(f'''INSERT INTO User VALUES {tuple(params)}''')

		con.commit()
		con.close()

		self.close()

		self.main_form = MainForm()
		self.main_form.show()

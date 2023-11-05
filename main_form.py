import calendar
import datetime as dt
import locale
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.Qt import QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QCalendarWidget, QVBoxLayout, QWidget, QLineEdit, QDoubleSpinBox, \
	QSpinBox, QComboBox, QMessageBox
from googletrans import Translator

from calculate_ccal import calculate_calories

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

con = sqlite3.connect('database.db')
cur = con.cursor()

translator = Translator()


class UserDialog(QDialog):
	def __init__(self, user_data):
		super(UserDialog, self).__init__()
		uic.loadUi('designs/user_dialog.ui', self)
		self.setWindowTitle(user_data['name'])

		self.user_data = user_data

		self.name.setText(user_data['name'])
		self.age.setValue(user_data['age'])
		self.weight.setValue(user_data['weight'])
		self.height.setValue(user_data['height'])
		self.sex.setCurrentText(user_data['sex'])
		self.activity.setCurrentText(user_data['activity'])
		self.target.setCurrentText(user_data['target'])
		self.kcal.setValue(user_data['kcal'])

		self.OKButton.clicked.connect(self.Ok)
		self.QuitButton.clicked.connect(self.remove_user)
		self.ChangeButton.clicked.connect(self.save_changes)
		self.FileButton.clicked.connect(self.save_file)

		for widget in self.groupBox.findChildren(QWidget):
			if isinstance(widget, QLineEdit):
				widget.editingFinished.connect(self.change_data)
			elif isinstance(widget, QDoubleSpinBox) or isinstance(widget, QSpinBox):
				widget.valueChanged.connect(self.change_data)
			elif isinstance(widget, QComboBox):
				widget.currentIndexChanged.connect(self.change_data)

	def Ok(self):
		self.close()

	def remove_user(self):
		cur.execute('''DELETE FROM User''')
		cur.execute('''DELETE FROM Dates''')
		cur.execute('''DELETE FROM Used_food''')

		con.commit()
		sys.exit()

	def change_data(self):
		if self.sender().objectName() in self.user_data:
			if isinstance(self.sender(), QComboBox):
				self.user_data[self.sender().objectName()] = self.sender().currentText()
			elif isinstance(self.sender(), QDoubleSpinBox) or isinstance(self.sender(), QSpinBox):
				self.user_data[self.sender().objectName()] = self.sender().value()
			else:
				self.user_data[self.sender().objectName()] = self.sender().text()

	def save_changes(self):
		slc = list(self.user_data.values())[2:-1]
		if calculate_calories(*slc)[1] < 18.5:
			QMessageBox.warning(self, "Предупреждение",
			                    '''Ваш индекс массы тела ниже нормы, если введёные данные верны, \
			                    то вам следует обратиться к врачу''')

		self.user_data['kcal'] = calculate_calories(*slc)[0]
		for i in self.user_data:
			cur.execute(f'''UPDATE User SET 
							{i} = "{self.user_data[i]}"''')

		con.commit()
		self.close()

	def save_file(self):
		f = open(f"данные_{self.user_data['name']}.txt", 'w', encoding='UTF-8')
		f.write('\n'.join([f'{i}: {self.user_data[i]}' for i in self.user_data]))
		f.close()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return:
			pass


class AddKcalDialog(QDialog):
	def __init__(self, date_id, meal):
		super(AddKcalDialog, self).__init__()
		uic.loadUi('designs/add_kcal_dialog.ui', self)
		self.setWindowTitle('Добавить продукт')

		self.series = QPieSeries()
		self.series.setHorizontalPosition(0.5)
		self.series.setPieSize(0.6)

		chart = QChart()
		chart.legend().setAlignment(Qt.AlignLeft)
		chart.addSeries(self.series)

		chart.setAnimationOptions(QChart.SeriesAnimations)
		chart.setTheme(QChart.ChartThemeDark)

		chartview = QChartView(chart)
		chartview.setRenderHint(QPainter.Antialiasing)
		self.graph_layout.addWidget(chartview)

		self.series.hovered.connect(self.handle_hovered)
		self.searchButton.clicked.connect(self.search_product)
		self.search_line.editingFinished.connect(self.search_product)
		self.weight.valueChanged.connect(self.calc_kcal)
		self.OKButton.clicked.connect(self.Ok)
		self.QuitButton.clicked.connect(self.close)
		self.productList.itemClicked.connect(self.select_product)

		self.date_id = date_id
		self.meal = meal

	def Ok(self):
		if self.product_name.text():
			cur.execute(f'''INSERT INTO Used_food (name, kcal, date_id, meal)
			                VALUES {(self.product_name.text(), self.total_kcal.value(), self.date_id, self.meal)}''')
			con.commit()

		self.close()

	# Функция для перевода текста
	def translate_text(self, text, dest_lang):
		result = translator.translate(text, dest=dest_lang)
		return result.text

	def search_product(self):
		self.productList.clear()

		if self.search_line.text():
			product = self.translate_text(self.search_line.text(), 'en')

			products = cur.execute(f'''SELECT Descrip FROM Food
                                        WHERE Descrip LIKE "%{product}%"''').fetchmany(50)

			translated_products = ''
			for i in products:
				translated_products += i[0] + '\n'

			if translated_products:
				translated_products = self.translate_text(translated_products, 'ru').split('\n')

				for i in range(len(translated_products)):
					self.productList.addItem(f'{translated_products[i]}\t{products[i][0]}')

	def select_product(self, item):
		self.series.clear()

		product_name, en_product = item.text().split('\t')

		data_product = cur.execute(f"""SELECT Energy_kcal, Fat_g, Carb_g, Protein_g, Sugar_g   FROM Food
                                        WHERE Descrip = ?""", (en_product,)).fetchone()

		self.product_name.setText(product_name)
		self.kcal.setValue(float(data_product[0]))
		self.calc_kcal()

		self.series.append(f'Белки {data_product[3]}г', float(data_product[3]))
		self.series.append(f'Жиры {data_product[1]}г', float(data_product[1]))
		self.series.append(f'Углеводы {data_product[2]}г', float(data_product[2]))
		self.series.append(f'Сахар {data_product[4]}г', float(data_product[4]))

	def calc_kcal(self):
		self.total_kcal.setValue((self.kcal.value() / 100) * self.weight.value())

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return:
			pass

	def handle_hovered(self, slice, state):
		if state:
			slice.setExploded(True)
			slice.setLabelVisible(True)
		else:
			slice.setExploded(False)
			slice.setLabelVisible(False)


class CalendarDialog(QDialog):
	def __init__(self):
		super(CalendarDialog, self).__init__()
		self.setWindowTitle('Выбор даты')

		self.calendar = QCalendarWidget(self)
		self.calendar.setGridVisible(True)
		self.calendar.clicked.connect(self.get_date)

		layout = QVBoxLayout()
		layout.addWidget(self.calendar)

		self.setLayout(layout)

	def get_date(self):
		self.close()
		return self.calendar.selectedDate().toString("yyyy-MM-dd")


class MainForm(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('designs/main_design.ui', self)
		self.setWindowTitle('SlimSecret')

		self.current_date = str(dt.datetime.now()).split()[0]

		# заполняем нужные словари
		self.user_data = {}
		self.kcal_dict = {self.DinnerButton: 'dinner_kcal',
		                  self.BreakfastButton: 'breakfast_kcal',
		                  self.SupperButton: 'supper_kcal',
		                  self.OtherButton: 'other_kcal'}
		self.meal_dict = {self.add_kcal_buttons.buttons()[0]: 'breakfast',
		                  self.add_kcal_buttons.buttons()[1]: 'dinner',
		                  self.add_kcal_buttons.buttons()[2]: 'supper',
		                  self.add_kcal_buttons.buttons()[3]: 'other'}
		self.del_dict = {self.delete_buttons.buttons()[0]: self.breakfest_list,
		                 self.delete_buttons.buttons()[2]: self.dinner_list,
		                 self.delete_buttons.buttons()[1]: self.supper_list,
		                 self.delete_buttons.buttons()[3]: self.other_list}

		# привязываем функции к кнопкам
		self.ProfileButton.clicked.connect(self.get_user_info)
		self.calendarButton.clicked.connect(self.open_calendar_dialog)

		for button in self.add_kcal_buttons.buttons():
			button.clicked.connect(self.add_kcal)

		for button in self.delete_buttons.buttons():
			button.clicked.connect(self.del_kcal)

		self.update_values()

	def update_values(self):
		self.breakfest_list.clear()
		self.dinner_list.clear()
		self.supper_list.clear()
		self.other_list.clear()

		data = cur.execute('''SELECT * FROM User''').fetchone()
		columns = cur.execute('''PRAGMA table_info("User")''').fetchall()

		for i in range(len(columns)):
			self.user_data[columns[i][1]] = data[i]

		self.user_name.setText(self.user_data['name'])
		self.rsk_kcal.setText(str(self.user_data['kcal']))

		date = self.current_date

		if not cur.execute('''SELECT EXISTS(SELECT * FROM Dates WHERE date = ?)''', (date,)).fetchone()[0]:
			cur.execute('''INSERT INTO Dates (date) VALUES (?)''', (date,))
			con.commit()

		self.date_data = cur.execute('''SELECT * FROM Dates WHERE date = ?''',
		                             (date,)).fetchone()

		date = dt.datetime.strptime(self.current_date, '%Y-%m-%d')
		self.date.setText(f'{calendar.month_name[date.month]}, {date.day}')

		breakfest = cur.execute(f'''SELECT * FROM Used_food 
									WHERE date_id = {self.date_data[0]} 
									AND meal = "breakfast"''').fetchall()
		dinner = cur.execute(f'''SELECT * FROM Used_food 
									WHERE date_id = {self.date_data[0]} 
									AND meal = "dinner"''').fetchall()
		supper = cur.execute(f'''SELECT * FROM Used_food 
									WHERE date_id = {self.date_data[0]} 
									AND meal = "supper"''').fetchall()
		other = cur.execute(f'''SELECT * FROM Used_food 
									WHERE date_id = {self.date_data[0]} 
									AND meal = "other"''').fetchall()

		self.breakfast_kcal.setText(str(round(sum(map(lambda p: p[2], breakfest)), 1)))
		for i in breakfest:
			self.breakfest_list.addItem(f'{i[0]}. {i[1]}\t{i[2]}')

		self.dinner_kcal.setText(str(round(sum(map(lambda p: p[2], dinner)), 1)))
		for i in dinner:
			self.dinner_list.addItem(f'{i[0]}. {i[1]}\t{i[2]}')

		self.supper_kcal.setText(str(round(sum(map(lambda p: p[2], supper)), 1)))
		for i in supper:
			self.supper_list.addItem(f'{i[0]}. {i[1]}\t{i[2]}')

		self.other_kcal.setText(str(round(sum(map(lambda p: p[2], other)), 1)))
		for i in other:
			self.other_list.addItem(f'{i[0]}. {i[1]}\t{i[2]}')

		self.total_kcal.setText(str(sum(map(float, [self.breakfast_kcal.text(), self.dinner_kcal.text(),
		                                            self.supper_kcal.text(), self.other_kcal.text()]))))

		left_kcal = self.user_data['kcal'] - float(self.total_kcal.text())
		if left_kcal > 0:
			self.left_kcal.setText(str(left_kcal))
		else:
			self.left_kcal.setText('0')

	def add_kcal(self):
		dialog = AddKcalDialog(self.date_data[0], self.meal_dict[self.sender()])
		dialog.exec_()

		self.update_values()

	def del_kcal(self):
		lst = self.del_dict[self.sender()]
		row = lst.currentRow()
		if row >= 0:
			item = lst.takeItem(row).text()

			cur.execute(f'''DELETE FROM Used_food
							WHERE id = {item[:item.find(".") + 1]}''')
			con.commit()

			self.update_values()

	def get_user_info(self):
		dialog = UserDialog(self.user_data)
		dialog.exec_()

		self.update_values()

	def open_calendar_dialog(self):
		dialog = CalendarDialog()
		dialog.exec_()

		self.current_date = dialog.get_date()
		self.update_values()

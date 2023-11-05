def calculate_calories(weight, height, age, gender, activity_level, coef):
	"""
    Рассчитывает общее количество калорий, необходимых в день, и индекс массы тела (ИМТ) для человека.

	:param float weight: Вес человека в килограммах.
	:param int height: Рост человека в сантиметрах.
	:param int age: Возраст человека в годах.
	:param str gender: Пол человека. Принимает "мужской" для мужчин и "женский" для женщин.
	:param str activity_level: Уровень физической активности человека. Принимает следующие варианты:
        - "Малая активность (мало или нет спорта)"
        - "Невысокая активность (спорт 1-3 дня в неделю)"
        - "Умеренная активность (спорт 3-5 дней в неделю)"
        - "Высокая активность (спорт 6-7 дней в неделю)"
        - "Очень высокая активность (тяжёлые физические упражнения)"
	:param str coef: Цель человека. Принимает "похудение" для похудения и "набор массы" для набора веса.
	:return: ортеж, содержащий общее количество калорий в день (округленное до ближайшего целого числа) и ИМТ (округленный до ближайшего целого числа).
	"""
	# Словарь коэффициентов активности
	activity_coefficients = {
		"Малая активность (мало или нет спорта)": 1.2,
		"Невысокая активность (спорт 1-3 дня в неделю)": 1.375,
		"Умеренная активность (спорт 3-5 дней в неделю)": 1.55,
		"Высокая активность (спорт 6-7 дней в неделю)": 1.725,
		"Очень высокая активность (тяжёлые физические упражнения)": 1.9
	}

	target_coefficients = {
		'похудение': 0.85,
		'набор массы': 1.15
	}

	# Вычисление BMR
	if gender == "мужской":
		bmr = 10 * weight + 6.25 * height - 5 * age + 5
	elif gender == "женский":
		bmr = 10 * weight + 6.25 * height - 5 * age - 161

	# Вычисление общего количества калорий
	total_calories = bmr * activity_coefficients.get(activity_level, 0) * target_coefficients.get(coef, 1)

	# Вычисление индекса массы тела (BMI)
	bmi = weight / ((height / 100) ** 2)

	return round(total_calories), round(bmi)

from datetime import datetime, timedelta

numb_SBU = 1  # Кол-во СБУ.
numb_PDM = 2  # Кол-во ПДМ.
numb_extraction = 4  # Кол-во выработок.
start_time = datetime(2022, 6, 1, 0, 0, 0)  # Задаём временную точку начала работ.
end_time = datetime(2022, 6, 20, 0, 0, 0)  # Задаём временную точку окончания работ.


class Extraction:  # Класс выработки .
	# Рабочие данные.
	rock_mass_density = 3.4  # Плотность горной массы. (тонны/м3)
	sectional_area_mine = 20  # Площадь сечения выработки. (м2)
	max_working_length = 200  # Максимальная длина выработки. (М)
	charging_time = 60  # Заряжание. (Мин)
	separation_explosion = 3.2  # Отрыв после взрыва. (М)

	# Счётчики процесса.
	numb_of_exp = 0  # Количество взрывов.
	working_length = 0.0  # Метры проходки.
	drilling = 0  # Процесс бурения.
	charge = 0  # Процесс заряда.

	def __init__(self, meters_worked, rock_mass):
		self.meters_worked = meters_worked  # Отработано метров на момент запуска скрипта.
		self.rock_mass = rock_mass  # Кол-во неубранной горной породы на момент запуска скрипта.


class SBU:  # Класс СБУ.
	useful_time = 0  # Полезное время работы.
	in_work = False  # Состояние техники.

	def __init__(self, working_time):
		self.working_time = working_time  # Рабочее время. (Мин)


class PDM(SBU):  # Класс ПДМ.
	bucket_capacity = 7  # Вместимость ковша. (Тонн)
	mass_mined_ore = 0.0  # Масса добытой руды.
	number_flights = 0  # Кол-во рейсов.


def show_stats():  # Функция вывода статистики.
	print(f'Начало периода работы: {start_time}')
	print(f'Окончание периода работы: {end_time}')
	print(f'Количество взрывов в каждой выработке: {[ext_id.numb_of_exp for ext_id in extraction_list]}')
	print(f'Общее количество взрывов: {sum([ext_id.numb_of_exp for ext_id in extraction_list])}')
	print(f'Метры проходки по каждой выработке: {[f"{ext_id.working_length:.2f}" for ext_id in extraction_list]}')
	print(f'Общие метры проходки: {sum([ext_id.working_length for ext_id in extraction_list]):.2f}')
	print(
		f'Полезное время работы: СБУ - {sum([sbu_id.useful_time for sbu_id in SBU_list])} мин., '
		f'ПДМ - {sum([pdm_id.useful_time for pdm_id in PDM_list])} мин.')
	print(f'Масса добытой руды: {sum([pdm_id.mass_mined_ore for pdm_id in PDM_list]):.2f} тонн.')
	print(f'Количество рейсов по каждой ПДМ: {[pdm_id.number_flights for pdm_id in PDM_list]}')


extraction_list = [Extraction(0, 0) for _ in range(numb_extraction)]  # Иницилизируем объекты выработок.
SBU_list = [SBU(150) for _ in range(numb_SBU)]  # Иницилизируем объекты техники.
PDM_list = [PDM(10) for _ in range(numb_PDM)]  # Иницилизируем объекты техники.

current_time = start_time
while True:
	# Если текущее время достигло конечной точки.
	if current_time > end_time:
		show_stats()  # Выводим статистику.
		break  # Останавливаем рабочий процесс.
	# Если сейчас время перерыва пропускаем рабочий процесс.
	elif current_time.hour in (0, 8, 16) or (current_time.hour in (7, 15, 23) and current_time.minute != 0):
		current_time += timedelta(minutes=110)  # Добавляем 110 минут к рабочему процессу.
		continue
	for pdm_id in PDM_list:  # Проходим по списку ПДМ.
		if not pdm_id.in_work: continue  # Если техника не в работе, переходим к следующей.
		ext_id = pdm_id.in_work
		if ext_id.rock_mass <= pdm_id.bucket_capacity:  # Если остатки горной массы меньше или ровно вместимости ковша ПДМ.
			pdm_id.mass_mined_ore += ext_id.rock_mass  # Добавляем остатки горной массы к числу добытой руды.
			ext_id.rock_mass = 0  # Обнуляем наличие горной массы в выработке.
			pdm_id.in_work = False  # Снимаем технику с выработки.
		else:  # Если остатки горной массы больше вместимости ковша ПДМ.
			ext_id.rock_mass -= pdm_id.bucket_capacity  # Отнимаем наличие горной массы в выработке ровно на вместимость ковша ПДМ.
			pdm_id.mass_mined_ore += pdm_id.bucket_capacity  # Добавляем ковш горной массы к числу добытой руды.
		pdm_id.useful_time += 10  # Добавляем полезное время работы ПДМ.
		pdm_id.number_flights += 1  # Добавляем рейс ПДМ.

	for sbu_id in SBU_list:  # Проходим по списку СБУ.
		if not sbu_id.in_work: continue  # Если техника не в работе, переходим к следующей.
		ext_id = sbu_id.in_work
		ext_id.drilling += 10  # Добавляем время бурения выарботке.
		sbu_id.useful_time += 10  # Добавляем полезное время работы СБУ.
		if ext_id.drilling == sbu_id.working_time:  # Если время бурения в выработке достигло требуемого.
			sbu_id.in_work = False  # Снимаем технику с выработки.
			ext_id.drilling = 'Redy'  # Выставляем статус бурения Redy.

	for ext_id in extraction_list:  # Проходим по всем выработкам.
		# Если выработка достигла максимальной глубины и горная порода вывезена - переходим к следующей выработке.
		if ext_id.meters_worked + ext_id.working_length >= ext_id.max_working_length and not ext_id.rock_mass:
			continue
		elif ext_id.rock_mass:  # Если присутствует не убранная горная порода.
			for pdm_id in PDM_list:  # Проходим имеющиеся ПДМ.
				if pdm_id.in_work: continue  # Если техника уже занята - переходим к следующей.
				pdm_id.in_work = ext_id  # Присваеваем технике ИД выработки.
				break  # Выходим из цикла.
		elif not ext_id.drilling:  # Если бурение не производится.
			for sbu_id in SBU_list:  # Проходим имеющиеся СБУ.
				if sbu_id.in_work: continue  # Если техника уже занята - переходим к следующей.
				sbu_id.in_work = ext_id  # Присваеваем технике ИД выработки.
				break  # Выходим из цикла.
		elif ext_id.drilling == 'Redy' and not ext_id.charge:  # Если бурение прошло, а заряд не заложен.
			# Проверяем текущее время, если за час до окночания смены - начинаем заряд.
			ext_id.charge = 1  # Приступаем к процессу заряда.
		elif ext_id.charge:  # Процесс заряда начался.
			if ext_id.charge >= ext_id.charging_time:  # Если заряд заложен.
				if current_time.hour in (7, 15, 23):  # И смена подошла к концу.
					# Производим взрыв!
					ext_id.charge = 0  # Обнуляем заряд.
					ext_id.drilling = 0  # Обнуляем бурение.
					ext_id.numb_of_exp += 1  # Увеличиваем кол-во взрывов.
					ext_id.working_length += ext_id.separation_explosion  # Увеличиваем метры проходки на "Отрыв после взрыва".
					# Задаём кол-во неубранной горной породы после взрыва.
					ext_id.rock_mass = ext_id.sectional_area_mine * ext_id.separation_explosion * ext_id.rock_mass_density
			else:  # Если процесс заряда не окончен.
				ext_id.charge += 10  # Продолжаем процесс заряда.
	current_time += timedelta(minutes=10)  # Добавляем 10 минут к рабочему процессу.

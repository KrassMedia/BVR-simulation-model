# Имитационная модель БВР

Добыча руды ведётся в 4-х выработках. Площадь сечения выработки 20м2, плотность горной
массы – 3,4 тонны/м3, длина выработок 200 метров. Работы производятся круглосуточно,
посменно: 3 смены с межсменными перерывами в 2 часа (23:00 – 1:00, 7:00 – 9:00, 15:00 – 17:00).

Технология добычи циклическая с применением взрывчатых веществ (ВВ). Цикл таков: бурение
шпуров под ВВ (самоходная буровая установка - СБУ) – заряжание – взрыв – откатка оторванной
горной массы (погрузочно – доставочная машина - ПДМ). Взрыв производится в конце смены
(заряжание за 1 час до окончания смены).

### Данные по производительности:
- СБУ выполняет работу за 2,5 часа (шпуры бурит на глубину 3,4м, отрыв после взрыва –
3,2м);
- вместимость ковша ПДМ – 7 тонн;
- длительность одного рейса ПДМ – 10 минут;
- заряжание – 1 час.

### Задача:
Необходимо разработать имитационную модель, которая за произвольный период времени на
основе данных о производительности и количестве задействованной техники, а также начальных
условий (фазы цикла) каждой выработки – на момент времени 0, вычисляет:

- количество взрывов в каждой выработке, общее количество взрывов;
- метры проходки по каждой выработке, общие метры проходки;
- время работы СБУ и ПДМ;
- массу добытой руды, количество рейсов по каждой ПДМ.

Количество СБУ – 1 ед., количество ПДМ – переменное (от 1 до 2-х)

Алгоритм должен быть реализован на Python.

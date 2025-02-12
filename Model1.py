import random
import queue

# Константы
t1 = 10  # Интервал прихода пользователей (мин)
t2 = 25  # Время обработки задач на ЭВМ (мин)
t3 = 30  # Время печати результата (мин)
delta = 0.3  # Доля пользователей, которые будут печатать
N = 4  # Общее количество ЭВМ
M = 2  # Общее количество принтеров
sim_time = 7 * 24 * 60  # Общее время симуляции (неделя в минутах)
cpu_index_2 = 0
cpu_index_try = 0
printer_index_try = 0
printer_index_2 = 0
# Структуры данных для очередей
cpu_queue = queue.Queue()  # Очередь пользователей, ожидающих свободную ЭВМ
printer_queue = queue.Queue()  # Очередь пользователей, ожидающих свободный принтер

# Параметры
total_users = 0
busy_cpus = 0  # Количество занятых ЭВМ
busy_printers = 0  # Количество занятых принтеров
cpu_release_times = [0] * N  # Время освобождения ЭВМ
printer_release_times = [0] * M  # Время освобождения принтера

# Массивы для хранения метрик
cpu_usage = []  # Записываем загрузку ЭВМ
printer_usage = []  # Записываем загрузку принтеров
cpu_queue_length = []  # Записываем длину очереди пользователей на ЭВМ
printer_queue_length = []  # Записываем длину очереди пользователей на принтере

# Основной цикл моделирования
for current_time in range(0, sim_time, 1): # Шаг моделирования - 1 минута
    # Проверка освобождения ЭВМ
    for i in range(N):
        if busy_cpus > 0 and current_time >= cpu_release_times[i] and cpu_release_times[i] != 0 :
            busy_cpus -= 1  # Освобождаем ЭВМ
            cpu_index_2 = i
            cpu_release_times[i] = 0
            cpu_index_try += 1
            # Проверяем, есть ли пользователи в очереди на ЭВМ
            if not cpu_queue.empty():
                cpu_queue.get()  # Обслуживаем следующего пользователя
                busy_cpus += 1  # Обслуживаем нового пользователя
                cpu_release_times[busy_cpus - 1] = current_time + t2  # Запланируем время освобождения ЭВМ

    # Проверка освобождения принтера
    for j in range(M):
        if busy_printers > 0 and current_time >= printer_release_times[j] and printer_release_times[j] != 0:
            busy_printers -= 1  # Освобождаем принтер
            printer_index_2 = j
            printer_release_times[j] = 0
            printer_index_try += 1
            # Проверяем, есть ли пользователи в очереди на принтер
            if not printer_queue.empty():
                printer_queue.get()  # Обслуживаем следующего пользователя
                busy_printers += 1  # Обслуживаем нового пользователя
                printer_release_times[busy_printers - 1] = current_time + t3  # Запланируем время освобождения принтера

    # Приход пользователя
    if current_time % t1 == 0:  # Каждые t1 минут
        total_users += 1  # Увеличиваем общее количество пользователей
        # Проверяем наличие свободных ЭВМ
        if busy_cpus < N:
            busy_cpus += 1  # Увеличиваем счетчик занятых ЭВМ
            cpu_index = busy_cpus - 1  # Индекс занятой ЭВМ

            if cpu_index_try != 0 :
                cpu_index = cpu_index_2
                cpu_index_try = 0

            cpu_release_times[cpu_index] = current_time + t2  # Запланируем время освобождения ЭВМ
            # Определяем, хочет ли пользователь распечатать результат
            if random.random() < delta:
                # Проверяем наличие свободных принтеров
                if busy_printers < M:
                    busy_printers += 1
                    printer_index = busy_printers - 1
                    if printer_index_try != 0:
                        printer_index = printer_index_2
                        printer_index_try = 0
                    printer_release_times[printer_index] = current_time + t2 + t3  # Время освобождения принтера
                else:
                    # Принтер занят, добавляем в очередь
                    printer_queue.put(current_time + t2 + t3)
        else:
            # Добавляем пользователя в очередь на ЭВМ
            cpu_queue.put(current_time)

    # Обновление метрик

    cpu_usage.append(busy_cpus / N)  # Коэффициент загрузки ЭВМ
    printer_usage.append(busy_printers / M)  # Коэффициент загрузки принтеров
    cpu_queue_length.append(cpu_queue.qsize())  # Длина очереди на ЭВМ
    printer_queue_length.append(printer_queue.qsize())  # Длина очереди на принтер

    # Протоколирование текущего состояния системы
    print(f"Время: {current_time} мин - Пользователи: {total_users}, "
          f"Занятых ЭВМ: {busy_cpus}, Занятых принтеров: {busy_printers}, "
          f"Очередь на ЭВМ: {cpu_queue.qsize()}, Очередь на принтер: {printer_queue.qsize()}")

    # Результаты моделирования
average_cpu_queue_length = sum(cpu_queue_length) / len(cpu_queue_length) if cpu_queue_length else 0
average_printer_queue_length = sum(printer_queue_length) / len(printer_queue_length) if printer_queue_length else 0

print(f"\nСредняя загрузка ЭВМ: {sum(cpu_usage) / len(cpu_usage):.2f}")
print(f"Средняя загрузка принтеров: {sum(printer_usage) / len(printer_usage):.2f}")
print(f"Средняя длина очереди на ЭВМ: {average_cpu_queue_length:.2f}")
print(f"Средняя длина очереди на принтер: {average_printer_queue_length:.2f}")


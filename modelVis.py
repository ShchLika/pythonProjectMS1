import tkinter as tk
from tkinter import scrolledtext
import random
import queue
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.text as mtext

# Константы
t1 = 10  # Интервал прихода пользователей (мин)
t2 = 25  # Время обработки задач на ЭВМ (мин)
t3 = 30  # Время печати результата (мин)
delta = 0.3  # Доля пользователей, которые будут печатать
N = 4  # Общее количество ЭВМ
M = 2  # Общее количество принтеров
sim_time = 7 * 24 * 60  # Общее время симуляции (неделя в минутах)
cpu_index_try = 0
printer_index_try = 0
total_users = 0
# Структуры данных
cpu_queue = queue.Queue()  # Очередь пользователей, ожидающих свободную ЭВМ
printer_queue = queue.Queue()  # Очередь пользователей, ожидающих свободный принтер
busy_cpus = 0  # Количество занятых ЭВМ
busy_printers = 0  # Количество занятых принтеров
cpu_release_times = [0] * N  # Время освобождения ЭВМ
printer_release_times = [0] * M  # Время освобождения принтера

# Для анимации
fig, ax = plt.subplots(figsize=(10, 5))
frames = []  # Данные для каждого кадра анимации
animation_speed = 1  # Скорость анимации (мс)

# Основной цикл моделирования
for current_time in range(0, sim_time, 1):
    frame_data = {}

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
    if current_time % t1 == 0:
        if current_time % t1 == 0:  # Каждые t1 минут
            total_users += 1  # Увеличиваем общее количество пользователей
            # Проверяем наличие свободных ЭВМ
            if busy_cpus < N:
                busy_cpus += 1  # Увеличиваем счетчик занятых ЭВМ
                cpu_index = busy_cpus - 1  # Индекс занятой ЭВМ

                if cpu_index_try != 0:
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

    # Сохранение состояния для анимации
    frame_data['current_time'] = current_time
    frame_data['busy_cpus'] = busy_cpus
    frame_data['busy_printers'] = busy_printers
    frame_data['cpu_queue_length'] = cpu_queue.qsize()
    frame_data['printer_queue_length'] = printer_queue.qsize()
    frame_data['total_users'] = total_users  # Добавляем текущее количество пользователей
    frames.append(frame_data)

# Создание основного окна
window = tk.Tk()
window.title("Симуляция системы")

# Создание области для анимации
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=window)  # Привязка matplotlib canvas к tkinter
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Прокручиваемое текстовое поле для вывода логов
log_text_widget = scrolledtext.ScrolledText(window, height=10, width=100, font=('Arial', 10), wrap=tk.WORD)
log_text_widget.pack(side=tk.BOTTOM, fill=tk.BOTH)
# Поддерживаемая строка для вывода на "мини-консоль"
log_text = []

# Функция для отрисовки каждого кадра
def update(frame):
    ax.clear()
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 3)

    # ЭВМ
    for i in range(N):
        color = 'red' if i < frame['busy_cpus'] else 'green'
        rect = patches.Rectangle((i, 1), 0.8, 0.5, color=color)
        ax.add_patch(rect)

    # Принтеры
    for j in range(M):
        color = 'red' if j < frame['busy_printers'] else 'blue'
        rect = patches.Rectangle((j, 0), 0.8, 0.5, color=color)
        ax.add_patch(rect)

    # Очереди
    for q in range(frame['cpu_queue_length']):
        ax.plot(-0.5, 1 + q * 0.15, 'o', color='black')  # Очередь на ЭВМ

    for q in range(frame['printer_queue_length']):
        ax.plot(-0.5, 0 + q * 0.15, 'o', color='black')  # Очередь на принтер

    ax.set_title(f"Моделирование работы системы в момент времени: {frame['current_time']} мин")
    ax.set_xticks([])
    ax.set_yticks([])

    # Заголовок
    ax.set_title(f"Моделирование работы системы в момент времени: {frame['current_time']} мин")

    # Форматирование строки состояния
    status_line = (f"Время: {frame['current_time']} мин - "
                   f"Пользователи: {frame['total_users']}, "  # Используем total_users из frame
                   f"Занятых ЭВМ: {frame['busy_cpus']}, "
                   f"Занятых принтеров: {frame['busy_printers']}, "
                   f"Очередь на ЭВМ: {frame['cpu_queue_length']}, "
                   f"Очередь на принтер: {frame['printer_queue_length']}")

    # Добавление строки в текстовое поле
    log_text.append(status_line)
    log_text_widget.configure(state='normal')  # Разрешаем редактирование
    log_text_widget.insert(tk.END, status_line + "\n")  # Вставляем строку
    log_text_widget.configure(state='disabled')  # Запрещаем редактирование, чтобы избежать ошибок
    log_text_widget.yview(tk.END)  # Прокручиваем текстовое поле вниз

    # Обновляем график
    canvas.draw()

def update_animation_speed(val):
    global animation_speed
    animation_speed = max(1, float(val))  # Убедимся, что скорость не меньше 1 мс

# Добавляем ползунок для регулировки скорости анимации
scale = tk.Scale(window, from_=0, to=500, resolution=1, orient=tk.HORIZONTAL,
                 label="Скорость анимации (мс)", command=update_animation_speed)
scale.set(animation_speed)  # Установим начальное значение
scale.pack(side=tk.BOTTOM, fill=tk.X)

# Создание анимации
ani = FuncAnimation(fig, update, frames=frames, interval=animation_speed, repeat=False)

# Запуск окна
window.mainloop()
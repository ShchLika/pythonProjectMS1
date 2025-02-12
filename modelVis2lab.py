import queue
import random
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import scrolledtext

# Константы
lmbda = 1 / 10  # Средний интервал времени прихода пользователей (10 минут)
#t2 = 25  # Время обработки задач на ЭВМ (мин)
#t3 = 30  # Время печати результата (мин)
delta = 0.3  # Доля пользователей, которые будут печатать
N = 4  # Общее количество ЭВМ
M = 2  # Общее количество принтеров
sim_time = 7 * 24 * 60  # Общее время симуляции (неделя в минутах)

# Функция для генерации экспоненциального распределения
def exponential(lmbda):
    x = random.random()
    return int((-1 / lmbda) * math.log(x))  # Преобразуем в целое число

# Функция для генерации нормального распределения
def normal(sigma, m):
    x = random.random()
    x2 = random.random()
    return int(sigma * math.cos(2 * math.pi * x) * math.sqrt(-2 * math.log(x2)) + m)  # Преобразуем в целое число

# Структуры данных
cpu_queue = queue.Queue()  # Очередь пользователей, ожидающих свободную ЭВМ
printer_queue = queue.Queue()  # Очередь пользователей, ожидающих свободный принтер
busy_cpus = 0  # Количество занятых ЭВМ
busy_printers = 0  # Количество занятых принтеров
cpu_release_times = [0] * N  # Время освобождения ЭВМ
printer_release_times = [0] * M  # Время освобождения принтера
total_users = 0  # Общее количество пользователей

# Для анимации
frames = []  # Данные для каждого кадра анимации
animation_speed = 1  # Скорость анимации (мс)

# Основной цикл моделирования
current_time = 0
next_arrival_time = exponential(lmbda)  # Первое событие прихода пользователя

while current_time < sim_time:
    frame_data = {}

    # Проверка освобождения ЭВМ
    for i in range(N):
        if busy_cpus > 0 and current_time >= cpu_release_times[i] and cpu_release_times[i] != 0:
            busy_cpus -= 1  # Освобождаем ЭВМ
            cpu_release_times[i] = 0

            if not cpu_queue.empty():
                cpu_queue.get()
                busy_cpus += 1
                t2 = normal(5, 25)  # Генерация времени обработки на ЭВМ
                cpu_release_times[i] = current_time + t2

    # Проверка освобождения принтера
    for j in range(M):
        if busy_printers > 0 and current_time >= printer_release_times[j] and printer_release_times[j] != 0:
            busy_printers -= 1  # Освобождаем принтер
            printer_release_times[j] = 0

            # Проверяем, есть ли пользователи в очереди на принтер
            if not printer_queue.empty():
                printer_queue.get()
                busy_printers += 1
                t3 = normal(5, 30)  # Генерация времени печати результата
                printer_release_times[j] = current_time + t3

    # Приход пользователя
    if current_time >= next_arrival_time:
        total_users += 1
        next_arrival_time += exponential(lmbda)

        if busy_cpus < N:
            busy_cpus += 1
            # Поиск индекса первой свободной ЭВМ
            cpu_index = cpu_release_times.index(0)

            t2 = normal(5, 25)  # Генерация времени обработки на ЭВМ
            cpu_release_times[cpu_index] = current_time + t2

            if random.random() < delta:
                if busy_printers < M:
                    busy_printers += 1
                    printer_index = printer_release_times.index(0)

                    t3 = normal(5, 30)  # Генерация времени печати результата
                    printer_release_times[printer_index] = current_time + t2 + t3
                else:
                    printer_queue.put(current_time)
        else:
            cpu_queue.put(current_time)

    frame_data['current_time'] = current_time
    frame_data['busy_cpus'] = busy_cpus
    frame_data['busy_printers'] = busy_printers
    frame_data['cpu_queue_length'] = cpu_queue.qsize()
    frame_data['printer_queue_length'] = printer_queue.qsize()
    frame_data['total_users'] = total_users
    frames.append(frame_data)

    current_time += 1

# Создание основного окна
window = tk.Tk()
window.title("Симуляция системы")

# Создание области для анимации
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

log_text_widget = scrolledtext.ScrolledText(window, height=10, width=100, font=('Arial', 10), wrap=tk.WORD)
log_text_widget.pack(side=tk.BOTTOM, fill=tk.BOTH)
log_text = []

ani = None

def update(frame):
    ax.clear()
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 3)

    for i in range(N):
        color = 'red' if i < frame['busy_cpus'] else 'green'
        rect = patches.Rectangle((i, 1), 0.8, 0.5, color=color)
        ax.add_patch(rect)

    for j in range(M):
        color = 'red' if j < frame['busy_printers'] else 'blue'
        rect = patches.Rectangle((j, 0), 0.8, 0.5, color=color)
        ax.add_patch(rect)

    for q in range(frame['cpu_queue_length']):
        ax.plot(-0.5, 1 + q * 0.15, 'o', color='black')

    for q in range(frame['printer_queue_length']):
        ax.plot(-0.5, 0 + q * 0.15, 'o', color='black')

    ax.set_title(f"Время: {frame['current_time']} мин")

    status_line = (f"Время: {frame['current_time']} мин - "
                   f"Пользователи: {frame['total_users']}, "
                   f"ЭВМ: {frame['busy_cpus']}, "
                   f"Принтеры: {frame['busy_printers']}, "
                   f"Очередь ЭВМ: {frame['cpu_queue_length']}, "
                   f"Очередь принтеров: {frame['printer_queue_length']}")

    log_text.append(status_line)
    log_text_widget.configure(state='normal')
    log_text_widget.insert(tk.END, status_line + "\n")
    log_text_widget.configure(state='disabled')
    log_text_widget.yview(tk.END)
    canvas.draw()

def update_animation_speed(val):
    global ani, animation_speed
    animation_speed = max(1, float(val))
    if ani:
        ani.event_source.stop()
    ani = FuncAnimation(fig, update, frames=frames, interval=animation_speed, repeat=False)
    canvas.draw()

scale = tk.Scale(window, from_=1, to=500, resolution=1, orient=tk.HORIZONTAL,
                 label="Скорость анимации (мс)", command=update_animation_speed)
scale.set(animation_speed)
scale.pack(side=tk.BOTTOM, fill=tk.X)

ani = FuncAnimation(fig, update, frames=frames, interval=animation_speed, repeat=False)
window.mainloop()

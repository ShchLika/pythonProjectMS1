import math
import random
import openpyxl

# Формулы распределений с генерацией случайного t внутри
# Функция для генерации экспоненциального распределения
def exponential(lmbda):
    """Экспоненциальное распределение."""
    t = random.uniform(0, 1)  # Генерация случайного числа t ∈ [0, 1]
    return lmbda * math.exp(-lmbda * t)

# Функция для генерации нормального распределения
def normal(mean, sigma):
    """Нормальное распределение."""
    t = random.uniform(0, 1)  # Генерация случайного числа t ∈ [0, 1]
    coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
    exponent = math.exp(-((t - mean) ** 2) / (2 * sigma ** 2))
    return coefficient * exponent

# Генерация данных
rows = 2000  # Количество строк данных
lmbda_1 = 0.1  # Лямбда для t1
sigma_2, m_2 = 5, 25  # Параметры нормального распределения для t2
sigma_3, m_3 = 5, 30  # Параметры нормального распределения для t3

# Создание Excel файла
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Distributions"

# Заголовки
ws.append(["t1 (Exponential)", "t2 (Normal)", "t3 (Normal)"])

# Заполнение данных
for _ in range(rows):
    t1 = exponential(lmbda_1)
    t2 = normal(m_2, sigma_2)
    t3 = normal(m_3, sigma_3)
    ws.append([t1, t2, t3])

# Сохранение Excel файла
output_file = "distributions5.xlsx"
wb.save(output_file)
print(f"Данные успешно сохранены в файл {output_file}")

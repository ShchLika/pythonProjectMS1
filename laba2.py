import math
import random
import pandas as pd

def exponential_distribution(lmbda, n=2000):
    """
    Генерация случайных чисел с показательного распределения.
    Используется формула: y_i = -(1 / lambda) * ln(x_i)
    """
    values = []
    for _ in range(n):
        x_i = random.random()  # Генерация случайного числа от 0 до 1
        y_i = -(1 / lmbda) * math.log(x_i)
        values.append(y_i)
    return values

def normal_distribution(sigma, m, n=2000):
    """
    Генерация случайных чисел с нормального распределения (по формуле Лапласса).
    Используется формула: y_i = sigma * cos(2 * pi * x_i) * sqrt(-2 * ln(x_i)) + m
    """
    values = []
    for _ in range(n):
        x_i = random.random()  # Генерация случайного числа от 0 до 1
        x_i2 = random.random()
        y_i = sigma * math.cos(2 * math.pi * x_i) * math.sqrt(-2 * math.log(x_i2)) + m
        values.append(y_i)
    return values

def main():
    # Параметры из задачи
    lambda_1 = 0.1
    sigma_2, m2 = 5, 25
    sigma_3, m3 = 5, 30
    n = 2000

    # Генерация значений
    t1 = exponential_distribution(lambda_1, n)
    t2 = normal_distribution(sigma_2, m2, n)
    t3 = normal_distribution(sigma_3, m3, n)

    # Создание DataFrame для сохранения в Excel
    data = {
        't1 (Exponential)': t1,
        't2 (Normal, sigma=5, m=25)': t2,
        't3 (Normal, sigma=5, m=30)': t3
    }
    df = pd.DataFrame(data)

    # Сохранение в Excel
    df.to_excel('random_distributions_final.xlsx', index=False)
    print("Файл успешно сохранен как 'random_distributions_final.xlsx'")

if __name__ == "__main__":
    main()

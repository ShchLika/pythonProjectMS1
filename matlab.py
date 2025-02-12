import numpy as np
import matplotlib.pyplot as plt

# Создание вектора значений x в диапазоне [0, 48]
x = np.arange(0, 48.1, 0.1)

# Инициализация функции принадлежности
membership = np.zeros_like(x)

# Вычисление степени принадлежности
for i in range(len(x)):
    if x[i] <= 16:
        membership[i] = 1  # Степень принадлежности равна 1, если x <= 16
    elif x[i] < 32:
        membership[i] = 1 - (x[i] - 16) / (32 - 16)  # Линейное уменьшение степени
    else:
        membership[i] = 0  # Степень принадлежности равна 0, если x >= 32

# Построение графика
plt.figure()
plt.plot(x, membership, linewidth=2)
plt.title('График функции принадлежности для нечёткого подмножества')
plt.xlabel('x')
plt.ylabel('Степень принадлежности')
plt.grid(True)
plt.show()

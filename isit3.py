import numpy as np

# Сигмоида и её производная
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Нормализация данных
def normalize_data(data, min_val=None, max_val=None):
    if min_val is None or max_val is None:
        min_val = np.min(data, axis=0)
        max_val = np.max(data, axis=0)
    return (data - min_val) / (max_val - min_val), min_val, max_val

# Пример данных: время в пути, стоимость, количество услуг, уровень комфорта
raw_data = np.array([
    [0.3, 0.2, 0.8, 0.9],
    [0.7, 0.8, 0.2, 0.2],
    [0.5, 0.4, 0.6, 0.6],
    [0.2, 0.7, 0.3, 0.4]
])

inputs, min_val, max_val = normalize_data(raw_data[:, :-1])  # Входные параметры
true_output = raw_data[:, -1:]  # Истинные значения

# Инициализация весов
np.random.seed(42)
input_to_hidden_weights = np.random.rand(3, 4)
hidden_to_output_weights = np.random.rand(4, 1)

learning_rate = 0.5
iterations = 2

# Обучение
for iteration in range(iterations):
    hidden_layer_input = np.dot(inputs, input_to_hidden_weights)
    hidden_layer_output = sigmoid(hidden_layer_input)

    output_layer_input = np.dot(hidden_layer_output, hidden_to_output_weights)
    predicted_output = sigmoid(output_layer_input)

    # Вычисление ошибки
    error = true_output - predicted_output
    mse = np.mean(error ** 2)

    # Обратное распространение
    d_predicted_output = error * sigmoid_derivative(predicted_output)
    error_hidden_layer = d_predicted_output.dot(hidden_to_output_weights.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

    # Обновление весов
    hidden_to_output_weights += hidden_layer_output.T.dot(d_predicted_output) * learning_rate
    input_to_hidden_weights += inputs.T.dot(d_hidden_layer) * learning_rate

# Пример нового маршрута
new_route = np.array([[0.4, 0.3, 0.7]])
normalized_route = (new_route - min_val) / (max_val - min_val)
predicted_comfort = sigmoid(np.dot(sigmoid(np.dot(normalized_route, input_to_hidden_weights)), hidden_to_output_weights))
print("Предсказанный уровень комфорта:", predicted_comfort)



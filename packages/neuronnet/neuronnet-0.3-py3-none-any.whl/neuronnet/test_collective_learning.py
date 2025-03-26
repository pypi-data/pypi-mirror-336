import numpy as np
from collective_learning import CollectiveLearningModel, collective_training

def test_collective_learning():
    input_size = 10
    hidden_size = 5
    output_size = 2
    num_models = 3
    epochs = 300
    learning_rate = 0.001
    batch_size = 5

    # Создаем несколько моделей
    models = [CollectiveLearningModel(input_size, hidden_size, output_size) for _ in range(num_models)]
    
    # Генерируем случайные данные для обучения
    X = np.random.rand(100, input_size)
    y = np.random.rand(100, output_size)

    # Запускаем коллективное обучение
    collective_training(models, X, y, epochs, learning_rate, batch_size)

    print("Тест завершен успешно.")

if __name__ == "__main__":
    test_collective_learning()

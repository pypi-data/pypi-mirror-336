import numpy as np

class CollectiveLearningModel:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.zeros((1, hidden_size))
        self.bias_output = np.zeros((1, output_size))

    def forward(self, X):
        hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        hidden_output = np.tanh(hidden_input)
        final_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        return final_input, hidden_output

    def backward(self, X, y, output, hidden_output, learning_rate):
        output_error = output - y
        output_gradient = output_error
        hidden_error = np.dot(output_gradient, self.weights_hidden_output.T)
        hidden_gradient = hidden_error * (1 - hidden_output ** 2)

        self.weights_input_hidden -= learning_rate * np.dot(X.T, hidden_gradient)
        self.weights_hidden_output -= learning_rate * np.dot(hidden_output.T, output_gradient)
        self.bias_hidden -= learning_rate * np.sum(hidden_gradient, axis=0, keepdims=True)
        self.bias_output -= learning_rate * np.sum(output_gradient, axis=0, keepdims=True)

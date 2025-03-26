import numpy as np

class CollectiveLearningModel:
    def __init__(self, input_size, hidden_size, output_size, activation_function='relu'):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.zeros((1, hidden_size))
        self.bias_output = np.zeros((1, output_size))
        self.activation_function = activation_function

    def forward(self, X):
        hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        if self.activation_function == 'relu':
            hidden_output = np.maximum(0, hidden_input)  # ReLU activation
        elif self.activation_function == 'tanh':
            hidden_output = np.tanh(hidden_input)  # Tanh activation
        elif self.activation_function == 'sigmoid':
            hidden_output = 1 / (1 + np.exp(-hidden_input))  # Sigmoid activation
        final_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        return final_input, hidden_output

    def backward(self, X, y, output, learning_rate, lambda_reg=0.01):
        output_error = output - y
        output_gradient = output_error
        hidden_error = np.dot(output_gradient, self.weights_hidden_output.T)

        if self.activation_function == 'relu':
            hidden_gradient = hidden_error * (hidden_output > 0)  # ReLU derivative
        elif self.activation_function == 'tanh':
            hidden_gradient = hidden_error * (1 - hidden_output ** 2)  # Tanh derivative
        elif self.activation_function == 'sigmoid':
            hidden_gradient = hidden_error * (hidden_output * (1 - hidden_output))  # Sigmoid derivative

        self.weights_input_hidden -= learning_rate * (np.dot(X.T, hidden_gradient) + lambda_reg * self.weights_input_hidden)
        self.weights_hidden_output -= learning_rate * (np.dot(hidden_output.T, output_gradient) + lambda_reg * self.weights_hidden_output)
        self.bias_hidden -= learning_rate * np.sum(hidden_gradient, axis=0, keepdims=True)
        self.bias_output -= learning_rate * np.sum(output_gradient, axis=0, keepdims=True)

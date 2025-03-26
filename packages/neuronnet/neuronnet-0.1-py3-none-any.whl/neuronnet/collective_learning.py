import numpy as np

class CollectiveLearningModel:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.bias_output = np.random.randn(output_size)
    
    def forward(self, X):
        self.hidden = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.hidden = np.maximum(0, self.hidden)  # ReLU activation
        output = np.dot(self.hidden, self.weights_hidden_output) + self.bias_output
        return output, self.hidden
    
    def backward(self, X, y, output, learning_rate):
        error = y - output
        output_grad = error
        hidden_grad = np.dot(output_grad, self.weights_hidden_output.T)
        
        self.weights_input_hidden += learning_rate * np.dot(X.T, hidden_grad)
        self.weights_hidden_output += learning_rate * np.dot(self.hidden.T, output_grad)
        self.bias_hidden += learning_rate * np.sum(hidden_grad, axis=0)
        self.bias_output += learning_rate * np.sum(output_grad, axis=0)
    
def collective_training(models, X, y, epochs, learning_rate):
    for epoch in range(epochs):
        for model in models:
            output, _ = model.forward(X)
            for other_model in models:
                if other_model != model:
                    other_output, _ = other_model.forward(X)
                    output += other_output
            model.backward(X, y, output / len(models), learning_rate)

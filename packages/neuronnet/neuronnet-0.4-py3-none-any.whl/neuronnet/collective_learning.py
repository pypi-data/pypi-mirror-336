import numpy as np

class AdamOptimizer:
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, decay_rate=0.0):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.t = 0

    def update(self, param, grad):
        self.t += 1
        if self.m is None:
            self.m = np.zeros_like(param)
            self.v = np.zeros_like(param)
        
        self.m = self.beta1 * self.m + (1 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grad ** 2)
        
        m_hat = self.m / (1 - self.beta1 ** self.t)
        v_hat = self.v / (1 - self.beta2 ** self.t)
        
        param -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
        return param

class CollectiveLearningModel:
    def __init__(self, input_size, hidden_size, output_size, activation_function='relu'):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.bias_output = np.random.randn(output_size)
    
    def forward(self, X):
        self.hidden = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        if activation_function == 'relu':
            self.hidden = np.maximum(0, self.hidden)  # ReLU activation
        elif activation_function == 'tanh':
            self.hidden = np.tanh(self.hidden)  # Tanh activation
        elif activation_function == 'sigmoid':
            self.hidden = 1 / (1 + np.exp(-self.hidden))  # Sigmoid activation
        output = np.dot(self.hidden, self.weights_hidden_output) + self.bias_output
        return output, self.hidden
    
    def backward(self, X, y, output, learning_rate, lambda_reg=0.01):
        error = y - output
        output_grad = error
        hidden_grad = np.dot(output_grad, self.weights_hidden_output.T)
        
        self.weights_input_hidden += learning_rate * (np.dot(X.T, hidden_grad) + lambda_reg * self.weights_input_hidden)
        self.weights_hidden_output += learning_rate * (np.dot(self.hidden.T, output_grad) + lambda_reg * self.weights_hidden_output)
        self.bias_hidden += learning_rate * np.sum(hidden_grad, axis=0)
        self.bias_output += learning_rate * np.sum(output_grad, axis=0)
    
def collective_training(models, X, y, epochs, learning_rate, batch_size=32, early_stopping=False, patience=5):
    optimizer = AdamOptimizer(learning_rate)
    previous_loss = float('inf')
    for epoch in range(epochs):
        if early_stopping and epoch > 0 and previous_loss > 0:  # Ensure previous_loss is defined
            print("Early stopping triggered after {} epochs".format(patience))
            break

        loss = np.mean((y - output) ** 2)  # Calculate loss for early stopping
        for i in range(0, X.shape[0], batch_size): 
            X_batch = X[i:i+batch_size]
            y_batch = y[i:i+batch_size]
            for model in models:
                output, _ = model.forward(X_batch)
                for other_model in models:
                    if other_model != model:
                        other_output, _ = other_model.forward(X_batch)
                        output += other_output
                model.backward(X_batch, y_batch, output / len(models), learning_rate)
        
        if epoch % 100 == 0:
            print(f"Epoch {epoch}/{epochs} completed")

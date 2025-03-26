def collective_training(models, X, y, epochs, learning_rate):
    for epoch in range(epochs):
        for model in models:
            output, hidden_output = model.forward(X)
            model.backward(X, y, output, hidden_output, learning_rate)
        if epoch % 100 == 0:
            print(f"Epoch {epoch}/{epochs} completed")

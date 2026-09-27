import numpy as np

# ----- Activation Function -----
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(a):
    return a * (1 - a)   # derivative using activated output

# ----- Initialize Parameters -----
np.random.seed(42)

W1 = np.random.randn(2, 3)
b1 = np.random.randn(1, 3)

W2 = np.random.randn(3, 1)
b2 = np.random.randn(1, 1)

learning_rate = 0.01

# ----- Single Training Example -----
x = np.array([[0.5, 0.8]])   # shape (1,2)
y = np.array([[1]])          # shape (1,1)

# ================================
#        FORWARD PROPAGATION
# ================================

z1 = np.dot(x, W1) + b1
a1 = sigmoid(z1)

z2 = np.dot(a1, W2) + b2
a2 = sigmoid(z2)   # final output

# Loss (Mean Squared Error)
loss = np.mean((y - a2) ** 2)

print("Output:", a2)
print("Loss:", loss)

# ================================
#        BACKPROPAGATION
# ================================

# Output layer error
dL_da2 = -2 * (y - a2)
da2_dz2 = sigmoid_derivative(a2)
dL_dz2 = dL_da2 * da2_dz2

# Gradients for W2 and b2
dL_dW2 = np.dot(a1.T, dL_dz2)
dL_db2 = dL_dz2

# Hidden layer error
dL_da1 = np.dot(dL_dz2, W2.T)
da1_dz1 = sigmoid_derivative(a1)
dL_dz1 = dL_da1 * da1_dz1

# Gradients for W1 and b1
dL_dW1 = np.dot(x.T, dL_dz1)
dL_db1 = dL_dz1

# ================================
#        UPDATE WEIGHTS
# ================================

W2 -= learning_rate * dL_dW2
b2 -= learning_rate * dL_db2

W1 -= learning_rate * dL_dW1
b1 -= learning_rate * dL_db1

print("Updated W1:", W1)
print("Updated W2:", W2)
import numpy as np

# -----------------------------
# Activation Function
# -----------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def derivative(y):
    # derivative using output y
    return y * (1 - y)

# -----------------------------
# Given Data
# -----------------------------
# Inputs
X = np.array([0.3, 0.5])

# Target (from your work)
target = 0.8

# Learning rate
lr = 0.01

# -----------------------------
# Initial Weights (Hidden Layer)
# -----------------------------
W_hidden = np.array([
    [2.5, 3.0],   # Neuron 1
    [2.0, 0.5],   # Neuron 2
    [1.5, 1.0]    # Neuron 3
])

b_hidden = np.array([1.5, -1.5, 0.5])

# -----------------------------
# Output Layer Weights
# -----------------------------
W_output = np.array([5.0, 2.5, 2.0])
b_output = 3.5

# =====================================================
#                FORWARD PASS
# =====================================================

# Hidden layer linear combination
S_hidden = np.dot(W_hidden, X) + b_hidden

# Hidden layer activation
Y_hidden = sigmoid(S_hidden)

# Output layer linear combination
S_output = np.dot(W_output, Y_hidden) + b_output

# Output activation
Y_output = sigmoid(S_output)

print("Forward Pass Results")
print(f"{'='*80}")
print("Activations Function Results (hidden layer):", Y_hidden)
print("Output Layer Activation Function Result:", Y_output)
print(f"{'='*80}")

# =====================================================
#                BACKPROPAGATION
# =====================================================

# Output layer delta
delta_output = derivative(Y_output) * (target - Y_output)

# Update output weights
dW_output = lr * delta_output * Y_hidden
db_output = lr * delta_output

W_output_new = W_output + dW_output
b_output_new = b_output + db_output

# Hidden layer deltas
delta_hidden = derivative(Y_hidden) * (W_output * delta_output)

# Update hidden weights
dW_hidden = lr * np.outer(delta_hidden, X)
db_hidden = lr * delta_hidden

W_hidden_new = W_hidden + dW_hidden
b_hidden_new = b_hidden + db_hidden

# =====================================================
#                RESULTS AFTER 1 EPOCH
# =====================================================

print("\nAfter 1 Epoch Update")
print(f"{'='*60}")
print("\nNew Output Weights:", W_output_new)
print("Updated Output Bias:", b_output_new)

print("\nNew Hidden Weights:\n", W_hidden_new)
print("New Hidden Biases:", b_hidden_new)
print(f"{'='*60}")

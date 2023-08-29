from scipy.io import loadmat
import numpy as np
from Model import neural_network
from RandInitialize import initialise
from Prediction import predict
from scipy.optimize import minimize

data = loadmat('mnist-original.mat')
X = data['data'].transpose() / 255
y = data['label'].flatten()
X_train, y_train = X[:60000, :], y[:60000]
X_test, y_test = X[60000:, :], y[60000:]
m = X.shape[0]
input_layer_size = 784
hidden_layer_size = 100
num_labels = 10
initial_Theta1 = initialise(hidden_layer_size, input_layer_size)
initial_Theta2 = initialise(num_labels, hidden_layer_size)
initial_nn_params = np.concatenate((initial_Theta1.flatten(), initial_Theta2.flatten()))
maxiter = 100
lambda_reg = 0.1
myargs = (input_layer_size, hidden_layer_size, num_labels, X_train, y_train, lambda_reg)
results = minimize(neural_network, x0=initial_nn_params, args=myargs,
                   options={'disp': True, 'maxiter': maxiter}, method="L-BFGS-B", jac=True)
nn_params = results["x"]
Theta1 = np.reshape(nn_params[:hidden_layer_size * (input_layer_size + 1)],
                    (hidden_layer_size, input_layer_size + 1))
Theta2 = np.reshape(nn_params[hidden_layer_size * (input_layer_size + 1):],
                    (num_labels, hidden_layer_size + 1))
pred = predict(Theta1, Theta2, X_test)
print('Test Set Accuracy: {:f}'.format((np.mean(pred == y_test) * 100)))
pred = predict(Theta1, Theta2, X_train)
print('Training Set Accuracy: {:f}'.format((np.mean(pred == y_train) * 100)))
true_positive = 0
for i in range(len(pred)):
    if pred[i] == y_train[i]:
        true_positive += 1
false_positive = len(y_train) - true_positive
print('Precision =', true_positive / (true_positive + false_positive))
np.savetxt('Theta1.txt', Theta1, delimiter=' ')
np.savetxt('Theta2.txt', Theta2, delimiter=' ')

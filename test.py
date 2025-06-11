from client import Api
import numpy as np
a = Api("192.168.1.81", 5000) #connect
dot = a.dot(10, 20) #multiply
print(dot)
i = np.array([10, 20])
w = np.array([0.1, 0.2])
dot = a.dot(i, w) #scalar multyply from numpy
print(dot)

print(a.get_error(dot, 7)) #error = (true_prediction - prediction) ** 2
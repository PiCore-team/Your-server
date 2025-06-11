from client import Api
import numpy as np
a = Api("YOUR_SERVER_ID", PORT) #connect
dot = a.dot(10, 20) #multiply
print(dot)
i = np.array([10, 20])
w = np.array([0.1, 0.2])
dot = a.dot(i, w) #scalar multyply from numpy
print(dot)

print(a.get_error(dot, 7)) #error = (true_prediction - prediction) ** 2

a.echo("Done") #echo like a win cmd

print(a.sysinfo()) #print server system info

res = a.send_application(f"{dot} * 3 + 9") #calculate on server
print(res)

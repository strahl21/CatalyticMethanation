import numpy as np
from Model_functions import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# I want to simulate the PBR with the proper parameters and look at end point
file_name_params = "allparametersIncludeHighT.csv"

data = np.genfromtxt(file_name_params, skip_header = True, delimiter = ",")
print(data)
weight = np.linspace(0, 2, 25)
initial_condition = [0, 0]

data_reorganized = np.empty(data.shape)
print(data[0][:])

measured = data[:,4]
predicted = []

run = 0
for i in range(len(data)):
    #A = data[i][0]
    #E_a = data[i][1]
    #lpha = data[i][2]
    #beta = data[i][3]
    A = 0.0436489
    E_a = 0.842941
    alpha = 0.31416
    beta = 0.115857
    T = data[i][0]
    F_CO2_0 = data[i][1]
    F_H2_0 = data[i][2]
    FT_0 = data[i][3]
    #measured = data[i][4] # this is actual measured conversion
    v_0 = data[i][5]

    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    run += 1
    predicted.append(simulate[:,0][-1])
    #plot_result(simulate, measured, weight, run)

#print(len(predicted))
#print(measured)
print(predicted)
plt.scatter(np.linspace(0, len(predicted), len(predicted)), predicted, label = "Predicted")
plt.scatter(np.linspace(0, len(predicted), len(predicted)), measured, label = "Measured")
plt.xlabel("Experiment #")
plt.ylabel("Conversion")
plt.legend()
plt.show()

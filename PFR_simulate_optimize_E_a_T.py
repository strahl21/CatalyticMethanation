import numpy as np
from Model_functions import *
from scipy.integrate import odeint
from scipy.optimize import minimize

# I want to simulate the PBR with the proper parameters and look at end point
#file_name_params = "allparameters270300.csv" # just 300 270
#file_name_params = "allparametersNot325.csv" # just 300 270 285 250
#file_name_params = "allparametersIncludeHighT.csv" # just 300 270 285 325 250
file_name_params = "allparameters325.csv"


data = np.genfromtxt(file_name_params, skip_header = True, delimiter = ",")
weight = np.linspace(0, 2, 25)
initial_condition = [0, 0]

def objective_PBR(vars, data):
    predicted = []
    for i in range(len(data)):
        A = 0.043299
        E_a = vars[0]
        alpha = 0.6
        beta = 0.1
        T = data[i][0]
        F_CO2_0 = data[i][1]
        F_H2_0 = data[i][2]
        FT_0 = data[i][3]
        v_0 = data[i][5]
        simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
        predicted.append(simulate[:,0][-1])
    measured = np.array(data[:,4]) # this is actual measured conversion
    predicted = np.array(predicted)
    #print(predicted)
    return sum((predicted - measured) ** 2)

    #plot_result(simulate, measured, weight
# guess for all pts 0.05, 0.85, 0.3, 0.1
# initialization
E_a_0 = 0.89
method = 'SLSQP'
initialization = np.array([E_a_0])

#bounds = ((0, 0.3), (0, 1), (0.4, 0.7), (0.1, 0.5))

regression_result = minimize(objective_PBR, initialization, args=(data), method=method)#, bounds=bounds)

print("Initial sum of squared error = ", objective_PBR([E_a_0], data))

if regression_result.success:
    print("Success")
else:
    print(regression_result.message)

E_a = regression_result.x

print("Final sum of squared error = ", objective_PBR([E_a], data))

print("E_a = ", E_a)

import numpy as np
from Model_functions import *
from scipy.integrate import odeint
from scipy.optimize import minimize

# I want to simulate the PBR with the proper parameters and look at end point
#file_name_params = "allparameters270300.csv" # just 300 270
#file_name_params = "allparametersNot325.csv" # just 300 270 285 250
#file_name_params = "allparametersIncludeHighT.csv" # just 300 270 285 325 250
#file_name_params = "allparametersHighTOnly.csv"
#file_name_params = "allparametersInclude285300.csv"
file_name_params = "allparametersLowT.csv"


data = np.genfromtxt(file_name_params, skip_header = True, delimiter = ",")
weight = np.linspace(0, 2, 25)
initial_condition = [0, 0]

def objective_PBR(vars, data):
    predicted = []
    for i in range(len(data)):
        A = vars[0]
        E_a = vars[1]
        alpha = vars[2]
        beta = vars[3]
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
A_0 = 0.05
E_a_0 = 0.79
alpha_0 = 0.45
beta_0 = 0.13
method = 'L-BFGS-B'
initialization = np.array([A_0, E_a_0, alpha_0, beta_0])

bounds = ((0, 0.3), (0, 1), (0.4, 0.7), (0.1, 0.5))

regression_result = minimize(objective_PBR, initialization, args=(data), method=method, bounds=bounds)

print("Initial sum of squared error = ", objective_PBR([A_0, E_a_0, alpha_0, beta_0], data))

if regression_result.success:
    print("Success")
else:
    print(regression_result.message)

A, E_a, alpha, beta = regression_result.x

print("Final sum of squared error = ", objective_PBR([A, E_a, alpha, beta], data))

print("A = ", A)
print("E_a = ", E_a)
print("alpha = ", alpha)
print("beta = ", beta)

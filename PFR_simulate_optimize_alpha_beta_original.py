import numpy as np
from Model_functions import *
from scipy.integrate import odeint
from scipy.optimize import minimize

# I want to simulate the PBR with the proper parameters and look at end point
#file_name_params = "allparameters270300.csv" # just 300 270
#file_name_params = "allparametersNot325.csv" # just 300 270 285 250
#file_name_params = "allparametersIncludeHighT.csv" # just 300 270 285 325
#file_name_params = "allparameters250.csv"
#file_name_params = "allparameters270.csv"
#file_name_params = "allparameters285.csv"
#file_name_params = "allparameters300.csv"
#file_name_params = "allparameters325.csv"
file_name_params = "allparametersConstCompT.csv"

data = np.genfromtxt(file_name_params, skip_header = True, delimiter = ",")
weight = np.linspace(0, 2, 25)
initial_condition = [0, 0]

def objective_PBR(vars, data):
    predicted = []
    for i in range(len(data)):
        #A = 0.0432994
        #E_a = 0.7876877
        A = 0.043299
        #E_a = 0.746652
        E_a = 0.787688
        alpha = vars[0]
        beta = vars[1]
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
alpha_0 = 0.5
beta_0 = 0.1
method = 'SLSQP'
initialization = np.array([alpha_0, beta_0])

#bounds = ((0, 1), (0.8, 1.0), (0.3, 0.6), (0.1, 0.3))

regression_result = minimize(objective_PBR, initialization, args=(data), method=method)#, bounds=bounds)

print("Initial sum of squared error = ", objective_PBR([alpha_0, beta_0], data))

if regression_result.success:
    print("Success")
else:
    print(regression_result.message)

alpha, beta = regression_result.x

print("Final sum of squared error = ", objective_PBR([alpha, beta], data))

print("alpha = ", alpha)
print("beta = ", beta)

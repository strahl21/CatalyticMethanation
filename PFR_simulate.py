import numpy as np
from Model_functions import *
from scipy.integrate import odeint

# I want to simulate the PBR with the proper parameters and look at end point
#file_name_params = "allparametersIncludeHighT.csv"
file_name_params = "allparameters325.csv"

data = np.genfromtxt(file_name_params, skip_header = True, delimiter = ",")
print(data)
weight = np.linspace(0, 2, 25)
initial_condition = [0, 0]

#measured = data[:,4]
#predicted = []

run = 0
for i in range(len(data)):
    #A = data[i][0]
    #E_a = data[i][1]
    #lpha = data[i][2]
    #beta = data[i][3]
    A = 0.060046
    E_a = 0.746652
    alpha = 0.5169
    beta = 0.17615
    T = data[i][0]
    F_CO2_0 = data[i][1]
    F_H2_0 = data[i][2]
    FT_0 = data[i][3]
    measured = data[i][4] # this is actual measured conversion
    v_0 = data[i][5]

    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    run += 1
    #print(simulate)
    plot_result(simulate, measured, weight, run)

from mainFunc import nonLinearConfInt
from Model_functions import *
import numpy as np
from scipy.integrate import odeint
#(func, param1, param2, dataY, **kwargs)
# function = PBR_differentiate
# param 1 = alpha
# param 2 = beta
# data Y = measured
# kwargs:
data = np.genfromtxt("allparametersLowT.csv", skip_header = True, delimiter = ',')

"""
# parameter 1 = alpha
# parameter 2 = beta
dataY = data[:,4]
T = data[:,0]
CO2_0 = data[:,1]
H2_0 = data[:,2]
FT_0 = data[:,3]
v_0 = data[:,5]
E_0 = np.ones(len(data[:,4])) * 0.797136
A_0 = np.ones(len(data[:,5])) * 0.058322
alpha = 0.45#1773
beta = 0.13#129935
#alpha, beta, A, E_a, T, F_CO2_0, F_H2_0, FT_0, v_0
args = (A_0, E_0, T, CO2_0, H2_0, FT_0, v_0)

nonLinearConfInt(PBR_differentiate1, alpha, beta, dataY, args=args, perturb1 = 0.25, perturb2 = 0.7, pts1 = 60, pts2 = 60)
"""
# parameter 1 = alpha
# parameter 2 = beta
dataY = data[:,4]
T = data[:,0]
CO2_0 = data[:,1]
H2_0 = data[:,2]
FT_0 = data[:,3]
v_0 = data[:,5]
E_0 = 0.797136
A_0 = 0.058322
alpha = np.ones(len(data[:,5])) * 0.451773
beta = np.ones(len(data[:,5])) * 0.129935
#alpha, beta, A, E_a, T, F_CO2_0, F_H2_0, FT_0, v_0
args = (alpha, beta, T, CO2_0, H2_0, FT_0, v_0)

nonLinearConfInt(PBR_differentiate2, A_0, E_0, dataY, args=args, perturb1 = 0.75, perturb2 = 0.1, pts1 = 100, pts2 = 100)

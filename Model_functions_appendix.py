import numpy as np
from scipy.integrate import quad, odeint
import matplotlib.pyplot as plt

# CONSTANTS
# stoich coefficients
d = 2
c = 1
b = 4
a = 1

# Universal gas constant
R = 8.3145 # J / mol * K

def sccm_to_molar(sccm):
    # sccm to mol / hr
    return sccm * 7.45e-7 * 3600

# arrhenius equation
def arrhenius_equation(A, E_a, T):
    # pre-exponential factor and activation energy scaled for solver
    return A * 10**8 * np.exp(-E_a * 10**5 / (R * T))

# total molar flow as a function of conversion
def flow_total(F_CO2_0, X_CO2, FT_0):
    return (FT_0 + (d / a + c / a - b / a - 1) * F_CO2_0 * X_CO2)

# volumetric flow rate as a function of conversion
def volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0):
    return v_0 * (flow_total(F_CO2_0, X_CO2, FT_0) / FT_0)

# molar flow hydrogen = f(X_CO2)
def F_H2(X_CO2, F_H2_0):
    return F_H2_0 * (1 - d / a * X_CO2)

# molar flow CO2 = f(X_CO2)
def F_CO2(X_CO2, F_CO2_0):
    return F_CO2_0 * (1 - X_CO2)

# reaction rate for reaction
def rate(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0):
    first_part = arrhenius_equation(A, E_a, T)
    second_part = (F_H2(X_CO2, F_H2_0) / volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0)) ** alpha
    third_part =  (F_CO2(X_CO2, F_CO2_0) / volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0)) ** beta
    rate = first_part * second_part * third_part
    return rate

#-------------------------------------------------------------------------------
#--------------------------PBR FUNCTIONS----------------------------------------

def PBR(X_CO2, W, A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0):
    # PBR design equation in terms of dX/dW
    return rate(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0) / F_CO2_0

def PBR_differentiate1(alpha, beta, A, E_a, T, F_CO2_0, F_H2_0, FT_0, v_0):
    # numerically solves ODE and returns value. This function allows determination
    # of alpha and beta after activation energy and A are determined
    initial_condition = [0,0]
    weight = np.linspace(0, 2, 25)
    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    predicted = simulate[:,0][-1]
    return predicted

def PBR_differentiate2(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0):
    # numerically solves ODE and returns value. This function allows determination
    # of activation energy and A after alpha and beta are determined
    initial_condition = [0,0]
    weight = np.linspace(0, 2, 25)
    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    predicted = simulate[:, 0][-1]
    return predicted

def objective_PBR(vars, data):
    # this function finds the sum of squared errors for the PBR design equation
    # as a function of the parameters of interest. It minimized by solver
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
    measured = np.array(data[:,4])
    predicted = np.array(predicted)
    return sum((predicted - measured) ** 2)

def plot_result(y, measured, weight, run):
    # plots the result
    measured_line = np.ones(len(y)) * measured
    print("Theoretic Values = ", y[:,1])
    plt.figure()
    plt.plot(weight, y[:,1], label = "Theoretic Conversion")
    plt.plot(weight, measured_line, label = "Measured Conversion")
    plt.xlabel("Weight PBR")
    plt.ylabel("Conversion CO2")
    plt.legend()
    plt.title("Run: (%d)" %run)
    plt.show()
    return

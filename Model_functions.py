import numpy as np
from scipy.integrate import quad, odeint
import matplotlib.pyplot as plt

# CONSTANTS
# stoich coefficients
d = 2
c = 1
b = 4
a = 1

R = 8.3145 # J / mol * K

def sccm_to_molar(sccm):
    # sccm to mol / hr
    return sccm * 7.45e-7 * 3600
# arrhenius equation
def arrhenius_equation(A, E_a, T):
    return A * 10**8 * np.exp(-E_a * 10**5 / (R * T))

# volumetric flow as a function of conversion
def flow_total(F_CO2_0, X_CO2, FT_0):
    return (FT_0 + (d / a + c / a - b / a - 1) * F_CO2_0 * X_CO2)

def volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0):
    return v_0 * (flow_total(F_CO2_0, X_CO2, FT_0) / FT_0)

# molar flow hydrogen = f(X)
def F_H2(X_CO2, F_H2_0):
    return F_H2_0 * (1 - d / a * X_CO2)

# molar flow CO2 = f(X)
def F_CO2(X_CO2, F_CO2_0):
    return F_CO2_0 * (1 - X_CO2)

# converts the molar flows to pressures
def to_pressure(alpha, beta, T):
    return ((R * T) ** (alpha * beta))

def rate(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0):
    first_part = arrhenius_equation(A, E_a, T)
    second_part = (F_H2(X_CO2, F_H2_0) / volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0)) ** alpha
    third_part =  (F_CO2(X_CO2, F_CO2_0) / volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0)) ** beta
    #print("molar flow h2 = ", F_H2(X_CO2, F_H2_0))
    #print("first part = ", first_part)
    #print("arrhenius = ", arrhenius_equation(A, E_a, T))

    #print("second part = ", second_part)
    #print("third part = ", third_part)
    #print("E_a = ", E_a)
    #print("A = ", A)

    rate = first_part * second_part * third_part
    #print("molar flow CO2 = ", F_CO2(X_CO2, F_CO2_0))
    #print("alpha = ", alpha)
    #print("beta = ", beta)
    return rate

#-------------------------------------------------------------------------------
#------------------------CSTR FUNCTIONS-----------------------------------------

def design_equation_CSTR(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0):
    lhs_first_part = arrhenius_equation(A, E_a, T)
    lhs_second_part = (F_H2(X_CO2, F_H2_0) / volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0)) ** alpha
    print(F_H2(X_CO2, F_H2_0))
    lhs_third_part =  (F_CO2(X_CO2, F_CO2_0) / volumetric_flow(v_0, F_CO2_0, X_CO2, FT_0)) ** beta
    lhs = lhs_first_part * lhs_second_part * lhs_third_part
    return lhs

# create sum of sq error objective function for parameter regression
def objective_function_CSTR(vars, predicted, measured):
    predicted_result = np.zeros(len(predicted))
    for i in range(len(predicted)):
        T = predicted[i][0]
        #print("T = ", T)
        F_CO2_0 = predicted[i][1]
        #print("F_CO2_0 = ", F_CO2_0)
        F_H2_0 = predicted[i][2]
        #print("F_H2_0 = ", F_H2_0)
        FT_0 = predicted[i][3]
        #print("FT_0 = ", FT_0)
        X_CO2 = predicted[i][4]
        #print("X_CO2 = ", X_CO2)
        v_0 = predicted[i][5]
        #print("v_0 = ", v_0)
        predicted_result[i] = design_equation_CSTR(vars[0], vars[1], vars[2], vars[3], T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0)
    #print(measured)
    sum_sq_errors = (sum(predicted_result ** 2 - measured ** 2))
    #print("Sum squared errors = ", sum_sq_errors)
    return sum_sq_errors

def objective_function_CSTR_single(vars, predicted, measured):
        T = predicted[0]
        #print("T = ", T)
        F_CO2_0 = predicted[1]
        #print("F_CO2_0 = ", F_CO2_0)
        F_H2_0 = predicted[2]
        #print("F_H2_0 = ", F_H2_0)
        FT_0 = predicted[3]
        #print("FT_0 = ", FT_0)
        X_CO2 = predicted[4]
        #print("X_CO2 = ", X_CO2)
        v_0 = predicted[5]
        predicted_result = design_equation_CSTR(vars[0], vars[1], vars[2], vars[3], T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0)

        sum_sq_errors = (predicted_result - measured) ** 2
        return sum_sq_errors


#-------------------------------------------------------------------------------
#--------------------------PFR FUNCTIONS----------------------------------------
def design_equation_PFR(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0):
    def toIntegrate(X_CO2):
        return rate(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0) ** (-1)
    return quad(toIntegrate, 0, X_CO2)[0]

def objective_function_PFR(vars, predicted, measured):
    predicted_result = np.zeros(len(predicted))
    for i in range(len(predicted)):
        T = predicted[i][0]
        #print("T = ", T)
        F_CO2_0 = predicted[i][1]
        #print("F_CO2_0 = ", F_CO2_0)
        F_H2_0 = predicted[i][2]
        #print("F_H2_0 = ", F_H2_0)
        FT_0 = predicted[i][3]
        #print("FT_0 = ", FT_0)
        X_CO2 = predicted[i][4]
        #print("X_CO2 = ", X_CO2)
        v_0 = predicted[i][5]
        #print("v_0 = ", v_0)
        predicted_result[i] = design_equation_PFR(vars[0], vars[1], vars[2], vars[3], T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0)

    sum_sq_errors = (sum(predicted_result ** 2 - measured ** 2))
    return sum_sq_errors

#-------------------------------------------------------------------------------
#--------------------------Simulate PBR-----------------------------------------
def PBR(X_CO2, W, A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0):
    return rate(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, X_CO2, v_0) / F_CO2_0

def PBR_differentiate1(alpha, beta, A, E_a, T, F_CO2_0, F_H2_0, FT_0, v_0):
    #print(alpha, beta, A, E_a, T, F_CO2_0, F_H2_0, FT_0, v_0)
    initial_condition = [0,0]
    weight = np.linspace(0, 2, 25)
    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    predicted = simulate[:,0][-1]
    return predicted

def PBR_differentiate2(A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0):
    initial_condition = [0,0]
    weight = np.linspace(0, 2, 25)
    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    predicted = simulate[:, 0][-1]
    return predicted

def PBR_differentiate(alpha, beta, A, E_a, T, F_CO2_0, F_H2_0, FT_0, v_0):
    initial_condition = [0,0]
    weight = np.linspace(0, 2, 25)
    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    predicted = simulate[:, 0][-1]
    return predicted


def plot_result(y, measured, weight, run):
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

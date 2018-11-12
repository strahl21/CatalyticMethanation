import numpy as np
from Model_functions import *
from scipy.integrate import odeint
from scipy.optimize import minimize, basinhopping



def solve_alpha_beta(data):
    alpha_array = []
    beta_array = []
    for i in range(len(data)):
        alpha_0 = 0.5
        beta_0 = 0.2
        method = 'SLSQP'
        initialization = np.array([alpha_0, beta_0])
        """
        minimizer_kwargs = {"method": "SLSQP", "args":(data[i])}
        #bounds = ((0, 4000000000), (80000, 98000), (0.3, 0.6), (0.1, 0.3))
        regression_result = basinhopping(objective_PBR, initialization, niter = 10, minimizer_kwargs = minimizer_kwargs, disp=True)#, stepsize=5.0)#, bounds=bounds)



        print("Initial sum of squared error = ", objective_PBR([alpha_0, beta_0], data[i]))

        alpha, beta = regression_result.x

        print("Final sum of squared error = ", objective_PBR([alpha, beta], data[i]))

        print("alpha = ", alpha)
        print("beta = ", beta)
        """
        bounds = ((0.3, 0.6), (0.1, 0.3))

        regression_result = minimize(objective_PBR, initialization, args=(data[i]), method=method)#, bounds=bounds)

        print("Initial sum of squared error = ", objective_PBR([alpha_0, beta_0], data[i]))

        if regression_result.success:
            print("Success")
        else:
            print(regression_result.message)

        alpha, beta = regression_result.x

        print("Final sum of squared error = ", objective_PBR([alpha, beta], data[i]))

        print("alpha = ", alpha)
        print("beta = ", beta)

        alpha_array.append(alpha)
        beta_array.append(beta)

    return alpha_array, beta_array

def plotTemp(alpha_array, beta_array, data):
    plt.plot(data[:,0], alpha_array, label = "alpha")
    plt.scatter(data[:,0], alpha_array, marker = '+', s = 100)
    plt.xlabel("Temperature C")
    plt.ylabel("Power law value")
    plt.title("Power law alpha vs. T")
    plt.legend()
    plt.show()

    plt.plot(data[:,0], beta_array, label = "beta")
    plt.scatter(data[:,0], beta_array, marker = '+', s = 100)
    plt.xlabel("Temperature C")
    plt.ylabel("Power law value")
    plt.legend()
    plt.title("Power law beta vs. T")
    plt.show()
    return

def plotComp(alpha_array, beta_array, data):
    plt.plot(data, alpha_array, label = "alpha")
    plt.scatter(data, alpha_array, marker = '+', s = 100)
    plt.plot(data, beta_array, label = "beta")
    plt.scatter(data, beta_array, marker = '+', s = 100)
    plt.xlabel("Composition CO2 (%)")
    plt.ylabel("Power law value")
    plt.title("Alpha and Beta dependency on CO2 at 270 C, 20% H2")
    plt.legend()
    plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6])
    plt.show()

    return

def objective_PBR(vars, data):
    predicted = []
    A = 0.0432994
    E_a = 0.7876877
    #A = data[7]
    #E_a = 0.746652
    #E_a = data[6]
    alpha = vars[0]
    beta = vars[1]
    T = data[0]
    F_CO2_0 = data[1]
    F_H2_0 = data[2]
    FT_0 = data[3]
    v_0 = data[5]
    simulate = odeint(PBR, initial_condition, weight, args = (A, E_a, alpha, beta, T, F_CO2_0, F_H2_0, FT_0, v_0))
    predicted.append(simulate[:,0][-1])
    measured = np.array(data[4]) # this is actual measured conversion
    predicted = np.array(predicted)
    #print(predicted)
    return sum((predicted - measured) ** 2)
# I want to simulate the PBR with the proper parameters and look at end point
#file_name_params = "allparameters270300.csv" # just 300 270
#file_name_params = "allparametersNot325.csv" # just 300 270 285 250
#file_name_params = "allparametersIncludeHighT.csv" # just 300 270 285 325
#file_name_params = "allparameters250.csv"
#file_name_params = "allparameters270.csv"
#file_name_params = "allparameters285.csv"
#file_name_params = "allparameters300.csv"
#file_name_params = "allparameters325.csv"
#file_name_params = "allparametersConstCompT.csv"
file_name_params = "concDependParamsCO2.csv"
#file_name_params = "concDependParamsH2.csv"

data = np.genfromtxt(file_name_params, skip_header = True, delimiter = ",")
weight = np.linspace(0, 2, 25)
initial_condition = [0, 0]

alpha, beta = solve_alpha_beta(data)

composition = data[:,6]  # varying CO2
#composition = data[:,7]  # varying H2
plotComp(alpha, beta, composition)



    #plot_result(simulate, measured, weight
# guess for all pts 0.05, 0.85, 0.3, 0.1
# initialization

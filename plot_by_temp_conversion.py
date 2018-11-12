import numpy as np
import matplotlib.pyplot as plt

data_input = np.genfromtxt("allparameters_conv_plot.csv", skip_header = True, delimiter = ',')

num_temperatures = 4
num_points = 8
counter = 0
for i in range(num_temperatures):
    x_1 = data_input[(0 + counter * num_points) : (counter * num_points + 3), 4]
    h2_1 = data_input[(0 + counter * num_points) : (counter * num_points + 3), -1]
    x_2 = data_input[(3 + counter * num_points) : 3 + (counter * num_points + 3), 4]
    h2_2 = data_input[3 + (0 + counter * num_points) : 3 + (counter * num_points + 3), -1]
    x_3 = data_input[(6 + counter * num_points) : 6 + (counter * num_points + 2), 4]
    h2_3 = data_input[6 + (0 + counter * num_points) : 6 + (counter * num_points + 2), -1]

    plt.plot(h2_1, x_1, label = "Constant %.2f %% CO2" %(data_input[0][6] * 100))
    plt.plot(h2_2, x_2, label = "Constant %.2f %% CO2" %(data_input[3][6] * 100))
    plt.plot(h2_3, x_3, label = "Constant %.2f %% CO2" %(data_input[6][6] * 100))
    plt.xlabel("Percent Hydrogen")
    plt.ylabel("Conversion of CO2")
    plt.legend()
    plt.title("Conversion as a function of H2 at %d K" %data_input[counter * num_points][0])
    plt.show()

    counter +=1

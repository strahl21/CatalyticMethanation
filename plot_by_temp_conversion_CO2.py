import numpy as np
import matplotlib.pyplot as plt

data_input = np.genfromtxt("allparameters_conv_plot2.csv", skip_header = True, delimiter = ',')

num_temperatures = 4
num_points = 8
counter = 0
for i in range(num_temperatures):
    x_1 = data_input[(5 + counter * num_points) : (counter * num_points + 8), 4]
    co2_1 = data_input[(5 + counter * num_points) : (counter * num_points + 8), -2]
    plt.plot(co2_1, x_1, label = "%d K" %(data_input[counter * num_points][0]))
    plt.scatter(co2_1, x_1, marker='+', s=100)

    #plt.plot(h2_2, x_2, label = "Constant %.2f %% CO2" %(data_input[3][6] * 100))
    #plt.plot(h2_3, x_3, label = "Constant %.2f %% CO2" %(data_input[6][6] * 100))

    counter +=1

plt.xlabel("Percent CO2")
plt.ylabel("Conversion of CO2")
plt.legend()
plt.title("Conversion dependency on CO2 at 20 % constant H2")
plt.show()

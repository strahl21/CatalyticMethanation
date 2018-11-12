import numpy as np
import matplotlib.pyplot as plt

data_input = np.genfromtxt("allparameters_conv_plot.csv", skip_header = True, delimiter = ',')

num_temperatures = 4
num_points = 8
counter = 0
for i in range(num_temperatures):
    x_1 = data_input[(counter * num_points) : (counter * num_points + 3), 4]
    co2_1 = data_input[(counter * num_points) : (counter * num_points + 3), -1]
    plt.plot(co2_1, x_1, label = "%d K" %(data_input[counter * num_points][0]))
    plt.scatter(co2_1, x_1, marker='+', s=100)

    counter +=1

plt.xlabel("Percent H2")
plt.ylabel("Conversion of CO2")
plt.legend()
plt.title("Conversion dependency on H2 at 1% constant CO2")
plt.show()

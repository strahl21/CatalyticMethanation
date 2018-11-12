import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("Temp_alpha_beta2.csv", skip_header = True, delimiter = ',')

plt.plot(data[:,0], data[:,1], label = "alpha")
plt.scatter(data[:,0], data[:,1], marker = '+', s = 100)
plt.xlabel("Temperature C")
plt.ylabel("Power law value")
plt.title("Power law alpha vs. T")
plt.legend()
plt.show()

plt.plot(data[:,0], data[:,2], label = "beta")
plt.scatter(data[:,0], data[:,2], marker = '+', s = 100)
plt.xlabel("Temperature C")
plt.ylabel("Power law value")
plt.legend()
plt.title("Power law beta vs. T")
plt.show()

import numpy as np
import matplotlib.pyplot as plt

def rate_constant(E_a, A, T):
    R = 8.3145
    return A * np.exp(-E_a / (R * T))

temperature_range = np.linspace(250 + 273.15, 325 + 273.15, 100)
temperature_range = np.array([250, 270, 285, 300, 325])
for i in range(len(temperature_range)):
    temperature_range[i] += 273.15

E_a_high2 = 0.746652e5
E_a_high1 = 0.797136e5
#E_a_high1 = 0.802627e5
E_a_low = 0.787688e5
A_high2 = 0.060046e8
A_high1 = 0.058322e8
A_low = 0.043299e8


curve = np.zeros(len(temperature_range))
slopes = np.zeros(len(temperature_range))

for i in range(len(curve)):
    if temperature_range[i] >= 285 + 273.15 and temperature_range[i] < 300 + 273.15:
        activation_energy = E_a_high1
        pre_exponential = A_high1
    elif temperature_range[i] >= 300 + 273.15:
        activation_energy = E_a_high2
        pre_exponential = A_high2
    else:
        activation_energy = E_a_low
        pre_exponential = A_low
    curve[i] = rate_constant(activation_energy, pre_exponential, temperature_range[i])
    slopes[i] = rate_constant(activation_energy, pre_exponential, temperature_range[i]) / activation_energy

temp_plot = 1 / temperature_range
rate_plot = np.log(curve)

#temp_plot = temperature_range
#rate_plot = slopes

plt.scatter(temp_plot, rate_plot)
plt.xlabel("${\\frac{1}{T}}$")
plt.ylabel("$ln(k)$")
plt.title("$ln(k)  vs.  \\frac{1}{T}$")
plt.xlim([0.00165, 0.002])
plt.show()

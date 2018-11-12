import numpy as np
from scipy.optimize import fsolve

def FT(X_CO2, F_CO2_0):
    FT0 = 1.49E-04
    d = 2
    c = 1
    b = 4
    a = 1
    return FT0 + (d / a + c / a - b / a - 1) * F_CO2_0 * X_CO2

def solve_xco2(X_CO2, F_CO2_0, area_ch4):
    equations = np.zeros(1)
    lhs = area_ch4 * (0.04 / 1347.4) * FT(X_CO2, F_CO2_0) / F_CO2_0
    rhs = X_CO2
    equations[0] = lhs - rhs
    return equations

def getConversion(CO2_init, area_ch4):
    guess = .1
    conversion = fsolve(solve_xco2, guess, args = (CO2_init, area_ch4,))
    return conversion
# in moles
CO2_2sccm = 1.49E-06
CO2_5sccm = 3.725E-06
CO2_8sccm = 5.96E-06
CO2_init = [CO2_2sccm, CO2_2sccm, CO2_2sccm, CO2_5sccm, CO2_5sccm, CO2_5sccm, \
            CO2_8sccm, CO2_8sccm]
CO2_init = [CO2_2sccm, CO2_2sccm, CO2_2sccm, CO2_5sccm, CO2_5sccm, CO2_5sccm]#, \
#            CO2_8sccm, CO2_8sccm]

#area_ch4 = [65.6, 86.7, 106.5, 105.6, 124.7, 139.2, 141.1, 151.4] # 270 C
#area_ch4 = [123.2, 172.5, 202.9, 218.2, 264.6, 297.7, 303, 339.3] # 300 C
#area_ch4 = [85.7, 117.6, 144.3, 147.7, 173.4, 194.2, 201.1, 216.8] # 285 C
#area_ch4 = [152.8, 219.6, 248.5, 309.4, 393.4, 450.2, 468.6, 541.9] # 325 C
area_ch4 = [34.8, 43.5, 53.5, 50.1, 57.9, 62.2]#, 468.6, 541.9] # 250 C


for i in range(len(CO2_init)):
    print(getConversion(CO2_init[i], area_ch4[i])[0])

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 14:51:49 2018

@author: wills
"""

from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import uncertainties as unc
import uncertainties.unumpy as unp

def funcLinear(x, slope, intercept):
    return slope * x + intercept

def predband(x, xd, yd, f_vars, function = funcLinear, conf=0.95):
    alpha = 1. - conf    # Significance
    N = xd.size          # data sample size
    var_n = len(f_vars)  # Number of variables used by the fitted function.

    # Quantile of Student's t distribution for p=(1 - alpha/2)
    q = stats.t.ppf(1. - alpha / 2., N - var_n)

    # Std. deviation of an individual measurement (Bevington, eq. 6.15)
    se = np.sqrt(1. / (N - var_n) * np.sum((yd - function(xd, *f_vars)) ** 2))

    # Auxiliary definitions
    sx = (x - xd.mean()) ** 2
    sxd = np.sum((xd - xd.mean()) ** 2)

    # Predicted values (best-fit model)
    yp = function(x, *f_vars)
    # Prediction band
    dy = q * se * np.sqrt(1. + (1. / N) + (sx / sxd))

    # Upper & lower prediction bands.
    lpb, upb = yp - dy, yp + dy

    return lpb, upb

def linearPredictionBand(dataX, dataY, **kwargs):
    show = kwargs.get('show', True)
    numPoints = kwargs.get('pts', 100)
    alpha = kwargs.get('alpha', 0.95)

    # Read data from file.
    xd = dataX
    yd = dataY

    # Find best fit of data with 3-parameters exponential function.
    popt, pcov = curve_fit(funcLinear, xd, yd)

    slope, intercept = unc.correlated_values(popt, pcov)

    # Generate equi-spaced x values.
    x = np.linspace(xd.min(), xd.max(), numPoints)

    py =  x * slope + intercept

    nom = unp.nominal_values(py)
    std = unp.std_devs(py)

    # Call function to generate lower an upper prediction bands.
    lpb, upb = predband(x, xd, yd, popt, conf=alpha)

    #std = np.zeros(len(std))
    # Plot
    # Plot data.
    plt.scatter(xd, yd)
    # Plot best fit curve.
    conf_int = stats.norm.ppf(1 - (1 - alpha) / 2)
    plt.plot(x, funcLinear(x, *popt), c='r')
    plt.plot(x, nom - conf_int * std, c='c')
    plt.plot(x, nom + conf_int * std, c='c')
    # Prediction band (upper)
    plt.plot(x, upb, c='g')
    # Prediction band (lower)
    plt.plot(x, lpb, c='g')
    #plt.plot(x, nom - 2 * std, 'c')
    #plt.plot(x, nom + 2 * std,'c')
    if show:
        plt.show()
    width = upb - lpb
    avg = np.average(width)

    return

def nonLinearPredictionBand(func, funcUnp, dataX, dataY, **kwargs):
    printValues = kwargs.get('printValues', False)
    lowerBound = kwargs.get('lb', dataX[0])
    upperBound = kwargs.get('ub', dataX[-1])
    confIntervalPoints = kwargs.get('pts', 100)
    show = kwargs.get('show', True)
    name = kwargs.get('name', "Nonlinear_Prediction_Band")
    save = kwargs.get('save', False)
    alpha = kwargs.get('alpha', 0.95)
    args = kwargs.get('args', ())


    numPoints = len(dataX)
    popt, pcov = curve_fit(func, dataX, dataY)

    if printValues:
        for i in range(len(popt)):
            print("Optimal parameter ", i + 1, ": ", popt[i])

    argTuple = ()
    for i in popt:
        argTuple += (i,)

    r2 = 1.0 - (sum((dataY - func(dataX, *argTuple)) **2 ) / ((numPoints - 1.0) * np.var(dataY , ddof=1)))
    if printValues:
        print("R Squared = ", r2)

    uncertainties = unc.correlated_values(popt, pcov)
    if printValues:
        for i in range(len(uncertainties)):
            print("Uncertainy parameter ", i + 1, ": ", uncertainties[i])

    # calculate regression confidence interval
    px = np.linspace(lowerBound, upperBound, confIntervalPoints)
    py = funcUnp(px, *uncertainties)
    nom = unp.nominal_values(py)
    std = unp.std_devs(py)

    lpb, upb = predband(px, dataX, dataY, popt, function=func, conf=alpha)


    plt.scatter(dataX, dataY, s=3, label='Data')
    # plot the regression
    plt.plot(px, nom, c='black', label='fit')

    # uncertainty lines (95% confidence)
    conf_int = stats.norm.ppf(1 - (1 - alpha) / 2)
    percent_conf = str(alpha * 100) + '% Confidence Region'
    plt.plot(px, nom - conf_int * std, c='orange',\
             label=percent_conf)
    plt.plot(px, nom + conf_int * std, c='orange')
    # prediction band (95% confidence)

    plt.plot(px, lpb, 'k--',label=percent_conf)
    plt.plot(px, upb, 'k--')
    plt.ylabel('y')
    plt.xlabel('x')
    plt.legend(loc='best')
    if save:
        name += ".png"
        plt.savefig(name)

    if show:
        plt.show()

    return

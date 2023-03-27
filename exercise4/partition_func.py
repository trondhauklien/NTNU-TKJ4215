import numpy as np
from math import factorial, sqrt, exp, log
import matplotlib.pyplot as plt
import pickle


def calculate_Q_exact(m_AB, temp_inv):
    """
    Calculates the partition function as a sum of a list with Boltzmann factors.
    Given is a list with AB-bonds, m_AB, providing the energy (a minus sign difference)
    and the inverse of the temperature, temp_inv. The Boltzmann constant is here set to 1.
    """
    return sum([exp(-m * temp_inv) for m in m_AB])


def calculate_Q_approx(n, temp):
    """
    Calculates the partition function using the Bragg-Williams approximation
    Gives the number of particles, n, and the temperature, temp.
    Get the multiplicity (not from Stirling's approximation!)
    Returns ln Q
    """
    return -sum([log(i) for i in range(1, n + 1)]) - log(2) + n / temp


def partition_function_plot(m_AB, n):
    """
    Generates plots with the partition function.
    Given is a list with AB-bonds, m_AB, providing the energy (a minus sign difference)
    and the number of particles, n.
    """
    temps = np.linspace(1, 10, 100)  # Temperature range to be plotted. High resolution
    Q_exact_list = []
    Q_approx_list = []
    Q_ratio = []
    # The for loop calculates and appends Q(T)
    for temp in temps:
        Q_exact = calculate_Q_exact(m_AB, 1.0 / temp)
        Q_approx = calculate_Q_approx(n, temp)
        Q_exact_list.append(log(Q_exact))
        Q_approx_list.append(Q_approx)
        Q_ratio.append(log(Q_exact) / Q_approx)
    # Makes and saves plots
    plt.plot(temps, Q_exact_list)
    plt.plot(temps, Q_approx_list)
    plt.legend(["ln Q_exact", "ln Q_approx"], loc="upper left")
    plt.savefig("partition_function")
    plt.close()
    plt.plot(temps, Q_ratio)
    plt.legend(["Q_ratio"], loc="upper left")
    plt.savefig("partition_function_ratio")
    plt.close()


with open("m_AB.pkl", "rb") as f:  # Opens microstate list
    m_AB, n = pickle.load(f)  # and creates variables m_AB (list) and N (system size)

partition_function_plot(m_AB, n)

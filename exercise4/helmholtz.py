import numpy as np
from math import factorial, sqrt, exp, log
import matplotlib.pyplot as plt
import pickle

def calculate_F(m_AB):
    """
    Plots the Helmholtz free energy as a function of the energy for different temperatures.
    Given is a list of microstates, m_AB
    """
    macrostates = sorted(list(set(m_AB))) # Get macrosteps. Sorts list in ascending order
    # Obtain a list of degeneracies (same as in Task 1)
    degeneracies = [m_AB.count(macrostate) for macrostate in macrostates]
    temperatures = np.linspace(0,10,10) # the temperature range 
    for temp in temperatures:
        # Calculate a list with free energies. Use list comprehension. Hint: use zip(macrostates, degeneracies) as iterator
        free_energies = [-24 - temp *  log(macrostates * degeneracies) for macrostates, degeneracies in zip(macrostates, degeneracies)]
        plt.plot(macrostates, free_energies, label=f"{temp} K")
    plt.legend()
    plt.xlabel("Macrostate, AB-interactions")
    plt.ylabel("Free energy")
    plt.savefig('helmholtz_free_energy') #Saves plot as Helmholtz_free_energy.png
    plt.close()

with open('m_AB.pkl', 'rb') as f: # Loads microstate list
    m_AB = pickle.load(f)[0]
calculate_F(m_AB)

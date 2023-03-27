# %%
import numpy as np
from sympy.utilities.iterables import multiset_permutations
import matplotlib.pyplot as plt
import seaborn as sns
from math import factorial, log
import time
import pickle
import itertools
from numba import njit

# %% [markdown]
# # Exerxise 4
# 
# Trond Hauklien
# TKJ4215 Statistical Thermodynamics in Chemistry and Biology
# 
# Date: 24.03.2023

# %% [markdown]
# Task 1

# %%
@njit(parallel=True)
def count_AB(lattice, lattice_shape): 
    """
    Returns the number of AB-interactions, n_AB, for a provided lattice.
    Uses periodic boundary conditions.
    """
    
    n_AB = 0 
    for coord, particle in np.ndenumerate(lattice):
        if particle == 'A': #Prevents double counting
            # loop over the number of possible neighbours
            for incr in [(1,0),(0,-1),(-1,0),(0,1)]: # neighbour increments
                # The modulo operation ensures that periodic boundary conditions are employed
                # neighbour needs to be a tuple

                neighbour = np.mod(np.array(coord) + np.array(incr), np.array(lattice_shape))
                if lattice[(neighbour[0], neighbour[1])] == 'B': #Checks if AB-interaction
                    n_AB += 1 
    return n_AB

# %% [markdown]
# Assuming n is even and the lattice is saturated with no vacancies.

# %%
def create_arrays_and_count(n, shape): 
    """
    Given the number of molecules/lattice points, n, and returns a list with the number of AB interactions for all microstates, m_AB.
    A condition is that the number of A and B molecules is equal.
    """
    m_AB = [] 
    for config in multiset_permutations(int(n/2)*'AB'):
        lattice = np.array(config).reshape(shape)
        m_AB.append(count_AB(lattice, shape))
    return m_AB

# %%
shapes = {4:(2,2), 6:(2,3), 8:(2,4), 12:(3,4), 16:(4,4), 20:(5,4)}#, 24:(6,4)}

for key in shapes: # The system sizes, shorten the list while testing 
    m_AB = create_arrays_and_count(key, shapes[key]) 
    macrostates = sorted(list(set(m_AB))) # Sorts the macrostates list in ascending order
    # Find degeneracies by counting the number of times a certain number of bonds appear in m_AB
    degeneracies = [m_AB.count(macrostate) for macrostate in macrostates]
    #Plots bar chart
    y_pos = np.arange(len(macrostates))
    print(y_pos)
    plt.bar(y_pos, degeneracies)
    plt.xticks(y_pos, macrostates, fontsize=7, rotation=30)
    plt.savefig('density_of_states' + str(key))
    plt.clf()
    #Calculates the variance of the microstate list. The variance decreases as system size increases
    normalization_factor = max(m_AB) # The interaction energies are normalized
    normalized_mAB = [round(norm/normalization_factor, 2) for norm in m_AB] #Performs normalization
    print('%i particles:\nVariance: %6.4f\n' % (key, np.var(normalized_mAB))) #Prints variance
    

# %%




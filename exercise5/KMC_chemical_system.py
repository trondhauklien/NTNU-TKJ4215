from random import uniform  # will be used to pick random numbers between 0 and 1
from math import log
import matplotlib.pyplot as plt  # Will be used to create the relevant plots

# Part 1
n_a = 1e4
n_b = 1.3e4
n_c = 1e3

k_f = 0.05
k_r = 0.05


def probability_forward(k_f, k_r, n_a, n_b, n_c):
    """
    Calculates the probability of a forward transition. The reverse probability is 1 - forward.
    """
    # n = c because V = 1
    r_f = k_f * n_a * n_b
    r_r = k_r * n_c
    return r_f / (r_f + r_r)


# Part 2
num_trans = 1e5
equilibrium = False  # Sets up equilibrium check
n_a_time = [
    n_a
]  # Inititates a list with number of A particles at each time step; for plotting
n_b_time = [
    n_b
]  # Inititates a list with number of B particles at each time step; for plotting
n_c_time = [
    n_c
]  # Inititates a list with number of C particles at each time step; for plotting
time_step = [
    0
]  # Sets up a list with the time passed after each transition; for plotting
while not equilibrium:
    if uniform(0, 1) < probability_forward(
        k_f, k_r, n_a_time[-1], n_b_time[-1], n_c_time[-1]
    ):
        # Forward reaction
        n_b_time.append(n_b_time[-1] - 1)
        n_c_time.append(n_c_time[-1] + 1)
        n_a_time.append(n_a_time[-1] - 1)
    else:
        # Reverse reaction
        n_b_time.append(n_b_time[-1] + 1)
        n_c_time.append(n_c_time[-1] - 1)
        n_a_time.append(n_a_time[-1] + 1)
    time_step.append(time_step[-1] - log(uniform(0, 1)) / (k_f * n_a * n_b + k_r * n_c))

    if (
        n_a_time[-1] * n_b_time[-1] > 0
        and n_c_time[-1] / (n_a_time[-1] * n_b_time[-1]) == k_f / k_r
    ):
        equilibrium = True

    if len(time_step) > num_trans:
        equilibrium = True
    # Use uniform(0,1) (generates random number) to select either forward or reverse reaction
    # Use incr = ... int(uniform(0,1)) ... to get an increment as +1 or -1 for updating the number of A, B and C particles
    # Update the number of particles for A, B and C
    # Update the lists for plotting.
    # Check the equilibrium condition to see if it has been reached

# Part 3
# Show plot of number of each particle as a function of time. plt.plot(x-axis, y-axis, color)
plt.plot(time_step, n_a_time, "r")
plt.plot(time_step, n_b_time, "b")
plt.plot(time_step, n_c_time, "g")
plt.show()

from numpy import zeros
from random import choice, uniform, shuffle
import matplotlib.pyplot as plt
from math import log, factorial, lgamma
import imageio
import os
from pathlib import Path

base_path = Path(__file__).parent.__str__()

row = 100  # row and col are the dimension of the lattice
col = 200
n = 50  # number of particles
num_steps = int(3e4)  # number of simulation steps
dump_interval = int(num_steps/10)  # should be around 1/10 of num_steps, a bad choice (too frequent) can make the calculation very slow
filenames=[]

def initialize(row, col, n):
    """
    Put all the particles on for example the left-hand side
    """
    assert n <= row * col  # Check that there is enough space for all the particles
    p_list = []
    i, j = 0, 0
    for p in range(n):
        if i >= row:
            i = 0
            j += 1
        p_list.append((i, j))
        i += 1
    return p_list


def possible_transitions(positions_of_particles):
    """
    Calculate the possible transitions from the positions
    """
    shuffle(positions_of_particles)
    incr = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for p_pos in positions_of_particles:
        potential_transitions = []
        for inc in incr:
            new_pos = (p_pos[0] + inc[0], p_pos[1] + inc[1])
            if (
                new_pos[0] >= 0
                and new_pos[0] < row
                and new_pos[1] >= 0
                and new_pos[1] < col
                and new_pos not in positions_of_particles
            ):
                potential_transitions.append(new_pos)
        yield (
            p_pos,
            potential_transitions,
        )  # yield is a generator, it returns a value and then continues from where it left off. You can use it in a for-loop.


def perform_transition(positions_of_particles):
    """
    Choose a random transition and update the positions
    """
    for p_pos, potential_transitions in possible_transitions(positions_of_particles):
        while potential_transitions:
            new_pos = choice(potential_transitions)
            potential_transitions.remove(new_pos)
            if new_pos not in positions_of_particles:
                positions_of_particles.remove(p_pos)
                positions_of_particles.append(new_pos)
                break
    return


def entropy_calc(positions_of_particles, n):
    """
    Use the min and max functions to obtain "lattice_spread"
    """
    height = (
        max([p[0] for p in positions_of_particles])
        - min([p[0] for p in positions_of_particles])
        + 1
    )
    width = (
        max([p[1] for p in positions_of_particles])
        - min([p[1] for p in positions_of_particles])
        + 1
    )
    return lgamma(row * col + 1) - (lgamma(n + 1) + lgamma(width * height - n + 1))


entropy_calc(initialize(row, col, n), n)


def create_image(positions_of_particles, tr_num):
    """
    tr_num is the actual simulation step
    """
    current_state = zeros((row, col))
    for p in positions_of_particles:
        current_state[p] = 1
    plt.imshow(current_state, cmap="binary")
    plt.title("Simulation step: " + str(tr_num))
    filename = base_path + "/lattice" + str(tr_num) + ".png"
    filenames.append(filename)
    plt.savefig(filename)


# Main code starts
p_positions = initialize(row, col, n)
time_step = []
local_entropy = []
time = 0

for tr_num in range(num_steps):
    perform_transition(p_positions)
    time -= log(uniform(0, 1))
    if tr_num % dump_interval == 0 or tr_num == 0:
        create_image(p_positions, tr_num)
        local_entropy.append(entropy_calc(p_positions, n))
        time_step.append(time)

# The code below creates the plots the local entropy as a function of time.
plt.clf()
plt.plot(time_step, local_entropy)
plt.xlabel("Time")
plt.ylabel("Local entropy")
plt.tight_layout()
plt.savefig(base_path + "/local_entropy.png")

frames = []
for filename in filenames:
    frames.append(imageio.imread(filename))

imageio.mimsave(base_path + "/animation.gif", frames, format='GIF', duration=1)

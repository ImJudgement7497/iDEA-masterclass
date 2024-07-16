import numpy as np
from classes import System, SingleBodyState
import itertools
import copy
import pandas as pd
import time

def single_particle_energy(state: SingleBodyState) -> float:
    r"""
    Compute the single particle energy of a single particle state.
    """
    return np.sum(state.up.energies[:] * state.up.occupations[:]) + np.sum(
        state.down.energies[:] * state.down.occupations[:]
    )

def get_occupations(energy_method, s: System, state: SingleBodyState, k: int):
    r'Build an occupation array of a state, with a specified energy method'
    
    # Retrieve energy array
    state.up.energies = energy_method(state.up.energies)
    state.down.energies = energy_method(state.down.energies)

    # print(f"length of up.energies = {len(state.up.energies)}")

    # Calculate the max level of orbitals needed to achieve required state and only use these
    max_level = max(s.up_count,s.down_count) + k
    up_energies = state.up.energies[:max_level]
    down_energies = state.down.energies[:max_level]
    # Calculate all possible combinations of spin indices.
    up_indices = list(itertools.combinations(range(max_level), s.up_count))
    down_indices = list(itertools.combinations(range(max_level), s.down_count))

    # print(up_indices)

    # Construct all possible occupations.
    up_occupations = []
    for up_index in up_indices:
        up_occupation = np.zeros(len(up_energies), dtype=float)
        # print(f"length of up.occupation = {len(up_occupation)}")
        np.put(up_occupation, up_index, [1.0] * s.up_count)
        # print(up_occupation)
        up_occupations.append(up_occupation)
    down_occupations = []
    for down_index in down_indices:
        down_occupation = np.zeros(len(down_energies), dtype=float)
        np.put(down_occupation, down_index, [1.0] * s.down_count)
        # print(down_occupation)
        down_occupations.append(down_occupation)
    occupations = list(itertools.product(up_occupations, down_occupations))

    # Calculate the energies of all possible occpuations.

    energies = []
    for occupation in occupations:
        state_copy = copy.deepcopy(state)
        state_copy.up.occupations = np.zeros(len(state_copy.up.energies))
        state_copy.up.occupations[:max_level] = occupation[0]
        # print(f"length of up.occupations[:max_level] = {len(state_copy.up.occupations[:max_level])}")
        state_copy.down.occupations = np.zeros(len(state_copy.down.energies))
        state_copy.down.occupations[:max_level] = occupation[1]
        E = single_particle_energy(state_copy) # used to be taken from iDEA
        energies.append(E)

    # Choose the correct energy index.
    energy_index_arr = np.argsort(energies,kind='stable')
    # print(f"length of energy array = {len(energy_index_arr)}")
    energy_index = energy_index_arr[k]

    # Construct correct occupations.
    state.up.occupations = np.zeros(len(state_copy.up.energies))
    state.up.occupations[:max_level] = occupations[energy_index][0]
    state.up.occupied = np.nonzero(state.up.occupations)[0]
    state.down.occupations = np.zeros(len(state_copy.down.energies))
    state.down.occupations[:max_level] = occupations[energy_index][1]
    state.down.occupied = np.nonzero(state.down.occupations)[0]

    return state

def show_indices(energy_method, s: System, state: SingleBodyState, max_k):
    start = time.perf_counter()
    summary = []
    for i in range(max_k):
        t = get_occupations(energy_method, s, state, i)

        current_energy = single_particle_energy(t)
        current_up = t.up.occupied
        current_down = t.down.occupied

        summary.append([current_up, current_down, current_energy])
    
    df = pd.DataFrame(summary, columns=["Up index", "Down index", "Energy"])
    print(df)
    end = time.perf_counter()
    print(f"Elapsed = {end-start}")
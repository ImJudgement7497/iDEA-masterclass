import numpy as np
from multiplet_classes import CollectionOfStates
import itertools
import pickle
import os
import time
import iDEA

def create_indices(max_level: int):
    file_path = f"indices_up_to_{max_level}.pkl"
    text_path = "max_level.txt"

    # Check if the pickle file for the current max_level exists
    if os.path.exists(file_path):
        print(f"File {file_path} exists")
        with open(file_path, "rb") as file:
            return pickle.load(file)
    # Check if the max_level text file exists
    elif os.path.exists(text_path):
        with open(text_path, "r") as file:
            prev_max_level = int(file.read())
        
        # If current max_level is greater than the previous max level, delete the previous file
        if max_level > prev_max_level:
            prev_file_path = f"indices_up_to_{prev_max_level}.pkl"
            if os.path.exists(prev_file_path):
                print(f"Deleting old file {prev_file_path}")
                os.remove(prev_file_path)
        # If current max_level is less than or equal to the previous max level, use the previous indices
        elif max_level <= prev_max_level:
            prev_file_path = f"indices_up_to_{prev_max_level}.pkl"
            if os.path.exists(prev_file_path):
                print(f"Using indices_up_to_{prev_max_level}.pkl")
                with open(prev_file_path, "rb") as file:
                    return pickle.load(file)

    # If neither file exists, create a new indices file
    print(f"The file {file_path} does not exist. Creating it now")
    index = list(itertools.combinations(range(max_level), 1))
    indices = list(itertools.product(index, index))

    with open(file_path, "wb") as file:
        pickle.dump(indices, file)

    with open(text_path, "w") as file:
        file.write(f"{max_level}")
    
    return indices


def calculate_energy(energy_method, s: iDEA.system.System, max_k: int, max_index=20) -> CollectionOfStates:
    r"""
    Calculate the energy of non-interacting states and the occupation of each state

    Args:

    | energy_method: function, The analytic energy of state k
    | s: iDEA.system.System, The system (only needed for up_count, down_count)
    | max_k: int, Maximum state k considered
    | max_index: int, Maximmum index for indices list (can access upto (max_indes)^2 states), defaulted to 20

    Returns:

    | states: CollectionOfStates
    """
    start = time.perf_counter()

    if (max_index)**2 < max_k:
        raise AssertionError(f"Only {max_index**2} states will be accessed, please decrease the number of states from {max_k} or increase the max index {max_index}")

    states = CollectionOfStates(max_k)
    
    indices = create_indices(max_index)
    indices = np.array(indices).reshape(-1, 2)  

    if s.up_count == 2 or s.down_count == 2:
        mask = indices[:, 0] != indices[:, 1]
        indices = indices[mask]

    
    # Extract up and down indices
    up_indices = indices[:, 0]
    down_indices = indices[:, 1]
    
    # Compute energies
    up_energies = np.vectorize(energy_method)(up_indices)
    down_energies = np.vectorize(energy_method)(down_indices)
    energies = up_energies + down_energies
    
    # Sort and select top k energies
    energy_indices = np.argsort(energies, kind='stable')[:max_k]
    
    # # Create summary DataFrame
    # summary = np.zeros((max_k, 3))
    # summary[:, 0] = up_indices[energy_indices]
    # summary[:, 1] = down_indices[energy_indices]
    # summary[:, 2] = energies[energy_indices]
    
    # df = pd.DataFrame(summary, columns=["Up index", "Down index", "Energy"])
    
    # print(df)
    states.states = np.arange(max_k)
    states.up_indices = up_indices[energy_indices]
    states.down_indices = down_indices[energy_indices]
    states.energies = energies[energy_indices]

    end = time.perf_counter()
    print(f"Elapsed Time = {end-start}")

    return states

def calculate_multiplets(states: CollectionOfStates, tol=1e-12):

    states.multiplets = []

    energies_int = states.energies
    j = 0

    while j < len(energies_int):
        multiplet = []
        if j > 0 and np.abs(energies_int[j] - energies_int[j-1]) <= tol:
            # states.addMultiplet(j-1)
            # states.addMultiplet(j)
            states.add_multiplet_energy(energies_int[j])
            multiplet.append(j-1)
            multiplet.append(j)
            i = j + 1
            while i < len(energies_int):
                if np.abs(energies_int[i] - energies_int[i-1]) <= tol:
                    # states.addMultiplet(i)
                    multiplet.append(i)
                    i += 1
                else:
                    states.add_multiplet(multiplet)
                    break
            j = i 
        else:
            j += 1
    
    return states
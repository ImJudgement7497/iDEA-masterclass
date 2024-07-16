import numpy as np
import iDEA
import pickle
import time
import os

# Directory to save state files
states_dir = "states"
if not os.path.exists(states_dir):
    os.makedirs(states_dir)
    print(f"Directory {states_dir} created.")
else:
    print(f"Directory {states_dir} already exists.")

absolute_path = os.path.abspath(states_dir)
print(f"Path of newly created directory: {absolute_path}")

# Run variables
points = 231
start_num_of_states = 0
end_num_of_states = 10

# Initialize the system
l = 10
x = np.linspace(-l, l, points)
dx = x[1] - x[0]
omega = 0.3275
v_ext = 0.5 * omega**2 * (x**2)
v_int = np.zeros([len(x), len(x)])
qho_single = iDEA.system.System(x, v_ext, v_int, electrons="u")
qho_double = iDEA.system.System(x, v_ext, v_int, electrons="ud")

# Initialize the arrays
occupied_info = {}
time_array_text = []
time_array_num = []

# Solve for the state and extract the energy
for i in range(start_num_of_states, end_num_of_states):
    start_time = time.perf_counter()
    print(f"Start state {i}")
    orbital_energy = []

    try:
        # Methods using qho_single
        s = iDEA.methods.interacting.solve(qho_single, k=i)
        state_file_name = f"qho_single_state_{i}_{points}_points.pkl"
        filepath = os.path.join(states_dir, state_file_name)
        with open(filepath, "wb") as file:
            pickle.dump(s, file)
        print(f"Saved {state_file_name}")

        # Methods using qho_double
        j = iDEA.methods.interacting.solve(qho_double, k=i)
        state_file_name = f"qho_double_state_{i}_{points}_points.pkl"
        filepath = os.path.join(states_dir, state_file_name)
        with open(filepath, "wb") as file:
            pickle.dump(j, file)
        print(f"Saved {state_file_name}")

        t = iDEA.methods.non_interacting.solve(qho_double, k=i)
        energies_up = t.up.energies  # Energies of single body state
        energies_down = t.down.energies
        up_occ_index = t.up.occupied  # Index of occupied orbitals
        down_occ_index = t.down.occupied

        for index in up_occ_index:
            orbital_energy.append(energies_up[index])

        for index in down_occ_index:
            orbital_energy.append(energies_down[index])

        energy_sum = np.sum(orbital_energy)

        occupied_info[i] = [up_occ_index, down_occ_index, orbital_energy, energy_sum]
        
        print(f"End state {i} done")
    except Exception as e:
        print(f"An error occurred for state {i}: {e}")

    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(f"Run time for state {i} = {run_time} s")
    time_array_text.append(f"Run time for state {i} = {run_time} s\n")
    time_array_num.append(run_time)

print("Done")

total_time = np.sum(time_array_num)

with open('timings.txt', 'w') as file:
    # Write each line to the file
    for line in time_array_text:
        file.write(line)
    file.write(f"Total runtime: {total_time} s\n")
print("Saved timings.txt")

file_name_5 = f"occupied_info_{points}.pkl"

with open(file_name_5, "wb") as file:
    pickle.dump(occupied_info, file)
print(f"Saved {file_name_5}")

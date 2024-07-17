import numpy as np
import matplotlib.pyplot as plt
import iDEA
import pickle
import time

# run variables

points = ?
num_of_states = 10

# initalise the system

l = 5
x = np.linspace(0, l, points)
dx = x[1] - x[0]
v_ext = np.zeros(len(x))
v_int = np.zeros([len(x), len(x)])
pib_single = iDEA.system.System(x, v_ext, v_int, electrons = "u")
pib_double = iDEA.system.System(x, v_ext, v_int, electrons = "ud")

# initalise the arrays

energies_int = []
energies_single = []
energies_errors = []
occupied_levels = {}
occupied_info = {}
time_array_text = []
time_array_num = []

# solve for the state and extract the energy
for i in range(num_of_states):
    start_time = time.perf_counter()
    print(f"Start state {i}")
    orbital_energy = []
    # methods using pib_single
    s = iDEA.methods.interacting.solve(pib_single, k=i)
    energies_single.append(np.round((s.energy / (np.pi)**2), decimals=4))

    # methods using pib_double
    j = iDEA.methods.interacting.solve(pib_double, k=i)
    state_file_name = f"state{points}_{i}.pkl"
    with open(state_file_name, "wb") as file:
      pickle.dump(j, file)

    energies_int.append(np.round((j.energy / (np.pi)**2), decimals=4))
    
    t = iDEA.methods.non_interacting.solve(pib_double, k=i)
    energies_up = np.round((t.up.energies / ((np.pi)**2)), decimals=4) # energies of single body state
    energies_down = np.round((t.down.energies / ((np.pi)**2)), decimals=4)
    up_occ_index = t.up.occupied # index of occupied orbitals
    down_occ_index = t.down.occupied
    # up_occ = t.up.occupations # full array of occupations
    # down_occ = t.down.occupations

    for index in up_occ_index:
        orbital_energy.append(energies_up[index])

    for index in down_occ_index:
        orbital_energy.append(energies_down[index])

    energy_sum = np.sum(orbital_energy)
    
    occupied_levels[f"State = {i}"] = (f"Orbitals occupied by up: {up_occ_index}", f"Orbitals occupied by down: {down_occ_index}", \
                                       f"Energy of occupied orbitals: {orbital_energy}", f"Total energy = {energy_sum}")
    occupied_info[i] = [up_occ_index, down_occ_index, orbital_energy, energy_sum]
    
    
    # energies_errors.append(abs( ((i+1)**2) / (2*(l**2)) - np.round((s.energy / (np.pi)**2), decimals=4)))
    energies_errors.append(abs( ((i+1)**2) / (2*((l+2*dx)**2)) - np.round((s.energy / (np.pi)**2), decimals=4)))
    print(f"End state {i} done")
    end_time = time.perf_counter()
    print(f"Run time for state {i} = {end_time - start_time} s")
    time_array_text.append(f"Run time for state {i} = {end_time - start_time} s\n")
    time_array_num.append(end_time - start_time)
print("Done")

total_time = np.sum(time_array_num)

with open('timings.txt', 'w') as file:
    # Write each line to the file
    for line in time_array_text:
        file.write(line)
    file.write(f"Total runtime: {total_time} s\n")
file.close()


file_name_1 = f"energies_int_{points}.pkl"
file_name_2 = f"energies_single_{points}.pkl"
file_name_3 = f"energies_errors.{points}.pkl"
file_name_4 = f"occupied_levels.{points}.pkl"
file_name_5 = f"occupied_info_{points}.pkl"

with open(file_name_1, "wb") as file:
    pickle.dump(energies_int, file)

with open(file_name_2, "wb") as file:
    pickle.dump(energies_single, file)

with open(file_name_3, "wb") as file:
    pickle.dump(energies_errors, file)

with open(file_name_4, "wb") as file:
    pickle.dump(occupied_levels, file)

with open(file_name_5, "wb") as file:
    pickle.dump(occupied_info, file)





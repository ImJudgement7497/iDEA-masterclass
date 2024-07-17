import iDEA.methods
import iDEA.methods.non_interacting
import iDEA.observables
import iDEA.system
import numpy as np
import matplotlib.pyplot as plt
import iDEA
import pickle
import time
import os

def compare_methods(small_int_system: iDEA.system.System, no_int_system: iDEA.system.System, start_num_of_states: int, end_num_of_states: int):
    
    energies_small_int = []
    energies_zero_int = []
    energies_non_int = []
    time_array_text = []
    time_array_num = []

    # Ensure the 'states' directory exists
    states_dir = "states"
    if not os.path.exists(states_dir):
        os.makedirs(states_dir)
    
    energy_dir = "energies"
    if not os.path.exists(energy_dir):
        os.makedirs(energy_dir)


    # Solve for the state and extract the energy
    for i in range(start_num_of_states, end_num_of_states):
        start_time = time.perf_counter()
        print(f"Start state {i}")


        # Everything for the small int system

        j = iDEA.methods.interacting.solve(small_int_system, k=i)

        state_file_name = f"qho_small_int_state_{i}_1e-11.pkl"
        filepath = os.path.join(states_dir, state_file_name)
        with open(filepath, "wb") as file:
            pickle.dump(j, file)
            file.close()

        energies_small_int.append(j.energy)
        file_name_1 = f"qho_energies_small_int_{start_num_of_states}_{end_num_of_states-1}.pkl"
        filepath_2 = os.path.join(energy_dir, file_name_1)
        with open(filepath_2, "wb") as file:
            pickle.dump(energies_small_int, file)
            file.close()
        
        # Everything for the no int system (interacting)
        
        j = iDEA.methods.interacting.solve(no_int_system, k=i)

        state_file_name = f"qho_zero_int_state_{i}.pkl"
        filepath = os.path.join(states_dir, state_file_name)
        with open(filepath, "wb") as file:
            pickle.dump(j, file)
            file.close()

        energies_zero_int.append((j.energy))

        file_name_1 = f"qho_energies_zero_int_{start_num_of_states}_{end_num_of_states-1}.pkl"
        filepath_2 = os.path.join(energy_dir, file_name_1)
        with open(filepath_2, "wb") as file:
            pickle.dump(energies_zero_int, file)
            file.close()

        # # Everything for the no int system (non-interacting)
        
        # j = iDEA.methods.non_interacting.solve(no_int_system, k=i)
        # energies_non_int.append((iDEA.observables.single_particle_energy(no_int_system, j)))
        # file_name_2 = f"qho_energies_non_int_{start_num_of_states}_{end_num_of_states-1}.pkl"
        # filepath_3 = os.path.join(energy_dir, file_name_2)
        # with open(filepath_3, "wb") as file:
        #     pickle.dump(energies_non_int, file)
        #     file.close()


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

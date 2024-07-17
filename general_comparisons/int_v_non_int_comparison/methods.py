import iDEA.observables
import iDEA.system
import numpy as np
import matplotlib.pyplot as plt
import iDEA
import pickle
import time


def compare_methods(s: iDEA.system.System, start_num_of_states: int, end_num_of_states: int):

    energies_from_interacting = []
    energies_from_non_interacting = []
    time_array_text = []
    time_array_num = []
    summary = []

    # solve for the state and extract the energy
    for i in range(start_num_of_states, end_num_of_states):
        start_time = time.perf_counter()
        print(f"Start state {i}")

        # j = iDEA.methods.interacting.solve(s, k=i)

        # energies_from_interacting.append((j.energy / (np.pi)**2))
        
        t = iDEA.methods.non_interacting.solve(s, k=i)
        energies_from_non_interacting.append((iDEA.observables.single_particle_energy(s, t)) / (np.pi)**2)
        summary.append(f"State {i} = {t.up.occupied}, {t.down.occupied}")

        # file_name_1 = f"energies_interacting_{start_num_of_states}_{end_num_of_states}.pkl"
        # file_name_2 = f"energies_non_interacting_{start_num_of_states}_{end_num_of_states}.pkl"

        # # with open(file_name_1, "wb") as file:
        # #     pickle.dump(energies_from_interacting, file)
        # #     file.close()

        # with open(file_name_2, "wb") as file:
        #     pickle.dump(energies_from_non_interacting, file)
        #     file.close()

        print(f"End state {i} done")
        end_time = time.perf_counter()
        print(f"Run time for state {i} = {end_time - start_time} s")
        time_array_text.append(f"Run time for state {i} = {end_time - start_time} s\n")
        time_array_num.append(end_time - start_time)
    print("Done")

    for elm in summary:
        print(elm)

    total_time = np.sum(time_array_num)

    with open('timings.txt', 'w') as file:
        # Write each line to the file
        for line in time_array_text:
            file.write(line)
        file.write(f"Total runtime: {total_time} s\n")
    file.close()



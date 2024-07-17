import iDEA
import iDEA.observables
import numpy as np
import pickle
import os

l = 5
points = 750
x = np.linspace(0, l, points)
v_ext = np.zeros(len(x))
v_int = np.zeros([len(x), len(x)])
pib_double = iDEA.system.System(x, v_ext, v_int, electrons = "ud")

script_dir = os.path.dirname(os.path.abspath(__file__))
states = {}

for i in range(10):
    file_path = os.path.join(script_dir, f'state750_{i}.pkl')
    try:
        with open(file_path, "rb") as file:
            states[i] = pickle.load(file)
    except FileNotFoundError:
        print(f"File state_{i}.pkl not found.")
    except Exception as e:
        print(f"An error occurred while loading state_{i}.pkl: {e}")

ground_state = states[0]
n = iDEA.observables.density(pib_double, ground_state)
print(n)
import numpy as np
import iDEA
from methods_template import compare_methods


# run variables

points = 200
start_num_of_states = 0
end_num_of_states = 200

# initalise the system

l = 5
x = np.linspace(0, l, points)
dx = x[1] - x[0]
v_ext = np.zeros(len(x))
v_int = np.zeros([len(x), len(x)])
pib_double = iDEA.system.System(x, v_ext, v_int, electrons = "ud")

compare_methods(pib_double, start_num_of_states, end_num_of_states)


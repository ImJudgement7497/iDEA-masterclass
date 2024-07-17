import iDEA.interactions
import numpy as np
import iDEA
from methods_template import compare_methods


# run variables

# Run variables
points = 231
start_num_of_states = 116
end_num_of_states = 200

# Initialize the system
l = 10
x = np.linspace(-l, l, points)
dx = x[1] - x[0]
omega = 0.3275
v_ext = 0.5 * omega**2 * (x**2)
v_int_1 = np.zeros([len(x), len(x)])
qho_double_no_int = iDEA.system.System(x, v_ext, v_int_1, electrons="ud")
v_int_2 = iDEA.interactions.softened_interaction(x, strength=1e-11)
qho_double_small_int = iDEA.system.System(x, v_ext, v_int_2, electrons="ud")
compare_methods(qho_double_small_int, qho_double_no_int, start_num_of_states, end_num_of_states)


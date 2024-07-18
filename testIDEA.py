import iDEA
import numpy as np
import sys
import collections_iDEA

x = np.linspace(0, 1, 100)
v_int = np.zeros([len(x), len(x)])
v_ext = np.zeros(x.shape)

s = iDEA.system.System(x, v_ext, v_int, electrons="u")

# Initialize the system
points = 231
l = 10
x = np.linspace(-l, l, points)
omega = 0.3275
v_ext = 0.5 * omega**2 * (x**2)
v_int = np.zeros([len(x), len(x)])
qho_double = iDEA.system.System(x, v_ext, v_int, electrons="ud")

def qho_energy(index):
    return omega*(index+0.5)

analytic_collection = collections_iDEA.multiplets.apply_energy_method(qho_energy, qho_double, 50)
analytic_collection.calculate_multiplets()
print(analytic_collection.multiplets)
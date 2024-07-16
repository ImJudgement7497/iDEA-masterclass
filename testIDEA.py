import iDEA
import numpy as np

x = np.linspace(0, 1, 100)
v_int = np.zeros([len(x), len(x)])
v_ext = np.zeros(x.shape)

s = iDEA.system.System(x, v_ext, v_int, electrons="u")

help(iDEA)

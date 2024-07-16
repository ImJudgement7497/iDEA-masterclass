import numpy as np
import copy


class CollectionOfStates():
    r"""
    Collection of key information for non-interacting states

    | states: np.ndarray, Array of states, indexed as states[k], for k excited state
    | up_indices: np.ndarray, Array of the index of up occupied orbitals, indexed as up_indices[k]
    | down_indices: np.ndarray, Array of the index of down occupied orbitals, indexed as down_indices[k]
    | energies: np.ndarray, Array of analytical energies of each state, indexed as energies[k]
    | multiplets: list, List of states that are multiplets
    | multiplets_energies: ist, Energies of the corresponding multiplets
    """

    def __init__(self, max_k: int):
        self.states = np.zeros(max_k)
        self.up_indices = np.zeros(max_k)
        self.down_indices = np.zeros(max_k)
        self.energies = np.zeros(max_k)
        self.multiplets = []
        self.multiplet_energies = []
    
    def add_multiplet(self, multiplet):
        r"""
        Add a multiplet list to self.multiplets
        """
        self.multiplets.append(multiplet)
    
    def add_multiplet_energy(self, multiplet_energy):
        self.multiplet_energies.append(multiplet_energy)
    
    def get_num_of_multiplets(self):
        r"""
        Show the number of multiplets in self.multiplets
        """
        return len(self.multiplets)
    
    def get_deg_of_multiplets(self):
        r"""
        Show the degenracy of each sub-list in self.multiplets
        """
        deg = []
        for multiplet in self.multiplets:
            deg.append(len(multiplet))
        return deg
    
    def check_expected_num_of_multiplets(self, test_multiplets, test_energies, break_first=True):
        r"""
        Tests an array of multiplets against analytic multiplets
        """
        
        if test_multiplets == self.multiplets:
            return True
        else:
            diff_indices = []
            diff_elms = {}
            test_copy = copy.deepcopy(test_multiplets)

            i = 0
            while i < min(len(self.multiplets), len(test_copy)):
                if not np.array_equal(self.multiplets[i], test_copy[i]):
                    diff_indices.append(i)
                    if break_first:
                        break

                    # Attempt to concatenate current and next element in test_copy
                    if i + 1 < len(test_copy):
                        conc = test_copy[i] + test_copy[i+1]
                        if np.array_equal(self.multiplets[i], conc):
                            # Update test_copy to reflect the concatenation
                            test_copy[i] = conc
                            # Remove the next element as it has been merged
                            del test_copy[i+1]
                            # No increment for i since we stay at the same index for the next check
                            continue
                i += 1

            j = 1

            for index in diff_indices:
                diff_elms[j] = (f"Got: {test_multiplets[index]} with energy: {test_energies[index]}", 
                                f"Expected: {self.multiplets[index]}", f"Expected energy: {self.multiplet_energies[index]}")
                j += 1
            
            return diff_elms


# class System:
#     r"""Model system, containing all defining properties."""

#     def __init__(
#         self,
#         x: np.ndarray,
#         v_ext: np.ndarray,
#         v_int: np.ndarray,
#         electrons: str,
#         stencil: int = 13,
#     ):
#         r"""
#         Model system, containing all defining properties.

#         | Args:
#         |     x: np.ndarray, Grid of x values in 1D space.
#         |     v_ext: np.ndarray, External potential on the grid of x values.
#         |     v_int: np.ndarray, Interaction potential on the grid of x values.
#         |     electrons: string, Electrons contained in the system.
#         |     stencil: int, Stencil to use for derivatives on the grid of x values. (default = 13)

#         | Raises:
#         |     AssertionError.
#         """
#         self.__x = x
#         self.__dx = self.x[1] - self.x[0]
#         self.v_ext = v_ext
#         self.v_int = v_int
#         self.__electrons = electrons
#         self.count = len(electrons)
#         self.up_count = electrons.count("u")
#         self.down_count = electrons.count("d")
#         self.stencil = stencil
#         self.check()

#     def check(self):
#         r"""Performs checks on system properties. Raises AssertionError if any check fails."""
#         assert (
#             type(self.x) == np.ndarray
#         ), f"x grid is not of type np.ndarray, got {type(self.x)} instead."
#         assert (
#             type(self.v_ext) == np.ndarray
#         ), f"v_ext is not of type np.ndarray, got {type(self.v_ext)} instead."
#         assert (
#             type(self.v_int) == np.ndarray
#         ), f"v_int is not of type np.ndarray, got {type(self.v_int)} instead."
#         assert (
#             type(self.count) == int
#         ), f"count is not of type int, got {type(self.NE)} instead."
#         assert (
#             len(self.x.shape) == 1
#         ), f"x grid is not a 1D array, got {len(self.x.shape)}D array instead."
#         assert (
#             len(self.v_ext.shape) == 1
#         ), f"v_ext is not a 1D array, got {len(self.v_ext.shape)}D array instead."
#         assert (
#             len(self.v_int.shape) == 2
#         ), f"v_int is not a 2D array, got {len(self.v_int.shape)}D array instead."
#         assert (
#             self.x.shape == self.v_ext.shape
#         ), f"x grid and v_ext arrays are not the same shape, got x.shape = {self.x.shape} and v_ext.shape = {self.v_ext.shape} instead."
#         assert (
#             self.x.shape[0] == self.v_int.shape[0]
#             and self.x.shape[0] == self.v_int.shape[1]
#         ), "v_int is not of the correct shape, got shape {self.v_int.shape} instead."
#         assert self.count >= 0, f"count is not positive."
#         assert set(self.electrons).issubset(
#             set(["u", "d"])
#         ), f"Electrons must have only up or down spin, e.g 'uudd'. Got {self.electrons} instead"
#         assert (
#             self.count == self.up_count + self.down_count
#         ), f"Electrons must obay up_count + down_count = count."
#         assert self.stencil in [
#             3,
#             5,
#             7,
#             9,
#             11,
#             13,
#         ], f"stencil must be one of [3,5,7,9,11,13], got {self.stencil} instead."


#     @property
#     def x(self):
#         return self.__x

#     @x.setter
#     def x(self, value):
#         self.__x = value
#         self.__dx = self.__x[1] - self.__x[0]
#         warnings.warn(
#             "x grid has been changed: dx has been recomputed, please update v_ext and v_int on this grid."
#         )

#     @x.deleter
#     def x(self):
#         del self.__x

#     @property
#     def dx(self):
#         return self.__dx

#     @dx.setter
#     def dx(self, value):
#         raise AttributeError(
#             "cannot set dx directly: set the x grid and dx will be updated automatically."
#         )

#     @dx.deleter
#     def dx(self):
#         del self.__dx

#     @property
#     def electrons(self):
#         return self.__electrons

#     @electrons.setter
#     def electrons(self, value):
#         self.__electrons = value
#         self.count = len(value)
#         self.up_count = value.count("u")
#         self.down_count = value.count("d")

#     @electrons.deleter
#     def electrons(self):
#         del self.__electrons

#     def __str__(self):
#         return f"iDEA.system.System: x = np.array([{self.x[0]:.3f},...,{self.x[-1]:.3f}]), dx = {self.dx:.4f}..., v_ext = np.array([{self.v_ext[0]:.3f},...,{self.v_ext[-1]:.3f}]), electrons = {self.electrons}"
#     r"""Model system, containing all defining properties."""

#     def __init__(
#         self,
#         x: np.ndarray,
#         v_ext: np.ndarray,
#         v_int: np.ndarray,
#         electrons: str,
#         stencil: int = 13,
#     ):
#         r"""
#         Model system, containing all defining properties.

#         | Args:
#         |     x: np.ndarray, Grid of x values in 1D space.
#         |     v_ext: np.ndarray, External potential on the grid of x values.
#         |     v_int: np.ndarray, Interaction potential on the grid of x values.
#         |     electrons: string, Electrons contained in the system.
#         |     stencil: int, Stencil to use for derivatives on the grid of x values. (default = 13)

#         | Raises:
#         |     AssertionError.
#         """
#         self.__x = x
#         self.__dx = self.x[1] - self.x[0]
#         self.v_ext = v_ext
#         self.v_int = v_int
#         self.__electrons = electrons
#         self.count = len(electrons)
#         self.up_count = electrons.count("u")
#         self.down_count = electrons.count("d")
#         self.stencil = stencil
#         self.check()
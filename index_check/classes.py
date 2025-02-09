import numpy as np


class System:
    r"""Model system, containing all defining properties."""

    def __init__(
        self,
        x: np.ndarray,
        v_ext: np.ndarray,
        v_int: np.ndarray,
        electrons: str,
        stencil: int = 13,
    ):
        r"""
        Model system, containing all defining properties.

        | Args:
        |     x: np.ndarray, Grid of x values in 1D space.
        |     v_ext: np.ndarray, External potential on the grid of x values.
        |     v_int: np.ndarray, Interaction potential on the grid of x values.
        |     electrons: string, Electrons contained in the system.
        |     stencil: int, Stencil to use for derivatives on the grid of x values. (default = 13)

        | Raises:
        |     AssertionError.
        """
        self.__x = x
        self.__dx = self.x[1] - self.x[0]
        self.v_ext = v_ext
        self.v_int = v_int
        self.__electrons = electrons
        self.count = len(electrons)
        self.up_count = electrons.count("u")
        self.down_count = electrons.count("d")
        self.stencil = stencil
        self.check()

    def check(self):
        r"""Performs checks on system properties. Raises AssertionError if any check fails."""
        assert (
            type(self.x) == np.ndarray
        ), f"x grid is not of type np.ndarray, got {type(self.x)} instead."
        assert (
            type(self.v_ext) == np.ndarray
        ), f"v_ext is not of type np.ndarray, got {type(self.v_ext)} instead."
        assert (
            type(self.v_int) == np.ndarray
        ), f"v_int is not of type np.ndarray, got {type(self.v_int)} instead."
        assert (
            type(self.count) == int
        ), f"count is not of type int, got {type(self.NE)} instead."
        assert (
            len(self.x.shape) == 1
        ), f"x grid is not a 1D array, got {len(self.x.shape)}D array instead."
        assert (
            len(self.v_ext.shape) == 1
        ), f"v_ext is not a 1D array, got {len(self.v_ext.shape)}D array instead."
        assert (
            len(self.v_int.shape) == 2
        ), f"v_int is not a 2D array, got {len(self.v_int.shape)}D array instead."
        assert (
            self.x.shape == self.v_ext.shape
        ), f"x grid and v_ext arrays are not the same shape, got x.shape = {self.x.shape} and v_ext.shape = {self.v_ext.shape} instead."
        assert (
            self.x.shape[0] == self.v_int.shape[0]
            and self.x.shape[0] == self.v_int.shape[1]
        ), "v_int is not of the correct shape, got shape {self.v_int.shape} instead."
        assert self.count >= 0, f"count is not positive."
        assert set(self.electrons).issubset(
            set(["u", "d"])
        ), f"Electrons must have only up or down spin, e.g 'uudd'. Got {self.electrons} instead"
        assert (
            self.count == self.up_count + self.down_count
        ), f"Electrons must obay up_count + down_count = count."
        assert self.stencil in [
            3,
            5,
            7,
            9,
            11,
            13,
        ], f"stencil must be one of [3,5,7,9,11,13], got {self.stencil} instead."


    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
        self.__dx = self.__x[1] - self.__x[0]
        warnings.warn(
            "x grid has been changed: dx has been recomputed, please update v_ext and v_int on this grid."
        )

    @x.deleter
    def x(self):
        del self.__x

    @property
    def dx(self):
        return self.__dx

    @dx.setter
    def dx(self, value):
        raise AttributeError(
            "cannot set dx directly: set the x grid and dx will be updated automatically."
        )

    @dx.deleter
    def dx(self):
        del self.__dx

    @property
    def electrons(self):
        return self.__electrons

    @electrons.setter
    def electrons(self, value):
        self.__electrons = value
        self.count = len(value)
        self.up_count = value.count("u")
        self.down_count = value.count("d")

    @electrons.deleter
    def electrons(self):
        del self.__electrons

    def __str__(self):
        return f"iDEA.system.System: x = np.array([{self.x[0]:.3f},...,{self.x[-1]:.3f}]), dx = {self.dx:.4f}..., v_ext = np.array([{self.v_ext[0]:.3f},...,{self.v_ext[-1]:.3f}]), electrons = {self.electrons}"
    r"""Model system, containing all defining properties."""

    def __init__(
        self,
        x: np.ndarray,
        v_ext: np.ndarray,
        v_int: np.ndarray,
        electrons: str,
        stencil: int = 13,
    ):
        r"""
        Model system, containing all defining properties.

        | Args:
        |     x: np.ndarray, Grid of x values in 1D space.
        |     v_ext: np.ndarray, External potential on the grid of x values.
        |     v_int: np.ndarray, Interaction potential on the grid of x values.
        |     electrons: string, Electrons contained in the system.
        |     stencil: int, Stencil to use for derivatives on the grid of x values. (default = 13)

        | Raises:
        |     AssertionError.
        """
        self.__x = x
        self.__dx = self.x[1] - self.x[0]
        self.v_ext = v_ext
        self.v_int = v_int
        self.__electrons = electrons
        self.count = len(electrons)
        self.up_count = electrons.count("u")
        self.down_count = electrons.count("d")
        self.stencil = stencil
        self.check()

class Container:

    def __init__(self):
        self.energies = []
        self.orbitals = []
        self.occupations = []
        self.occupied = []


class SingleBodyState():

    r"""
    State of particles in a single-body state.

    This is described by three arrays for each spin channel:

    | up.energies: np.ndarray, Array of single-body energies, indexed as energies[orbital_number].
    | up.orbitals: np.ndarray, Array of single-body orbitals, indexed as orbitals[space,orbital_number].
    | up.occupations: np.ndarray, Array of single-body occupations, indexed as occupations[orbital_number].
    | up.occupied: np.ndarray, Indices of up.occupations that are non-zero, to indicate occupied orbitals.

    | down.energies: np.ndarray, Array of single-body energies, indexed as energies[orbital_number].
    | down.orbitals: np.ndarray, Array of single-body orbitals, indexed as orbitals[space,orbital_number].
    | down.occupations: np.ndarray, Array of single-body occupations, indexed as occupations[orbital_number].
    | down.occupied: np.ndarray, Indices of down.occupations that are non-zero, to indicate occupied orbitals.
    """

    def __init__(self, points):
        self.up = Container()
        self.down = Container()

        self.up.energies = np.zeros(points)
        self.up.orbitals = np.zeros(points)
        self.up.occupations = np.zeros(points)
        self.up.occupied = np.zeros(points)

        self.down.energies = np.zeros(points)
        self.down.orbitals = np.zeros(points)
        self.down.occupations = np.zeros(points)
        self.down.occupied = np.zeros(points)


            
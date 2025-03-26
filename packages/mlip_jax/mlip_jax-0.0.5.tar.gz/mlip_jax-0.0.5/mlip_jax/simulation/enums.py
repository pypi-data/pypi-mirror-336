from enum import Enum


class SimulationType(Enum):
    """Enum for the type of simulation.

    Attributes:
        MD: Molecular Dynamics.
        MINIMIZATION: Energy minimization.
    """

    MD = "md"
    MINIMIZATION = "minimization"


class SimulationBackend(Enum):
    """Enum for the simulation backend.

    Attributes:
        JAX_MD: Simulations with the JAX-MD backend.
        ASE: Simulations with the ASE backend.
    """

    JAX_MD = "jaxmd"
    ASE = "ase"


class TemperatureScheduleMethod(Enum):
    """Enum for the type of temperature schedule.

    Attributes:
        CONSTANT: Constant temperature schedule.
        LINEAR: Linear temperature schedule.
        TRIANGLE: Triangle temperature schedule.
    """

    CONSTANT = "constant"
    LINEAR = "linear"
    TRIANGLE = "triangle"

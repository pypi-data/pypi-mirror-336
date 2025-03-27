import abc
from typing import Callable

import ase

from mlip_jax.models.type_aliases import ModelParameters, ModelPredictorFun
from mlip_jax.simulation.configs.simulation_config import SimulationConfig
from mlip_jax.simulation.state import SimulationState


class SimulationEngine(abc.ABC):
    """Abstract base class of a simulation engine that can be implemented by different
    backends and can, in principle, run many types of
    simulations (e.g., MD or energy minimizations).
    """

    def __init__(self):
        """Constructor.

        Initializes the simulation state and an empty list of loggers.
        """
        self.state = SimulationState()
        self.loggers: list[Callable[[SimulationState], None]] = []

    @abc.abstractmethod
    def init(
        self,
        atoms: ase.Atoms,
        model: ModelPredictorFun,
        model_params: ModelParameters,
        simulation_config: SimulationConfig,
    ) -> None:
        """Initializes the simulation.

        Args:
            atoms: The atoms of the system to simulate.
            model: The MLIP model to use in the simulation.
            model_params: The parameters of the MLIP model.
            simulation_config: The configuration/settings of the simulation.
        """
        pass

    @abc.abstractmethod
    def run(self) -> None:
        """Runs the simulation and populates the simulation state during the run."""
        pass

    def attach_logger(self, logger: Callable[[SimulationState], None]) -> None:
        """Adds a logger to the list of loggers of the simulation engine.

        The logger function must only take in a single argument, the simulation state,
        and it shall not return anything.

        Args:
            logger: The logger to add.
        """
        self.loggers.append(logger)

from pydantic import Field
from typing_extensions import Annotated

from mlip_jax.simulation.configs.simulation_config import (
    SimulationConfig,
    TemperatureScheduleConfig,
)

PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0)]


class ASESimulationConfig(SimulationConfig):
    """Configuration for the ASE-based simulations.

    Also includes the attributes of the parent class
    :class:`~mlip_jax.simulation.configs.simulation_config.SimulationConfig`.

    The config is separated into three blocks: values that
    are used for both MD and minimization, and then the ones used exclusively for MD
    and for minimization, respectively.

    Attributes:
        graph_cutoff_angstrom: The graph cutoff radius in Angstrom used to create the
                               graph representations.
        allowed_atomic_numbers: A set of allowed atomic numbers in the model.
        timestep_fs: The simulation timestep in femtoseconds. The default is
                     1.0.
        temperature_kelvin: The temperature in Kelvin, set to 300 by default. Must be
                            set to ``None`` for energy minimizations.
        friction: Friction coefficient for the simulation. Default is 0.1.
        temperature_schedule_config: The temperature schedule config to use for the
                                   simulation. Default is the constant schedule in
                                   which case ``temperature_kelvin`` will be applied.
        max_force_convergence_threshold: The convergence threshold for minimizations
                                         w.r.t. the sum of the force norms. See the
                                         ASE docs for more information.
    """

    graph_cutoff_angstrom: PositiveFloat
    allowed_atomic_numbers: set[PositiveInt]

    # MD Only
    timestep_fs: PositiveFloat | None = 1.0
    temperature_kelvin: PositiveFloat | None = 300.0
    friction: PositiveFloat | None = 0.1

    # Temperature scheduling for MD
    temperature_schedule_config: TemperatureScheduleConfig = Field(
        default=TemperatureScheduleConfig(temperature=temperature_kelvin)
    )

    # Minimization only
    max_force_convergence_threshold: PositiveFloat | None = None

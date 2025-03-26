from typing import Optional

from pydantic import Field, field_validator, model_validator
from typing_extensions import Annotated, Self

from mlip_jax.simulation.configs.simulation_config import (
    SimulationConfig,
    TemperatureScheduleConfig,
)

PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0)]


class JaxMDSimulationConfig(SimulationConfig):
    """Configuration for the JAX-MD-based simulations.

    Also includes the attributes of the parent class
    :class:`~mlip_jax.simulation.configs.simulation_config.SimulationConfig`.

    The config is separated into three blocks: values that
    are used for both MD and minimization, and then the ones used exclusively for MD
    and for minimization, respectively.

    Attributes:
        num_episodes: Number of episodes to divide the simulation into. Each episode
                      runs in a fully jitted way, and the loggers are only
                      called after each episode.
        graph_cutoff_angstrom: The graph cutoff radius in Angstrom used to create the
                               graph representations.
        allowed_atomic_numbers: A set of allowed atomic numbers in the model.
        timestep_fs: The simulation timestep in femtoseconds. This is also used as the
                     initial timestep in the FIRE minimization algorithm. The default is
                     1.0.
        temperature_kelvin: The temperature in Kelvin, set to 300 by default. Must be
                            set to ``None`` for energy minimizations.
        temperature_schedule_config: The temperature schedule config to use for the
                                 simulation. Default is the constant schedule in
                                 which case ``temperature_kelvin`` will be applied.
    """

    num_episodes: PositiveInt
    graph_cutoff_angstrom: PositiveFloat
    allowed_atomic_numbers: set[PositiveInt]
    timestep_fs: Optional[PositiveFloat] = 1.0

    # MD only
    temperature_kelvin: Optional[PositiveFloat] = 300.0
    temperature_schedule_config: TemperatureScheduleConfig = Field(
        default=TemperatureScheduleConfig(temperature=temperature_kelvin)
    )

    @model_validator(mode="after")
    def validate_num_episodes(self) -> Self:
        if self.num_steps % self.num_episodes > 0:
            raise ValueError("Number of episodes must evenly divide total steps.")
        return self

    @model_validator(mode="after")
    def validate_log_frequency(self) -> Self:
        steps_per_episode = self.num_steps // self.num_episodes
        if steps_per_episode % self.log_frequency > 0:
            raise ValueError("Log frequency must evenly divide steps per episode.")
        return self

    @field_validator("allowed_atomic_numbers")
    @classmethod
    def validate_allowed_atomic_numbers_not_empty(cls, value: set[int]) -> set[int]:
        if len(value) == 0:
            raise ValueError("Allowed atomic numbers set must not be empty.")
        return value

    @field_validator("allowed_atomic_numbers")
    @classmethod
    def validate_maximum_allowed_atomic_number(cls, value: set[int]) -> set[int]:
        if max(value) > 118:
            raise ValueError(
                "Allowed atomic numbers contain values that are too large."
            )
        return value

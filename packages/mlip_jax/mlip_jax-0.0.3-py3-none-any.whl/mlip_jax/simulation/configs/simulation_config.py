import pydantic
from pydantic import Field
from typing_extensions import Annotated

from mlip_jax.simulation.enums import SimulationType, TemperatureScheduleMethod

DEFAULT_EDGE_CAPACITY_MULT = 1.25


PositiveInt = Annotated[int, pydantic.Field(gt=0)]
PositiveFloat = Annotated[float, pydantic.Field(gt=0)]
ThreeDimensionalListWithPositiveFloats = Annotated[
    list[PositiveFloat], pydantic.Field(min_length=3, max_length=3)
]
FloatLargerThanOrEqualToOne = Annotated[float, pydantic.Field(ge=1)]


class SimulationConfig(pydantic.BaseModel):
    """The base configuration that all simulations share.

    It only contains fields that are independent of backend and simulation type.

    Attributes:
        simulation_type: The type of simulation to run, either MD or minimization.
        num_steps: The number of total steps to run. For energy minimizations,
                   this is the maximum number of steps if no convergence reached
                   earlier.
        log_frequency: The logging frequency. This means information about every N-th
                       snapshot is stored in the simulation state available to the
                       loggers (N being the logging frequency). By default, this is 1.
        box: The simulation box. If ``None``, no periodic boundary conditions are
             applied (this is the default). It can be set to either a float or a list
             of three floats, describing the dimensions of the box.
        edge_capacity_multiplier: Factor to multiply the number of edges by to
                                  obtain the edge capacity including padding. Defaults
                                  to 1.25.
    """

    simulation_type: SimulationType
    num_steps: PositiveInt
    log_frequency: PositiveInt = 1
    box: PositiveFloat | ThreeDimensionalListWithPositiveFloats | None = None
    edge_capacity_multiplier: FloatLargerThanOrEqualToOne = DEFAULT_EDGE_CAPACITY_MULT


class TemperatureScheduleConfig(pydantic.BaseModel):
    """The base configuration containing all the possible parameters for the
    temperature schedules.

    Attributes:
        method: The type of temperature schedule to use. Default is constant.
        temperature: The temperature to use for the constant schedule in Kelvin.
        start_temperature: The starting temperature in Kelvin.
            Used for the linear schedule.
        end_temperature: The ending temperature in Kelvin.
            Used for the linear schedule.
        max_temperature: The maximum temperature in Kelvin.
            Used for the triangle schedule.
        min_temperature: The minimum temperature in Kelvin.
            Used for the triangle schedule.
        heating_period: The period for heating the system.
            Measured in number of simulation steps. Used for the triangle schedule.

    """

    method: TemperatureScheduleMethod = Field(
        default=TemperatureScheduleMethod.CONSTANT
    )

    # Constant schedule
    temperature: PositiveFloat | None = None

    # Linear schedule
    start_temperature: PositiveFloat | None = None
    end_temperature: PositiveFloat | None = None

    # Triangle schedule
    max_temperature: PositiveFloat | None = None
    min_temperature: PositiveFloat | None = None
    heating_period: PositiveInt | None = None

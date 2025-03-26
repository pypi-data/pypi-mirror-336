from typing import Optional

import pydantic
from typing_extensions import Annotated

PositiveInt = Annotated[int, pydantic.Field(gt=0)]
EMADecay = Annotated[float, pydantic.Field(gt=0.0, le=1.0)]


class TrainingLoopConfig(pydantic.BaseModel):
    """Pydantic config holding all settings related to the
    :class:`~mlip_jax.training.training_loop.TrainingLoop` class.

    Attributes:
        num_epochs: Number of epoch to run.
        num_gradient_accumulation_steps: Number of gradient steps to accumulate before
                                         taking an optimizer step. Default is 1.
        random_seed: A random seed, by default set to 42.
        ema_decay: The EMA decay rate, by default set to 0.99.
        use_ema_params_for_eval: Whether to use the EMA parameters for evaluation,
                                 set to ``True`` by default.
        eval_num_graphs: Number of validation set graphs to evaluate on. By default,
                         this is set to ``None`` which means to evaluate on
                         all the available graphs.
        run_eval_at_start: Whether to run an evaluation on the validation set before
                           we start the first epoch. By default, it is set to ``True``.
    """

    num_epochs: PositiveInt
    num_gradient_accumulation_steps: PositiveInt = 1
    random_seed: int = 42
    ema_decay: EMADecay = 0.99
    use_ema_params_for_eval: bool = True
    eval_num_graphs: Optional[PositiveInt] = None
    run_eval_at_start: bool = True

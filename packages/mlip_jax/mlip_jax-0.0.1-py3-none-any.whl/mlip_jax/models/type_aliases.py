from typing import Callable, TypeAlias

import jraph
import numpy as np

ModelParameters: TypeAlias = dict[str, dict[str, np.ndarray | dict]]
ModelPredictorFun: TypeAlias = Callable[
    [ModelParameters, jraph.GraphsTuple], dict[str, np.ndarray]
]

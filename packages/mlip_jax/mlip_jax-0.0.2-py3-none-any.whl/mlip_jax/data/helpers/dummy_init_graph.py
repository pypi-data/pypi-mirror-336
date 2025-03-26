import jax
import jraph
import numpy as np

from mlip_jax.data.helpers.graph_definition import GraphEdges, GraphGlobals, GraphNodes


def get_dummy_graph_for_model_init() -> jraph.GraphsTuple:
    """Generates a simple dummy graph that can be used for model initialization.

    Returns:
        The dummy graph.
    """
    return jraph.GraphsTuple(
        nodes=GraphNodes(
            positions=np.zeros((1, 3)),
            forces=np.zeros((1, 3)),
            species=np.array([0]),
        ),
        edges=GraphEdges(shifts=np.zeros((1, 3)), displ_fun=None),
        globals=jax.tree_util.tree_map(
            lambda x: x[None, ...],
            GraphGlobals(
                cell=np.zeros((3, 3)),
                energy=np.array(0.0),
                stress=np.zeros((3, 3)),
                weight=np.asarray(1.0),
            ),
        ),
        receivers=np.array([0]),
        senders=np.array([0]),
        n_edge=np.array([1]),
        n_node=np.array([1]),
    )

from typing import Callable

import e3nn_jax as e3nn
import jax.numpy as jnp
import jraph
import numpy as np
import optax

from mlip_jax.models.type_aliases import ModelParameters

HUBER_LOSS_DEFAULT_DELTA = 0.01


def _safe_divide(x, y):
    return jnp.where(y == 0.0, 0.0, x / y)


def _masked_mean(x, mask):
    return jnp.sum(jnp.dot(mask, x)) / jnp.sum(mask)


def _compute_mae(delta: jnp.ndarray, mask) -> float:
    return _masked_mean(jnp.abs(delta), mask)


def _masked_mean_f(x, mask):
    return jnp.sum(mask[..., jnp.newaxis] * x) / (jnp.sum(mask) * 3)


def _compute_mae_f(delta: jnp.ndarray, mask) -> float:
    return _masked_mean_f(jnp.abs(delta), mask)


def _masked_mean_stress(x, mask):
    return jnp.sum(mask[..., jnp.newaxis, jnp.newaxis] * x) / (jnp.sum(mask) * 9)


def _compute_mae_stress(delta: jnp.ndarray, mask) -> float:
    return _masked_mean_stress(jnp.abs(delta), mask)


def _compute_rel_mae(delta: jnp.ndarray, target_val: jnp.ndarray, mask) -> float:
    target_norm = _masked_mean(jnp.abs(target_val), mask)
    return _masked_mean(jnp.abs(delta), mask) / (target_norm + 1e-30)


def _compute_rel_mae_f(delta: jnp.ndarray, target_val: jnp.ndarray, mask) -> float:
    target_norm = _masked_mean_f(jnp.abs(target_val), mask)
    return _masked_mean_f(jnp.abs(delta), mask) / (target_norm + 1e-30)


def _compute_rel_mae_stress(delta: jnp.ndarray, target_val: jnp.ndarray, mask) -> float:
    target_norm = _masked_mean_stress(jnp.abs(target_val), mask)
    return _masked_mean_stress(jnp.abs(delta), mask) / (target_norm + 1e-30)


def _compute_rmse(delta: jnp.ndarray, mask) -> float:
    return jnp.sqrt(_masked_mean(jnp.square(delta), mask))


def _compute_rmse_f(delta: jnp.ndarray, mask) -> float:
    return jnp.sqrt(_masked_mean_f(jnp.square(delta), mask))


def _compute_rmse_stress(delta: jnp.ndarray, mask) -> float:
    return jnp.sqrt(_masked_mean_stress(jnp.square(delta), mask))


def _compute_rel_rmse(delta: jnp.ndarray, target_val: jnp.ndarray, mask) -> float:
    target_norm = jnp.sqrt(_masked_mean(jnp.square(target_val), mask))
    return jnp.sqrt(_masked_mean(jnp.square(delta), mask)) / (target_norm + 1e-30)


def _compute_rel_rmse_f(delta: jnp.ndarray, target_val: jnp.ndarray, mask) -> float:
    target_norm = jnp.sqrt(_masked_mean_f(jnp.square(target_val), mask))
    return jnp.sqrt(_masked_mean_f(jnp.square(delta), mask)) / (target_norm + 1e-30)


def _compute_rel_rmse_stress(
    delta: jnp.ndarray, target_val: jnp.ndarray, mask
) -> float:
    target_norm = jnp.sqrt(_masked_mean_stress(jnp.square(target_val), mask))
    return jnp.sqrt(_masked_mean_stress(jnp.square(delta), mask)) / (
        target_norm + 1e-30
    )


def _compute_q95(delta: jnp.ndarray) -> float:
    return jnp.percentile(jnp.abs(delta), q=95)


def _sum_nodes_of_the_same_graph(
    graph: jraph.GraphsTuple, node_quantities: jnp.ndarray
) -> jnp.ndarray:
    return e3nn.scatter_sum(node_quantities, nel=graph.n_node)  # [ n_graphs,]


def _compute_adaptive_huber_loss_forces(
    pred: np.ndarray, ref: np.ndarray
) -> np.ndarray:
    deltas = HUBER_LOSS_DEFAULT_DELTA * np.array([1.0, 0.7, 0.4, 0.1])

    cond_1 = jnp.linalg.norm(ref, axis=-1) < 100
    cond_2 = (jnp.linalg.norm(ref, axis=-1) > 100) & (
        jnp.linalg.norm(ref, axis=-1) < 200
    )
    cond_3 = (jnp.linalg.norm(ref, axis=-1) > 200) & (
        jnp.linalg.norm(ref, axis=-1) < 300
    )
    cond_4 = ~(cond_1 | cond_2 | cond_3)

    cond_1 = jnp.stack([cond_1] * 3, axis=1)
    cond_2 = jnp.stack([cond_2] * 3, axis=1)
    cond_3 = jnp.stack([cond_3] * 3, axis=1)
    cond_4 = jnp.stack([cond_4] * 3, axis=1)

    output = jnp.zeros_like(pred)
    output = jnp.where(
        cond_1, optax.losses.huber_loss(pred, ref, delta=deltas[0]), output
    )
    output = jnp.where(
        cond_2, optax.losses.huber_loss(pred, ref, delta=deltas[1]), output
    )
    output = jnp.where(
        cond_3, optax.losses.huber_loss(pred, ref, delta=deltas[2]), output
    )
    output = jnp.where(
        cond_4, optax.losses.huber_loss(pred, ref, delta=deltas[3]), output
    )

    return output


def _mean_squared_error_energy(
    graph: jraph.GraphsTuple, energy_pred: np.ndarray
) -> np.ndarray:
    energy_ref = graph.globals.energy  # [n_graphs, ]
    if energy_ref is None:
        # We null out the loss if the reference energy is not provided
        energy_ref = jnp.zeros_like(energy_pred)
        energy_pred = jnp.zeros_like(energy_pred)
    return graph.globals.weight * jnp.square(
        _safe_divide(energy_ref - energy_pred, graph.n_node)
    )  # [n_graphs, ]


def _huber_loss_energy(graph: jraph.GraphsTuple, energy_pred: np.ndarray) -> np.ndarray:
    energy_ref = graph.globals.energy  # [n_graphs, ]
    if energy_ref is None:
        # We null out the loss if the reference energy is not provided
        energy_ref = jnp.zeros_like(energy_pred)
        energy_pred = jnp.zeros_like(energy_pred)
    return graph.globals.weight * optax.losses.huber_loss(
        _safe_divide(energy_pred, graph.n_node),
        _safe_divide(energy_ref, graph.n_node),
        delta=HUBER_LOSS_DEFAULT_DELTA,
    )  # [n_graphs, ]


def _mean_squared_error_forces(
    graph: jraph.GraphsTuple, forces_pred: np.ndarray
) -> np.ndarray:
    forces_ref = graph.nodes.forces  # [n_nodes, 3]
    if forces_ref is None:
        # We null out the loss if the reference forces are not provided
        forces_ref = jnp.zeros_like(forces_pred)
        forces_pred = jnp.zeros_like(forces_pred)
    return graph.globals.weight * _safe_divide(
        _sum_nodes_of_the_same_graph(
            graph, jnp.mean(jnp.square(forces_ref - forces_pred), axis=1)
        ),
        graph.n_node,
    )  # [n_graphs, ]


def _adaptive_huber_loss_forces(
    graph: jraph.GraphsTuple, forces_pred: np.ndarray
) -> np.ndarray:
    forces_ref = graph.nodes.forces  # [n_nodes, 3]
    if forces_ref is None:
        # We null out the loss if the reference forces are not provided
        forces_ref = jnp.zeros_like(forces_pred)
        forces_pred = jnp.zeros_like(forces_pred)
    return graph.globals.weight * _safe_divide(
        _sum_nodes_of_the_same_graph(
            graph,
            jnp.mean(
                _compute_adaptive_huber_loss_forces(forces_pred, forces_ref),
                axis=1,
            ),
        ),
        graph.n_node,
    )  # [n_graphs, ]


def _mean_squared_error_stress(
    graph: jraph.GraphsTuple, stress_pred: np.ndarray
) -> np.ndarray:
    stress_ref = graph.globals.stress  # [n_graphs, 3, 3]
    if stress_ref is None:
        # We null out the loss if the reference stress is not provided
        stress_ref = jnp.zeros_like(stress_pred)
        stress_pred = jnp.zeros_like(stress_pred)
    return graph.globals.weight * jnp.mean(
        jnp.square(stress_ref - stress_pred), axis=(1, 2)
    )  # [n_graphs, ]


def _huber_loss_stress(graph: jraph.GraphsTuple, stress_pred: np.ndarray) -> np.ndarray:
    stress_ref = graph.globals.stress  # [n_graphs, 3, 3]
    if stress_ref is None:
        # We null out the loss if the reference stress is not provided
        stress_ref = jnp.zeros_like(stress_pred)
        stress_pred = jnp.zeros_like(stress_pred)
    return graph.globals.weight * jnp.mean(
        optax.losses.huber_loss(
            stress_pred,
            stress_ref,
            delta=HUBER_LOSS_DEFAULT_DELTA,
        ),
        axis=(1, 2),
    )  # [n_graphs, ]


def make_weighted_energy_forces_stress_loss(
    energy_weight_schedule: Callable,
    forces_weight_schedule: Callable,
    stress_weight_schedule: Callable,
    use_huber_loss: bool,
) -> Callable[[jraph.GraphsTuple, dict[str, np.ndarray, int]], np.ndarray]:
    """Factory function for the loss function.

    Args:
        energy_weight_schedule: A schedule function returning the weight for the energy
                                given an epoch number.
        forces_weight_schedule: A schedule function returning the weight for the forces
                                given an epoch number.
        stress_weight_schedule: A schedule function returning the weight for the stress
                                given an epoch number.
        use_huber_loss: Whether to use the Huber loss. If False, then use the MSE loss.

    Returns:
        The loss function.
    """

    def _loss_fun(
        graph: jraph.GraphsTuple,
        predictions: dict[str, np.ndarray],
        training_epoch: int,
    ) -> jnp.ndarray:
        energy_weight = energy_weight_schedule(training_epoch)
        forces_weight = forces_weight_schedule(training_epoch)
        stress_weight = stress_weight_schedule(training_epoch)

        loss = 0

        energy = predictions["energy"]
        if use_huber_loss:
            loss += energy_weight * _huber_loss_energy(graph, energy)
        else:
            loss += energy_weight * _mean_squared_error_energy(graph, energy)

        forces = predictions["forces"]
        if use_huber_loss:
            loss += forces_weight * _adaptive_huber_loss_forces(graph, forces)
        else:
            loss += forces_weight * _mean_squared_error_forces(graph, forces)

        if "stress" in predictions:
            stress = predictions["stress"]
            if use_huber_loss:
                loss += stress_weight * _huber_loss_stress(graph, stress)
            else:
                loss += stress_weight * _mean_squared_error_stress(graph, stress)

        return loss  # [n_graphs, ]

    return _loss_fun


class WeightedEnergyForcesStressLoss:
    """Class for the loss function."""

    def __init__(
        self,
        energy_weight_schedule: Callable[[int], float],
        forces_weight_schedule: Callable[[int], float],
        stress_weight_schedule: Callable[[int], float],
        model_predictor_fun: Callable,
        return_eval_metrics: bool = False,
        use_huber_loss: bool = False,
    ) -> None:
        """Constructor.

        Args:
            energy_weight_schedule: The schedule function for the energy weight.
            forces_weight_schedule: The schedule function for the energy weight.
            stress_weight_schedule: The schedule function for the energy weight.
            model_predictor_fun: The MLIP model predictor function.
            return_eval_metrics: Whether to return evaluation metrics in the
                                 auxiliary metrics dictionary.
            use_huber_loss: Whether to use the Huber loss. If ``False`` (default),
                            then use the MSE loss.
        """
        super().__init__()
        self.model_predictor_fun = model_predictor_fun
        self.return_eval_metrics = return_eval_metrics
        self.loss_fn = make_weighted_energy_forces_stress_loss(
            energy_weight_schedule,
            forces_weight_schedule,
            stress_weight_schedule,
            use_huber_loss,
        )
        self.energy_weight_schedule = energy_weight_schedule
        self.forces_weight_schedule = forces_weight_schedule
        self.stress_weight_schedule = stress_weight_schedule

    def __call__(
        self, params: ModelParameters, ref_graph: jraph.GraphsTuple, training_epoch: int
    ) -> tuple[float, dict[str, float]]:
        """The call function that outputs the loss and metrics (auxiliary data).

        Args:
            params: The model parameters.
            ref_graph: The reference graph holding the ground truth data.
            training_epoch: The epoch number.

        Returns:
            The loss and the auxiliary metrics dictionary.
        """
        graph_mask = jraph.get_graph_padding_mask(ref_graph)  # [n_graphs,]

        predictions = self.model_predictor_fun(params, ref_graph)

        loss = self.loss_fn(ref_graph, predictions, training_epoch)
        n_graphs = jnp.sum(graph_mask)
        total_loss = jnp.sum(jnp.where(graph_mask, loss, 0.0))
        avg_loss = total_loss / n_graphs

        metrics = {
            "loss": avg_loss,
            "energy_weight": self.energy_weight_schedule(training_epoch),
            "forces_weight": self.forces_weight_schedule(training_epoch),
            "stress_weight": self.stress_weight_schedule(training_epoch),
        }

        if self.return_eval_metrics:
            node_mask = jraph.get_node_padding_mask(ref_graph)  # [n_nodes,]

            delta_es_list = []
            es_list = []

            delta_es_per_atom_list = []
            es_per_atom_list = []

            delta_fs_list = []
            fs_list = []

            delta_stress_list = []
            stress_list = []

            delta_stress_per_atom_list = []
            stress_per_atom_list = []

            pred_graph = ref_graph._replace(
                nodes=ref_graph.nodes._replace(forces=predictions["forces"]),
                globals=ref_graph.globals._replace(
                    energy=predictions["energy"],
                    stress=predictions.get("stress"),
                ),
            )

            # ref_graph = jraph.unpad_with_graphs(ref_graph)
            # pred_graph = jraph.unpad_with_graphs(pred_graph)

            if ref_graph.globals.energy is not None:
                delta_es_list.append(
                    ref_graph.globals.energy - pred_graph.globals.energy
                )
                es_list.append(ref_graph.globals.energy)

                delta_es_per_atom_list.append(
                    _safe_divide(
                        (ref_graph.globals.energy - pred_graph.globals.energy),
                        ref_graph.n_node,
                    )
                )
                es_per_atom_list.append(ref_graph.globals.energy / jnp.sum(node_mask))

            if ref_graph.nodes.forces is not None:
                delta_fs_list.append(ref_graph.nodes.forces - pred_graph.nodes.forces)
                fs_list.append(ref_graph.nodes.forces)

            if ref_graph.globals.stress is not None:
                delta_stress_list.append(
                    ref_graph.globals.stress - pred_graph.globals.stress
                )
                stress_list.append(ref_graph.globals.stress)

                delta_stress_per_atom_list.append(
                    _safe_divide(
                        (ref_graph.globals.stress - pred_graph.globals.stress),
                        ref_graph.n_node[:, None, None],
                    )
                )
                stress_per_atom_list.append(
                    ref_graph.globals.stress / jnp.sum(node_mask)
                )

            metrics = {
                "loss": avg_loss,
                "mae_e": None,
                "rel_mae_e": None,
                "mae_e_per_atom": None,
                "rel_mae_e_per_atom": None,
                "rmse_e": None,
                "rel_rmse_e": None,
                "rmse_e_per_atom": None,
                "rel_rmse_e_per_atom": None,
                "q95_e": None,
                "mae_f": None,
                "rel_mae_f": None,
                "rmse_f": None,
                "rel_rmse_f": None,
                "q95_f": None,
                "mae_stress": None,
                "rel_mae_stress": None,
                "mae_stress_per_atom": None,
                "rel_mae_stress_per_atom": None,
                "rmse_stress": None,
                "rel_rmse_stress": None,
                "rmse_stress_per_atom": None,
                "rel_rmse_stress_per_atom": None,
                "q95_stress": None,
            }

            if len(delta_es_list) > 0:
                delta_es = jnp.concatenate(delta_es_list, axis=0)
                delta_es_per_atom = jnp.concatenate(delta_es_per_atom_list, axis=0)
                es = jnp.concatenate(es_list, axis=0)
                es_per_atom = jnp.concatenate(es_per_atom_list, axis=0)
                metrics.update(
                    {
                        # Mean absolute error
                        "mae_e": _compute_mae(delta_es, graph_mask),
                        "rel_mae_e": _compute_rel_mae(delta_es, es, graph_mask),
                        "mae_e_per_atom": _compute_mae(delta_es_per_atom, graph_mask),
                        "rel_mae_e_per_atom": _compute_rel_mae(
                            delta_es_per_atom, es_per_atom, graph_mask
                        ),
                        # Root-mean-square error
                        "rmse_e": _compute_rmse(delta_es, graph_mask),
                        "rel_rmse_e": _compute_rel_rmse(delta_es, es, graph_mask),
                        "rmse_e_per_atom": _compute_rmse(delta_es_per_atom, graph_mask),
                        "rel_rmse_e_per_atom": _compute_rel_rmse(
                            delta_es_per_atom, es_per_atom, graph_mask
                        ),
                        # Q_95
                        "q95_e": _compute_q95(delta_es),
                    }
                )

            if len(delta_fs_list) > 0:
                delta_fs = jnp.concatenate(delta_fs_list, axis=0)
                fs = jnp.concatenate(fs_list, axis=0)

                metrics.update(
                    {
                        # Mean absolute error
                        "mae_f": _compute_mae_f(delta_fs, node_mask),
                        "rel_mae_f": _compute_rel_mae_f(delta_fs, fs, node_mask),
                        # Root-mean-square error
                        "rmse_f": _compute_rmse_f(delta_fs, node_mask),
                        "rel_rmse_f": _compute_rel_rmse_f(delta_fs, fs, node_mask),
                        # Q_95
                        "q95_f": _compute_q95(delta_fs),
                    }
                )

            if len(delta_stress_list) > 0:
                delta_stress = jnp.concatenate(delta_stress_list, axis=0)
                delta_stress_per_atom = jnp.concatenate(
                    delta_stress_per_atom_list, axis=0
                )
                stress = jnp.concatenate(stress_list, axis=0)
                stress_per_atom = jnp.concatenate(stress_per_atom_list, axis=0)
                metrics.update(
                    {
                        # Mean absolute error
                        "mae_stress": _compute_mae_stress(delta_stress, graph_mask),
                        "rel_mae_stress": _compute_rel_mae_stress(
                            delta_stress, stress, graph_mask
                        ),
                        "mae_stress_per_atom": _compute_mae_stress(
                            delta_stress_per_atom, graph_mask
                        ),
                        "rel_mae_stress_per_atom": _compute_rel_mae_stress(
                            delta_stress_per_atom, stress_per_atom, graph_mask
                        ),
                        # Root-mean-square error
                        "rmse_stress": _compute_rmse_stress(delta_stress, graph_mask),
                        "rel_rmse_stress": _compute_rel_rmse_stress(
                            delta_stress, stress, graph_mask
                        ),
                        "rmse_stress_per_atom": _compute_rmse_stress(
                            delta_stress_per_atom, graph_mask
                        ),
                        "rel_rmse_stress_per_atom": _compute_rel_rmse_stress(
                            delta_stress_per_atom, stress_per_atom, graph_mask
                        ),
                        # Q_95
                        "q95_stress": _compute_q95(delta_stress),
                    }
                )

        return avg_loss, metrics

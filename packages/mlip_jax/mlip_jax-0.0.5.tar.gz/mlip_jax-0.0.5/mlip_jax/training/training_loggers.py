from typing import Any

from rich import print as table_print
from rich.table import Table

from mlip_jax.training.training_io_handler import LogCategory


def _build_rich_table(
    metrics: dict[str, int | float], title: str, epoch_number: int, metric_color: str
) -> Table:
    table = Table(
        title=f"{title} at epoch {epoch_number}",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    keys = [k.replace("_", " ").capitalize() for k in metrics.keys()]
    values = [v if isinstance(v, int) else f"{float(v):.3f}" for v in metrics.values()]

    for k, v in zip(keys, values):
        _k = f"[{metric_color}]{k}[/{metric_color}]"
        _v = f"[white]{v}[/white]"
        table.add_row(_k, _v)

    return table


def log_metrics_to_table(
    category: LogCategory, to_log: dict[str, Any], epoch_number: int
) -> None:
    """Logging function for the training loop which logs the metrics to a nice table.

    The table will be printed to the command line.

    Args:
        category: The logging category describing what type of data is currently logged.
        to_log: The data to log (typically, the metrics).
        epoch_number: The current epoch number.
    """
    table = None
    if category == LogCategory.BEST_MODEL:
        table = _build_rich_table(to_log, "Best model", epoch_number, "white")
    elif category == LogCategory.TRAIN_METRICS:
        table = _build_rich_table(to_log, "Training set metrics", epoch_number, "cyan")
    elif category == LogCategory.EVAL_METRICS:
        table = _build_rich_table(
            to_log, "Validation set metrics", epoch_number, "green"
        )
    elif category == LogCategory.TEST_METRICS:
        table = _build_rich_table(
            to_log, "Test set metrics", epoch_number, "blue_violet"
        )

    if table is not None:
        table_print(table)

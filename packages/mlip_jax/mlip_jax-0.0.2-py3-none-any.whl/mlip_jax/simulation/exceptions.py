class SimulationIsNotInitializedError(Exception):
    """Exception to be raised if a simulation is started before it was initialized."""


class S3OutputPathIsNotS3PathError(Exception):
    """Exception to be raised if a path is expected to be an S3 path,
    but it isn't provided as one.
    """

from typing import TypeAlias

from mlip_jax.data.chemical_system import ChemicalSystem

# To make the Callable with 3 list[ChemicalSystem] arguments in DataLoader more
# readable.
ChemicalSystems: TypeAlias = list[ChemicalSystem]

# Type alias for the DataLoader.load function output signature for convenience.
# It contains the list of chemical systems for train, validation and test splits.
ChemicalSystemsBySplit: TypeAlias = tuple[
    ChemicalSystems, ChemicalSystems, ChemicalSystems
]

"""Engineering materials for build123d models.

A *typical-values* database: figures are representative, not certified allowables
(materials are highly manufacturing- and vendor-specific). ``source`` records
origin -- PCBWay scrape values backfilled with typical reference (MatWeb-class)
values for omitted structure-insensitive fields (E, nu, rho, cp, k), tagged
"... + MatWeb"; ``condition`` records the temper/heat-treat/cure state that the
PCBWay strength values correspond to.

Usage::

    from bd_materials import REGISTRY, ALU_6061_T6
    ALU_6061_T6.mass_g_from_volume_mm3(part.volume)
    REGISTRY.filter(family="aluminum", condition="T6")
"""

from __future__ import annotations

from . import finishes, glass, metals, paper, plastics, resins, textile, wood
from .finishes import *  # noqa: F401,F403  (Finish + finish instances + queries)
from .base import (
    ArealMaterial,
    IsotropicSolidMaterial,
    Material,
    MaterialRegistry,
    REGISTRY,
)
from .finished import FinishedMaterial, Process
from .glass import *  # noqa: F401,F403  (glass instance)
from .metals import *  # noqa: F401,F403  (MetalMaterial + metal instances)
from .paper import *  # noqa: F401,F403  (PaperMaterial + paper instances)
from .plastics import *  # noqa: F401,F403  (PlasticMaterial + thermoplastics + composites)
from .resins import *  # noqa: F401,F403  (resin instances)
from .textile import *  # noqa: F401,F403  (TextileMaterial + textile instances)
from .wood import *  # noqa: F401,F403  (WoodMaterial + wood instances)

__all__ = [
    "Material",
    "IsotropicSolidMaterial",
    "ArealMaterial",
    "MaterialRegistry",
    "REGISTRY",
    "FinishedMaterial",
    "Process",
]
__all__ += metals.__all__
__all__ += plastics.__all__
__all__ += resins.__all__
__all__ += wood.__all__
__all__ += paper.__all__
__all__ += textile.__all__
__all__ += glass.__all__
__all__ += finishes.__all__

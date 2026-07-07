"""Engineering materials for build123d models.

A *typical-values* library: figures are representative, not certified allowables
(materials are highly manufacturing- and vendor-specific). Materials are reached
through **category namespaces** -- the code and its tab-completion are the
catalog; there is no string-keyed registry to search::

    from bd_materials import metals, plastics, finishes, FinishedMaterial, Process
    from bd_materials.metals import Alu

    metals.aluminum()                     # 6061-T6 (default)
    metals.aluminum(Alu.G7075_T6)         # a MetalMaterial
    plastics.pla(color="red")             # a coloured PlasticMaterial
    finishes.anodize("champagne")         # an AppliedFinish

    FinishedMaterial(metals.aluminum()).pbr           # resolved three.js look

Each category exposes family functions (metals/plastics) or per-material
functions (wood/paper/textile/glass/resins), plus ``all()`` to enumerate it.
Custom materials are just the dataclasses: ``metals.MetalMaterial(...)`` or
``metals.aluminum().with_overrides(...)``.
"""

from __future__ import annotations

from . import (
    finishes,
    glass,
    metals,
    paper,
    plastics,
    resins,
    textile,
    wood,
)
from .base import ArealMaterial, IsotropicSolidMaterial, Material
from .finished import FinishedMaterial, Process

__all__ = [
    # category namespaces (the catalog); finish functions live under `finishes`
    "metals",
    "plastics",
    "resins",
    "wood",
    "paper",
    "textile",
    "glass",
    "finishes",
    # base types (for isinstance checks / building custom materials)
    "Material",
    "IsotropicSolidMaterial",
    "ArealMaterial",
    # user touch points
    "FinishedMaterial",
    "Process",
]

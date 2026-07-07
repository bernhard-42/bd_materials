"""Range-based engineering-materials catalog for build123d.

Typical-value **ranges** (min-max), not single points -- honest about real
variation and free of the vendor/datasheet-licensing trap (a published band is
common knowledge). Materials are reached through category namespaces; a family
function returns a :class:`FinishedMaterial` (the part touch point): ``.material``
is the physics (a shared, immutable range table), ``.pbr`` is the three.js look.

    from bd_materials import metals, plastics, finishes
    from bd_materials.metals import Alu

    metals.aluminum()                                  # FinishedMaterial (6061 default)
    metals.aluminum(Alu.G7075_T6, finishes.anodize("champagne"))
    plastics.pla(color="red")                          # selectable colour (case 2)
    plastics.pmma(color="clear", thickness_mm=3)       # transparent -> pane thickness

    print(metals.aluminum().material)                  # typical-value dump (__str__)
    metals.aluminum().pbr                              # resolved look (needs threejs_materials)

Intrinsic identity (``family``, ``category``, ``transparent``) lives on the
``Material``; per-part choices (``color``, ``thickness_mm``, ``finish``,
``process``) live on the ``FinishedMaterial`` (``finish`` and ``process`` are
mutually exclusive). Each category exposes grade enums + family functions +
``ALL_<CATEGORY>`` + its ``<Cat>Material`` class. Shared primitives (``Range``,
``NOT_SUITABLE``, ``PROPERTY_UNITS``, ``RangeMaterial``) live in ``core``.
"""

from __future__ import annotations

from . import applicability, core, finishes
from .applicability import typical_finishes, typical_materials
from .finished import FinishedMaterial, Process
from .materials import (
    glass,
    metals,
    paper,
    plastics,
    resins,
    textile,
    wood,
)

__all__ = [
    # category namespaces (the catalog)
    "metals",
    "plastics",
    "resins",
    "glass",
    "wood",
    "paper",
    "textile",
    # finishes + shared core primitives
    "finishes",
    "core",
    # material<->finish applicability (advisory hints)
    "applicability",
    "typical_finishes",
    "typical_materials",
    # user touch points
    "FinishedMaterial",
    "Process",
]

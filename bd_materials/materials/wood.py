"""Range-based typical values for wood (solid species + engineered boards).

Sibling of the other range modules using the shared :mod:`..core` primitives.
Values are for ~12% moisture content and shift substantially when wet. Species are
grouped into three families -- :class:`Hardwood`, :class:`Softwood`,
:class:`EngineeredWood` -- each with a ``GENERIC`` early-phase grade where useful.

Wood is **orthotropic**; to fit a scalar range table the fields carry the
design-relevant **along-grain** values:

* ``modulus_of_elasticity`` -- along grain (parallel to fibres), GPa.
* ``modulus_of_rupture`` -- bending strength, MPa (wood has no true yield).
* ``compressive_strength_parallel`` -- along grain, MPa.
* ``janka_hardness`` -- side hardness (indentation force), N. ``None`` for
  engineered boards (MDF/OSB), where it is not commonly quoted (value missing).

``thermal_expansion`` is intentionally omitted: wood's dimensional movement is
driven by moisture, not temperature, so a CTE would mislead.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import Range, RangeMaterial


@dataclass(frozen=True)
class WoodMaterial(RangeMaterial):
    """A wood described by typical-value ranges (along-grain where directional).

    ``density`` is a single value; the rest are ``Range`` bands (or ``None`` if
    the value is missing). ``family`` is the three.js wood factory key; wood is
    opaque (no colour -- stain/paint is a finish), so ``transparent`` is False.
    """

    category: ClassVar[str] = "wood"
    name: str
    density: float  # kg/m³ (single representative value, ~12% MC)
    modulus_of_elasticity: Range | None  # GPa (along grain)
    modulus_of_rupture: Range | None  # MPa (bending strength)
    compressive_strength_parallel: Range | None  # MPa (along grain)
    janka_hardness: Range | None  # N (side hardness; None for MDF/OSB)
    specific_heat_capacity: Range | None  # J/(kg·K)
    thermal_conductivity: Range | None  # W/(m·K)
    family: str | None = None
    transparent: bool = False


class Hardwood(Enum):
    GENERIC = auto()  # early-phase, before a species is chosen
    ASH = auto()
    BEECH = auto()
    BIRCH = auto()
    MAPLE = auto()
    OAK = auto()
    WALNUT = auto()


HARDWOOD_MATERIALS: dict[Hardwood, WoodMaterial] = {
    Hardwood.GENERIC: WoodMaterial(
        name="Hardwood_GENERIC",
        density=675,
        modulus_of_elasticity=Range(10, 13),
        modulus_of_rupture=Range(90, 110),
        compressive_strength_parallel=Range(45, 60),
        janka_hardness=Range(4000, 7000),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
        family="oak",
    ),
    Hardwood.ASH: WoodMaterial(
        name="Hardwood_ASH",
        density=670,
        modulus_of_elasticity=Range(10, 13),
        modulus_of_rupture=Range(90, 115),
        compressive_strength_parallel=Range(45, 58),
        janka_hardness=Range(5500, 7000),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
        family="ash",
    ),
    Hardwood.BEECH: WoodMaterial(
        name="Hardwood_BEECH",
        density=720,
        modulus_of_elasticity=Range(11, 15),
        modulus_of_rupture=Range(90, 115),
        compressive_strength_parallel=Range(44, 56),
        janka_hardness=Range(5500, 7000),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
        family="beech",
    ),
    Hardwood.BIRCH: WoodMaterial(
        name="Hardwood_BIRCH",
        density=660,
        modulus_of_elasticity=Range(11, 15),
        modulus_of_rupture=Range(100, 125),
        compressive_strength_parallel=Range(50, 62),
        janka_hardness=Range(4800, 6200),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
        family="birch",
    ),
    Hardwood.MAPLE: WoodMaterial(
        name="Hardwood_MAPLE",
        density=705,
        modulus_of_elasticity=Range(11, 14),
        modulus_of_rupture=Range(95, 120),
        compressive_strength_parallel=Range(48, 60),
        janka_hardness=Range(5500, 7000),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
        family="maple",
    ),
    Hardwood.OAK: WoodMaterial(
        name="Hardwood_OAK",
        density=755,
        modulus_of_elasticity=Range(10, 14),
        modulus_of_rupture=Range(90, 115),
        compressive_strength_parallel=Range(45, 58),
        janka_hardness=Range(5000, 6500),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.14, 0.20),
        family="oak",
    ),
    Hardwood.WALNUT: WoodMaterial(
        name="Hardwood_WALNUT",
        density=640,
        modulus_of_elasticity=Range(10, 13),
        modulus_of_rupture=Range(90, 110),
        compressive_strength_parallel=Range(46, 58),
        janka_hardness=Range(4800, 5800),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
        family="walnut",
    ),
}


class Softwood(Enum):
    GENERIC = auto()  # early-phase, before a species is chosen
    SPRUCE = auto()
    PINE = auto()


SOFTWOOD_MATERIALS: dict[Softwood, WoodMaterial] = {
    Softwood.GENERIC: WoodMaterial(
        name="Softwood_GENERIC",
        density=470,
        modulus_of_elasticity=Range(8, 11),
        modulus_of_rupture=Range(60, 80),
        compressive_strength_parallel=Range(30, 40),
        janka_hardness=Range(2000, 3000),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
        family="spruce",
    ),
    Softwood.SPRUCE: WoodMaterial(
        name="Softwood_SPRUCE",
        density=430,
        modulus_of_elasticity=Range(8, 12),
        modulus_of_rupture=Range(60, 80),
        compressive_strength_parallel=Range(33, 43),
        janka_hardness=Range(2200, 2900),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.14),
        family="spruce",
    ),
    Softwood.PINE: WoodMaterial(
        name="Softwood_PINE",
        density=500,
        modulus_of_elasticity=Range(8, 12),
        modulus_of_rupture=Range(65, 100),
        compressive_strength_parallel=Range(35, 55),
        janka_hardness=Range(1700, 4500),
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
        family="spruce",  # three.js has no pine factory -- spruce is the closest look
    ),
}


class EngineeredWood(Enum):
    MDF = auto()
    OSB = auto()


ENGINEERED_WOOD_MATERIALS: dict[EngineeredWood, WoodMaterial] = {
    EngineeredWood.MDF: WoodMaterial(
        name="EngineeredWood_MDF",
        density=750,
        modulus_of_elasticity=Range(3.0, 4.5),
        modulus_of_rupture=Range(28, 42),
        compressive_strength_parallel=Range(10, 18),
        janka_hardness=None,
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
        family="mdf",
    ),
    EngineeredWood.OSB: WoodMaterial(
        name="EngineeredWood_OSB",
        density=640,
        modulus_of_elasticity=Range(4.5, 7.0),
        modulus_of_rupture=Range(22, 35),
        compressive_strength_parallel=Range(10, 18),
        janka_hardness=None,
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
        family="osb",
    ),
}


# ===========================================================================
# Family functions (return FinishedMaterial; wood is opaque -- no colour).
# ===========================================================================

_Finish = AppliedFinish | list[AppliedFinish] | None


def hardwood(
    grade: Hardwood = Hardwood.GENERIC,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial:
    return FinishedMaterial(HARDWOOD_MATERIALS[grade], finish, process=process)


def softwood(
    grade: Softwood = Softwood.GENERIC,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial:
    return FinishedMaterial(SOFTWOOD_MATERIALS[grade], finish, process=process)


def engineered_wood(
    grade: EngineeredWood = EngineeredWood.MDF,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial:
    return FinishedMaterial(ENGINEERED_WOOD_MATERIALS[grade], finish, process=process)


ALL_WOODS = (
    *HARDWOOD_MATERIALS.values(),
    *SOFTWOOD_MATERIALS.values(),
    *ENGINEERED_WOOD_MATERIALS.values(),
)


if __name__ == "__main__":
    print(f"woods: {len(ALL_WOODS)}")
    print()
    print(HARDWOOD_MATERIALS[Hardwood.OAK])
    print(ENGINEERED_WOOD_MATERIALS[EngineeredWood.MDF])

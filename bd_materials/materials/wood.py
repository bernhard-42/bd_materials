"""Typical-value property ranges for wood (solid species + engineered boards).

Values are for ~12% moisture content and shift substantially when wet. Wood is
**orthotropic**; to fit a scalar range table the fields carry the design-relevant
**along-grain** values:

* ``modulus_of_elasticity`` -- along grain (parallel to fibres), GPa.
* ``modulus_of_rupture`` -- bending strength, MPa (wood has no true yield).
* ``compressive_strength_parallel`` -- along grain, MPa.
* ``janka_hardness`` -- side hardness (indentation force), N; ``None`` for engineered
  boards, where it is not commonly quoted.

``thermal_expansion`` is intentionally omitted: wood moves with moisture, not
temperature, so a CTE would mislead.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, FinishSpec, Process
from ..core import Range, RangeMaterial, with_density


@dataclass(frozen=True, kw_only=True)
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


# --- Hardwood ----------------------------------------------------------------
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
        # identity
        name="Hardwood_GENERIC",
        family="oak",
        # mechanical properties
        compressive_strength_parallel=Range(45, 60),
        density=675,
        janka_hardness=Range(4000, 7000),
        modulus_of_elasticity=Range(10, 13),
        modulus_of_rupture=Range(90, 110),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
    ),
    Hardwood.ASH: WoodMaterial(
        # identity
        name="Hardwood_ASH",
        family="ash",
        # mechanical properties
        compressive_strength_parallel=Range(45, 58),
        density=670,
        janka_hardness=Range(5500, 7000),
        modulus_of_elasticity=Range(10, 13),
        modulus_of_rupture=Range(90, 115),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
    ),
    Hardwood.BEECH: WoodMaterial(
        # identity
        name="Hardwood_BEECH",
        family="beech",
        # mechanical properties
        compressive_strength_parallel=Range(44, 56),
        density=720,
        janka_hardness=Range(5500, 7000),
        modulus_of_elasticity=Range(11, 15),
        modulus_of_rupture=Range(90, 115),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
    ),
    Hardwood.BIRCH: WoodMaterial(
        # identity
        name="Hardwood_BIRCH",
        family="birch",
        # mechanical properties
        compressive_strength_parallel=Range(50, 62),
        density=660,
        janka_hardness=Range(4800, 6200),
        modulus_of_elasticity=Range(11, 15),
        modulus_of_rupture=Range(100, 125),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
    ),
    Hardwood.MAPLE: WoodMaterial(
        # identity
        name="Hardwood_MAPLE",
        family="maple",
        # mechanical properties
        compressive_strength_parallel=Range(48, 60),
        density=705,
        janka_hardness=Range(5500, 7000),
        modulus_of_elasticity=Range(11, 14),
        modulus_of_rupture=Range(95, 120),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
    ),
    Hardwood.OAK: WoodMaterial(
        # identity
        name="Hardwood_OAK",
        family="oak",
        # mechanical properties
        compressive_strength_parallel=Range(45, 58),
        density=755,
        janka_hardness=Range(5000, 6500),
        modulus_of_elasticity=Range(10, 14),
        modulus_of_rupture=Range(90, 115),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.14, 0.20),
    ),
    Hardwood.WALNUT: WoodMaterial(
        # identity
        name="Hardwood_WALNUT",
        family="walnut",
        # mechanical properties
        compressive_strength_parallel=Range(46, 58),
        density=640,
        janka_hardness=Range(4800, 5800),
        modulus_of_elasticity=Range(10, 13),
        modulus_of_rupture=Range(90, 110),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.12, 0.18),
    ),
}


def hardwood(
    grade: Hardwood = Hardwood.GENERIC,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[WoodMaterial]:
    """Hardwood as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic species.
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process``.
        process: As-made surface hint (e.g. ``Process.FDM``). Mutually exclusive with
            ``finish``.
        density: Override the material's single representative density (kg/m³) for this
            part.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(HARDWOOD_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Softwood ----------------------------------------------------------------
class Softwood(Enum):
    GENERIC = auto()  # early-phase, before a species is chosen
    SPRUCE = auto()
    PINE = auto()


SOFTWOOD_MATERIALS: dict[Softwood, WoodMaterial] = {
    Softwood.GENERIC: WoodMaterial(
        # identity
        name="Softwood_GENERIC",
        family="spruce",
        # mechanical properties
        compressive_strength_parallel=Range(30, 40),
        density=470,
        janka_hardness=Range(2000, 3000),
        modulus_of_elasticity=Range(8, 11),
        modulus_of_rupture=Range(60, 80),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
    ),
    Softwood.SPRUCE: WoodMaterial(
        # identity
        name="Softwood_SPRUCE",
        family="spruce",
        # mechanical properties
        compressive_strength_parallel=Range(33, 43),
        density=430,
        janka_hardness=Range(2200, 2900),
        modulus_of_elasticity=Range(8, 12),
        modulus_of_rupture=Range(60, 80),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.14),
    ),
    Softwood.PINE: WoodMaterial(
        # identity
        name="Softwood_PINE",
        family="pine",
        # mechanical properties
        compressive_strength_parallel=Range(35, 55),
        density=500,
        janka_hardness=Range(1700, 4500),
        modulus_of_elasticity=Range(8, 12),
        modulus_of_rupture=Range(65, 100),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
    ),
}


def softwood(
    grade: Softwood = Softwood.GENERIC,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[WoodMaterial]:
    """Softwood as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic species.
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process``.
        process: As-made surface hint (e.g. ``Process.FDM``). Mutually exclusive with
            ``finish``.
        density: Override the material's single representative density (kg/m³) for this
            part.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(SOFTWOOD_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Engineered wood ---------------------------------------------------------
class EngineeredWood(Enum):
    MDF = auto()
    OSB = auto()


ENGINEERED_WOOD_MATERIALS: dict[EngineeredWood, WoodMaterial] = {
    EngineeredWood.MDF: WoodMaterial(
        # identity
        name="EngineeredWood_MDF",
        family="mdf",
        # mechanical properties
        compressive_strength_parallel=Range(10, 18),
        density=750,
        janka_hardness=None,
        modulus_of_elasticity=Range(3.0, 4.5),
        modulus_of_rupture=Range(28, 42),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
    ),
    EngineeredWood.OSB: WoodMaterial(
        # identity
        name="EngineeredWood_OSB",
        family="osb",
        # mechanical properties
        compressive_strength_parallel=Range(10, 18),
        density=640,
        janka_hardness=None,
        modulus_of_elasticity=Range(4.5, 7.0),
        modulus_of_rupture=Range(22, 35),
        # thermal properties
        specific_heat_capacity=Range(1200, 1700),
        thermal_conductivity=Range(0.10, 0.15),
    ),
}


def engineered_wood(
    grade: EngineeredWood = EngineeredWood.MDF,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[WoodMaterial]:
    """Engineered wood as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to MDF.
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process``.
        process: As-made surface hint (e.g. ``Process.FDM``). Mutually exclusive with
            ``finish``.
        density: Override the material's single representative density (kg/m³) for this
            part.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(ENGINEERED_WOOD_MATERIALS[grade], density),
        finish,
        process=process,
    )


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

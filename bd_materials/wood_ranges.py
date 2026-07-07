"""Range-based typical values for wood (solid species + engineered boards).

Sibling of the other ``*_ranges`` modules using the shared :mod:`.ranges`
primitives. Values are for ~12% moisture content and shift substantially when wet.
Two generic softwood/hardwood categories cover early-phase design before a species
is chosen.

Wood is **orthotropic**; to fit a scalar range table the fields carry the
design-relevant **along-grain** values:

* ``modulus_of_elasticity`` -- along grain (parallel to fibres), GPa.
* ``modulus_of_rupture`` -- bending strength, MPa (wood has no true yield).
* ``compressive_strength_parallel`` -- along grain, MPa.
* ``janka_hardness`` -- side hardness (indentation force), N. ``None`` for
  engineered boards (MDF/OSB), where it is not commonly quoted (value missing).

``thermal_expansion`` is intentionally omitted: wood's dimensional movement is
driven by moisture, not temperature, so a CTE would mislead.

Standalone: does not touch the point-value library or the finishes/PBR stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ranges import Range, RangeMaterial


@dataclass(frozen=True)
class Material(RangeMaterial):
    """A wood described by typical-value ranges (along-grain where directional).

    ``density`` is a single value; the rest are ``Range`` bands (or ``None`` if
    the value is missing).
    """

    name: str
    density: float  # kg/m³ (single representative value, ~12% MC)
    modulus_of_elasticity: Range | None  # GPa (along grain)
    modulus_of_rupture: Range | None  # MPa (bending strength)
    compressive_strength_parallel: Range | None  # MPa (along grain)
    janka_hardness: Range | None  # N (side hardness; None for MDF/OSB)
    specific_heat_capacity: Range | None  # J/(kg·K)
    thermal_conductivity: Range | None  # W/(m·K)


# Generic categories for early-phase design, before a species is chosen.
WOOD_SOFTWOOD_GENERIC = Material(
    name="WOOD_SOFTWOOD_GENERIC",
    density=470,
    modulus_of_elasticity=Range(8, 11),
    modulus_of_rupture=Range(60, 80),
    compressive_strength_parallel=Range(30, 40),
    janka_hardness=Range(1500, 2700),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.10, 0.15),
)

WOOD_HARDWOOD_GENERIC = Material(
    name="WOOD_HARDWOOD_GENERIC",
    density=675,
    modulus_of_elasticity=Range(10, 13),
    modulus_of_rupture=Range(90, 110),
    compressive_strength_parallel=Range(45, 60),
    janka_hardness=Range(4000, 7000),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.12, 0.18),
)


WOOD_ASH = Material(
    name="WOOD_ASH",
    density=670,
    modulus_of_elasticity=Range(10, 13),
    modulus_of_rupture=Range(90, 115),
    compressive_strength_parallel=Range(45, 58),
    janka_hardness=Range(5000, 6500),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.12, 0.18),
)

WOOD_BEECH = Material(
    name="WOOD_BEECH",
    density=720,
    modulus_of_elasticity=Range(10, 13),
    modulus_of_rupture=Range(90, 115),
    compressive_strength_parallel=Range(44, 56),
    janka_hardness=Range(5000, 6500),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.12, 0.18),
)

WOOD_BIRCH = Material(
    name="WOOD_BIRCH",
    density=660,
    modulus_of_elasticity=Range(11, 15),
    modulus_of_rupture=Range(100, 125),
    compressive_strength_parallel=Range(50, 62),
    janka_hardness=Range(4800, 6200),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.12, 0.18),
)

WOOD_MAPLE = Material(
    name="WOOD_MAPLE",
    density=705,
    modulus_of_elasticity=Range(11, 14),
    modulus_of_rupture=Range(95, 120),
    compressive_strength_parallel=Range(48, 60),
    janka_hardness=Range(5500, 7000),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.12, 0.18),
)

WOOD_OAK = Material(
    name="WOOD_OAK",
    density=755,
    modulus_of_elasticity=Range(10, 14),
    modulus_of_rupture=Range(90, 115),
    compressive_strength_parallel=Range(45, 58),
    janka_hardness=Range(5200, 6800),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.14, 0.20),
)

WOOD_WALNUT = Material(
    name="WOOD_WALNUT",
    density=610,
    modulus_of_elasticity=Range(10, 13),
    modulus_of_rupture=Range(90, 110),
    compressive_strength_parallel=Range(46, 58),
    janka_hardness=Range(4000, 5000),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.12, 0.18),
)

WOOD_SPRUCE = Material(
    name="WOOD_SPRUCE",
    density=430,
    modulus_of_elasticity=Range(8, 12),
    modulus_of_rupture=Range(60, 80),
    compressive_strength_parallel=Range(33, 43),
    janka_hardness=Range(1800, 2700),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.10, 0.14),
)

WOOD_PINE = Material(
    name="WOOD_PINE",
    density=500,
    modulus_of_elasticity=Range(8, 12),
    modulus_of_rupture=Range(65, 100),
    compressive_strength_parallel=Range(35, 55),
    janka_hardness=Range(1700, 3100),
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.10, 0.15),
)

WOOD_MDF = Material(
    name="WOOD_MDF",
    density=750,
    modulus_of_elasticity=Range(3.0, 4.5),
    modulus_of_rupture=Range(28, 42),
    compressive_strength_parallel=Range(10, 18),
    janka_hardness=None,
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.10, 0.15),
)

WOOD_OSB = Material(
    name="WOOD_OSB",
    density=640,
    modulus_of_elasticity=Range(4.5, 7.0),
    modulus_of_rupture=Range(22, 35),
    compressive_strength_parallel=Range(10, 18),
    janka_hardness=None,
    specific_heat_capacity=Range(1200, 1700),
    thermal_conductivity=Range(0.10, 0.15),
)


ALL_WOODS = (
    WOOD_SOFTWOOD_GENERIC,
    WOOD_HARDWOOD_GENERIC,
    WOOD_ASH,
    WOOD_BEECH,
    WOOD_BIRCH,
    WOOD_MAPLE,
    WOOD_OAK,
    WOOD_WALNUT,
    WOOD_SPRUCE,
    WOOD_PINE,
    WOOD_MDF,
    WOOD_OSB,
)


if __name__ == "__main__":
    print(f"woods: {len(ALL_WOODS)}")
    print()
    print(WOOD_OAK.describe())
    print(WOOD_MDF.describe())

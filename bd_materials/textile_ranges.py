"""Range-based typical values for textiles (woven fabric, felt, leather).

Sibling of the other ``*_ranges`` modules using the shared :mod:`.ranges`
primitives. Textiles are **areal goods**: the primary mass metric is grammage
(``areal_density``, g/m²), not volumetric density. ``tensile_strength`` is the
in-plane value and is approximate for these flexible materials. Properties are
highly grade-dependent -- treat as rough typicals.

A single generic **woven** fabric is carried (the knit variant was dropped);
felt and leather are grouped here as soft areal goods (leather isn't strictly a
textile).

Standalone: does not touch the point-value library or the finishes/PBR stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ranges import Range, RangeMaterial


@dataclass(frozen=True)
class Material(RangeMaterial):
    """A textile described by typical-value ranges.

    ``density`` is a single representative (apparent) value; ``areal_density``
    (grammage) is the primary mass metric.
    """

    name: str
    density: float  # kg/m³ (apparent, single representative value)
    areal_density: Range | None  # g/m² (grammage -- primary mass metric)
    thickness: Range | None  # mm
    tensile_strength: Range | None  # MPa (in-plane; approx)
    thermal_conductivity: Range | None  # W/(m·K)
    specific_heat_capacity: Range | None  # J/(kg·K)


TEXTILE_WOVEN = Material(
    name="TEXTILE_WOVEN",
    density=500,
    areal_density=Range(150, 300),
    thickness=Range(0.3, 0.6),
    tensile_strength=Range(10, 50),
    thermal_conductivity=Range(0.03, 0.07),
    specific_heat_capacity=Range(1300, 1700),
)

TEXTILE_FELT = Material(
    name="TEXTILE_FELT",
    density=120,
    areal_density=Range(200, 400),
    thickness=Range(2, 4),
    tensile_strength=Range(2, 10),
    thermal_conductivity=Range(0.04, 0.08),
    specific_heat_capacity=Range(1300, 1700),
)

TEXTILE_LEATHER = Material(
    name="TEXTILE_LEATHER",
    density=860,
    areal_density=Range(800, 1600),
    thickness=Range(1, 3),
    tensile_strength=Range(10, 30),
    thermal_conductivity=Range(0.14, 0.20),
    specific_heat_capacity=Range(1500, 2000),
)


ALL_TEXTILES = (TEXTILE_WOVEN, TEXTILE_FELT, TEXTILE_LEATHER)


if __name__ == "__main__":
    print(f"textiles: {len(ALL_TEXTILES)}")
    print()
    for _t in ALL_TEXTILES:
        print(_t.describe())
        print()

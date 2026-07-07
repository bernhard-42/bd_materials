"""Range-based typical values for paper goods (paper, board, foamboard).

Sibling of the other ``*_ranges`` modules using the shared :mod:`.ranges`
primitives. Paper is an **areal good**: its primary mass metric is grammage
(``areal_density``, g/m²), not volumetric density, and a cut sheet's mass is
grammage x area. ``tensile_strength`` is the in-plane (machine-direction) value
and is approximate for these structured/layered materials. Grade and supplier
variation is large -- treat as rough typicals.

Standalone: does not touch the point-value library or the finishes/PBR stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ranges import Range, RangeMaterial


@dataclass(frozen=True)
class Material(RangeMaterial):
    """A paper good described by typical-value ranges.

    ``density`` is a single representative (apparent) value; ``areal_density``
    (grammage) is the primary mass metric.
    """

    name: str
    density: float  # kg/m³ (apparent, single representative value)
    areal_density: Range | None  # g/m² (grammage -- primary mass metric)
    thickness: Range | None  # mm
    tensile_strength: Range | None  # MPa (in-plane, machine direction; approx)
    thermal_conductivity: Range | None  # W/(m·K)
    specific_heat_capacity: Range | None  # J/(kg·K)


PAPER_OFFICE = Material(
    name="PAPER_OFFICE",
    density=800,
    areal_density=Range(70, 90),
    thickness=Range(0.09, 0.12),
    tensile_strength=Range(20, 60),
    thermal_conductivity=Range(0.05, 0.10),
    specific_heat_capacity=Range(1300, 1400),
)

PAPER_CORRUGATED = Material(
    name="PAPER_CORRUGATED",
    density=140,
    areal_density=Range(400, 700),
    thickness=Range(3, 5),
    tensile_strength=Range(5, 25),
    thermal_conductivity=Range(0.05, 0.10),
    specific_heat_capacity=Range(1300, 1400),
)

PAPER_FOAMBOARD = Material(
    name="PAPER_FOAMBOARD",
    density=100,
    areal_density=Range(400, 550),
    thickness=Range(3, 6),
    tensile_strength=Range(2, 10),
    thermal_conductivity=Range(0.03, 0.06),
    specific_heat_capacity=Range(1300, 1500),
)


ALL_PAPERS = (PAPER_OFFICE, PAPER_CORRUGATED, PAPER_FOAMBOARD)


if __name__ == "__main__":
    print(f"papers: {len(ALL_PAPERS)}")
    print()
    for _p in ALL_PAPERS:
        print(_p.describe())
        print()

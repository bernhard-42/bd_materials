"""Range-based typical values for glass.

Sibling of the other ``*_ranges`` modules using the shared :mod:`.ranges`
primitives (``Range``, ``PROPERTY_UNITS``, ``RangeMaterial``).

Glass is an amorphous, brittle inorganic solid, so the field set is tailored:
yield strength, shear strength, elongation at break, and heat-deflection
temperature are omitted entirely (a brittle glass has no yield/ductile
elongation, and HDT is a polymer test) rather than carried as ``NOT_SUITABLE``.
``tensile_strength`` is the practical **flaw-limited** annealed strength (pristine
fibre is far higher; surface flaws dominate). Hardness is on the **Vickers (HV)**
scale. Both ``melting_temperature`` (the melt/working range -- glass has no sharp
melt point) and ``glass_transition_temperature`` (Tg) are carried.

Borosilicate's defining feature is its low thermal expansion (~3.3e-6/K vs
~9e-6/K for soda-lime), i.e. much better thermal-shock resistance.

Standalone: does not touch the point-value library or the finishes/PBR stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ranges import Range, RangeMaterial


@dataclass(frozen=True)
class Material(RangeMaterial):
    """A glass described by typical-value ranges.

    ``density`` is a single value; the rest are ``Range`` bands (or ``None`` if
    the value is missing). ``tensile_strength`` is flaw-limited (annealed).
    """

    name: str
    density: float  # kg/m³ (single representative value)
    tensile_strength: Range | None  # MPa (flaw-limited, annealed)
    modulus_of_elasticity: Range | None  # GPa
    shear_modulus: Range | None  # GPa
    poisson_ratio: Range | None  # dimensionless
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "HV" (Vickers)
    specific_heat_capacity: Range | None  # J/(kg·K)
    glass_transition_temperature: Range | None  # °C
    melting_temperature: Range | None  # °C (melt / working range)
    max_service_temp: Range | None  # °C (engineering guide limit, not a hard max)
    thermal_expansion: Range | None  # 1/K
    thermal_conductivity: Range | None  # W/(m·K)


GLASS_SODA_LIME = Material(
    name="GLASS_SODA_LIME",
    density=2500,
    tensile_strength=Range(30, 90),
    modulus_of_elasticity=Range(68, 74),
    shear_modulus=Range(26, 30),
    poisson_ratio=Range(0.21, 0.24),
    hardness=Range(470, 570),
    hardness_scale="HV",
    specific_heat_capacity=Range(750, 880),
    glass_transition_temperature=Range(520, 570),
    melting_temperature=Range(1400, 1600),
    max_service_temp=Range(400, 500),
    thermal_expansion=Range(8.5e-6, 9.5e-6),
    thermal_conductivity=Range(0.9, 1.1),
)

GLASS_BOROSILICATE = Material(
    name="GLASS_BOROSILICATE",
    density=2230,
    tensile_strength=Range(30, 90),
    modulus_of_elasticity=Range(60, 66),
    shear_modulus=Range(24, 28),
    poisson_ratio=Range(0.19, 0.22),
    hardness=Range(480, 600),
    hardness_scale="HV",
    specific_heat_capacity=Range(750, 830),
    glass_transition_temperature=Range(525, 565),
    melting_temperature=Range(1500, 1650),
    max_service_temp=Range(450, 500),
    thermal_expansion=Range(3.0e-6, 3.5e-6),
    thermal_conductivity=Range(1.0, 1.2),
)


ALL_GLASSES = (GLASS_SODA_LIME, GLASS_BOROSILICATE)


if __name__ == "__main__":
    print(f"glasses: {len(ALL_GLASSES)}")
    print()
    for _g in ALL_GLASSES:
        print(_g.describe())
        print()

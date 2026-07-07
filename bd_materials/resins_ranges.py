"""Range-based typical values for photopolymer resins (SLA / DLP).

Sibling of ``metals_ranges`` / ``plastics_ranges`` using the same approach and the
shared :mod:`.ranges` primitives (``Range``, ``PROPERTY_UNITS``, ``RangeMaterial``).

Resins are grouped into **vendor-neutral functional families** (standard, tough,
high-temp, ...) rather than individual products. The property set mirrors plastics
(with ``glass_transition_temperature``, ``heat_deflection_temperature``,
``elongation_at_break``), except hardness is a dedicated ``shore_hardness`` field
-- photopolymers are quoted on the Shore scale, so its unit is fixed (Shore D for
all current families) via ``PROPERTY_UNITS`` rather than a per-material
``hardness_scale``.

``yield_strength`` ~equals tensile strength (cast photopolymers fail with little
distinct yielding). Standalone: does not touch the point-value library or the
finishes/PBR stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ranges import Range, RangeMaterial


@dataclass(frozen=True)
class Material(RangeMaterial):
    """A photopolymer resin described by typical-value ranges.

    ``density`` is a single value; the rest are ``Range`` bands (or ``None`` if
    the value is missing, or ``NOT_SUITABLE`` if the property does not apply).
    """

    name: str
    density: float  # kg/m³ (single representative value)
    tensile_strength: Range | None  # MPa
    yield_strength: Range | None  # MPa
    modulus_of_elasticity: Range | None  # GPa
    shear_modulus: Range | None  # GPa
    poisson_ratio: Range | None  # dimensionless
    shear_strength: Range | None  # MPa
    elongation_at_break: Range | None  # %
    shore_hardness: Range | None  # Shore D
    specific_heat_capacity: Range | None  # J/(kg·K)
    glass_transition_temperature: Range | None  # °C
    heat_deflection_temperature: Range | None  # °C
    max_service_temp: Range | None  # °C (engineering guide limit, not a hard max)
    thermal_expansion: Range | None  # 1/K
    thermal_conductivity: Range | None  # W/(m·K)


RESIN_STANDARD = Material(
    name="RESIN_STANDARD",
    density=1150,
    tensile_strength=Range(45, 60),
    yield_strength=Range(42, 55),
    modulus_of_elasticity=Range(2.4, 3.2),
    shear_modulus=Range(0.85, 1.15),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(27, 36),
    elongation_at_break=Range(5, 12),
    shore_hardness=Range(80, 86),
    specific_heat_capacity=Range(1400, 1600),
    glass_transition_temperature=Range(50, 65),
    heat_deflection_temperature=Range(50, 65),
    max_service_temp=Range(45, 55),
    thermal_expansion=Range(80e-6, 130e-6),
    thermal_conductivity=Range(0.18, 0.25),
)

RESIN_TOUGH = Material(
    name="RESIN_TOUGH",
    density=1150,
    tensile_strength=Range(40, 55),
    yield_strength=Range(35, 48),
    modulus_of_elasticity=Range(2.0, 2.8),
    shear_modulus=Range(0.7, 1.0),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(24, 33),
    elongation_at_break=Range(20, 60),
    shore_hardness=Range(78, 84),
    specific_heat_capacity=Range(1400, 1600),
    glass_transition_temperature=Range(45, 60),
    heat_deflection_temperature=Range(45, 58),
    max_service_temp=Range(40, 55),
    thermal_expansion=Range(90e-6, 150e-6),
    thermal_conductivity=Range(0.18, 0.25),
)

RESIN_HIGH_TEMP = Material(
    name="RESIN_HIGH_TEMP",
    density=1300,
    tensile_strength=Range(40, 55),
    yield_strength=Range(38, 50),
    modulus_of_elasticity=Range(2.8, 3.6),
    shear_modulus=Range(1.0, 1.3),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(24, 33),
    elongation_at_break=Range(3, 10),
    shore_hardness=Range(80, 86),
    specific_heat_capacity=Range(1400, 1600),
    glass_transition_temperature=Range(110, 160),
    heat_deflection_temperature=Range(100, 150),
    max_service_temp=Range(90, 130),
    thermal_expansion=Range(70e-6, 120e-6),
    thermal_conductivity=Range(0.18, 0.25),
)

RESIN_CERAMIC = Material(
    name="RESIN_CERAMIC",
    density=1650,
    tensile_strength=Range(60, 80),
    yield_strength=Range(55, 72),
    modulus_of_elasticity=Range(8, 12),
    shear_modulus=Range(3.0, 4.5),
    poisson_ratio=Range(0.30, 0.35),
    shear_strength=Range(36, 48),
    elongation_at_break=Range(1, 3),
    shore_hardness=Range(88, 95),
    specific_heat_capacity=Range(1100, 1300),
    glass_transition_temperature=Range(150, 250),
    heat_deflection_temperature=Range(200, 270),
    max_service_temp=Range(150, 220),
    thermal_expansion=Range(30e-6, 70e-6),
    thermal_conductivity=Range(0.2, 0.5),
)

RESIN_CASTABLE = Material(
    name="RESIN_CASTABLE",
    density=1150,
    tensile_strength=Range(35, 50),
    yield_strength=Range(32, 45),
    modulus_of_elasticity=Range(2.2, 3.0),
    shear_modulus=Range(0.8, 1.1),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(21, 30),
    elongation_at_break=Range(3, 10),
    shore_hardness=Range(76, 83),
    specific_heat_capacity=Range(1400, 1600),
    glass_transition_temperature=Range(48, 62),
    heat_deflection_temperature=Range(48, 62),
    max_service_temp=Range(40, 55),
    thermal_expansion=Range(90e-6, 150e-6),
    thermal_conductivity=Range(0.18, 0.25),
)

RESIN_ESD = Material(
    name="RESIN_ESD",
    density=1300,
    tensile_strength=Range(38, 50),
    yield_strength=Range(35, 46),
    modulus_of_elasticity=Range(1.6, 2.4),
    shear_modulus=Range(0.55, 0.85),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(23, 30),
    elongation_at_break=Range(5, 15),
    shore_hardness=Range(85, 92),
    specific_heat_capacity=Range(1400, 1600),
    glass_transition_temperature=Range(55, 70),
    heat_deflection_temperature=Range(55, 70),
    max_service_temp=Range(45, 60),
    thermal_expansion=Range(80e-6, 130e-6),
    thermal_conductivity=Range(0.18, 0.25),
)

RESIN_TRANSPARENT = Material(
    name="RESIN_TRANSPARENT",
    density=1300,
    tensile_strength=Range(38, 52),
    yield_strength=Range(35, 48),
    modulus_of_elasticity=Range(1.6, 2.4),
    shear_modulus=Range(0.55, 0.85),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(23, 31),
    elongation_at_break=Range(5, 15),
    shore_hardness=Range(80, 88),
    specific_heat_capacity=Range(1400, 1600),
    glass_transition_temperature=Range(45, 62),
    heat_deflection_temperature=Range(45, 60),
    max_service_temp=Range(40, 55),
    thermal_expansion=Range(80e-6, 130e-6),
    thermal_conductivity=Range(0.18, 0.25),
)


ALL_RESINS = (
    RESIN_STANDARD,
    RESIN_TOUGH,
    RESIN_HIGH_TEMP,
    RESIN_CERAMIC,
    RESIN_CASTABLE,
    RESIN_ESD,
    RESIN_TRANSPARENT,
)


if __name__ == "__main__":
    print(f"resins: {len(ALL_RESINS)}")
    print()
    print(RESIN_STANDARD.describe())
    print(RESIN_CERAMIC.describe())

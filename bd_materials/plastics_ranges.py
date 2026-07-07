"""Range-based typical values for plastics.

Sibling of ``metals_ranges`` using the same approach: every property is a
**min–max range** (see that module for the rationale -- common-knowledge bands
avoid the vendor/licensing trap and are honest about variation). ``density`` is a
single representative value; everything else is a ``Range``. Units are fixed per
property (``PROPERTY_UNITS``).

Same property set as metals, except ``melting_temperature`` is replaced by
``glass_transition_temperature`` (Tg is the transition that governs polymer
service), plus two plastics-specific ones: ``heat_deflection_temperature`` (°C)
and ``elongation_at_break`` (%).

Missing vs not-applicable. A ``Range`` field can also be:

* ``None`` -- the value is **missing** (not yet filled in).
* ``NOT_SUITABLE`` (``Range(nan, nan)``) -- the property **does not apply**. Used
  for: elastomers' ``yield_strength`` and ``heat_deflection_temperature`` (TPU,
  rubber); ``yield_strength`` of the thermoset-laminate / continuous-fibre grades
  (phenolic, FR4, CFRP), which have no isotropic yield; and PTFE's
  ``glass_transition_temperature`` (not usefully single-valued for PTFE).

Other conventions where a metals field maps awkwardly onto polymers:

* ``yield_strength`` -- for brittle *thermoplastics* and short-fibre-filled
  grades (PMMA, PLA-CF, PETG-CF, PPS-CF) that fracture with little yielding, this
  ~equals tensile strength.
* ``hardness`` -- ``hardness_scale`` is "Shore D" for rigid plastics, "Shore A"
  for elastomers. Composites use Shore D as a rough proxy.

Vendor-neutral: the Stratasys ABS-ESD7 grade from the old library is omitted.

Standalone: does not touch the point-value library or the finishes/PBR stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ranges import NOT_SUITABLE, Range, RangeMaterial


@dataclass(frozen=True)
class Material(RangeMaterial):
    """A plastic described by typical-value ranges.

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
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "Shore D", "Shore A", ...
    specific_heat_capacity: Range | None  # J/(kg·K)
    glass_transition_temperature: Range | None  # °C
    heat_deflection_temperature: Range | None  # °C
    max_service_temp: Range | None  # °C (engineering guide limit, not a hard max)
    thermal_expansion: Range | None  # 1/K
    thermal_conductivity: Range | None  # W/(m·K)


# ===========================================================================
# PLA (+ carbon-filled composite)
# ===========================================================================

PLA_GENERIC = Material(
    name="PLA_GENERIC",
    density=1240,
    tensile_strength=Range(45, 70),
    yield_strength=Range(45, 60),
    modulus_of_elasticity=Range(3.0, 3.9),
    shear_modulus=Range(1.2, 1.5),
    poisson_ratio=Range(0.35, 0.40),
    shear_strength=Range(30, 55),
    elongation_at_break=Range(3, 7),
    hardness=Range(78, 85),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1800, 1900),
    glass_transition_temperature=Range(55, 65),
    heat_deflection_temperature=Range(50, 60),
    max_service_temp=Range(45, 55),
    thermal_expansion=Range(60e-6, 90e-6),
    thermal_conductivity=Range(0.11, 0.16),
)

PLA_CARBON_FILLED = Material(
    name="PLA_CARBON_FILLED",
    density=1250,
    tensile_strength=Range(40, 65),
    yield_strength=Range(40, 55),
    modulus_of_elasticity=Range(4.0, 7.0),
    shear_modulus=Range(2.0, 3.5),
    poisson_ratio=Range(0.35, 0.40),
    shear_strength=Range(30, 50),
    elongation_at_break=Range(1, 3),
    hardness=Range(80, 88),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1500, 1700),
    glass_transition_temperature=Range(55, 65),
    heat_deflection_temperature=Range(55, 70),
    max_service_temp=Range(50, 60),
    thermal_expansion=Range(25e-6, 50e-6),
    thermal_conductivity=Range(0.15, 0.30),
)


# ===========================================================================
# ABS (Stratasys ABS-ESD7 omitted for vendor neutrality)
# ===========================================================================

ABS_GENERIC = Material(
    name="ABS_GENERIC",
    density=1050,
    tensile_strength=Range(30, 50),
    yield_strength=Range(30, 45),
    modulus_of_elasticity=Range(1.8, 2.5),
    shear_modulus=Range(0.7, 0.9),
    poisson_ratio=Range(0.35, 0.40),
    shear_strength=Range(20, 35),
    elongation_at_break=Range(5, 25),
    hardness=Range(70, 80),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1300, 1500),
    glass_transition_temperature=Range(100, 110),
    heat_deflection_temperature=Range(75, 95),
    max_service_temp=Range(60, 80),
    thermal_expansion=Range(80e-6, 110e-6),
    thermal_conductivity=Range(0.15, 0.20),
)

ABS_FLAME_RETARDANT = Material(
    name="ABS_FLAME_RETARDANT",
    density=1200,
    tensile_strength=Range(30, 45),
    yield_strength=Range(30, 42),
    modulus_of_elasticity=Range(2.0, 2.6),
    shear_modulus=Range(0.75, 0.95),
    poisson_ratio=Range(0.35, 0.40),
    shear_strength=Range(22, 38),
    elongation_at_break=Range(5, 20),
    hardness=Range(72, 82),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1300, 1500),
    glass_transition_temperature=Range(100, 110),
    heat_deflection_temperature=Range(75, 90),
    max_service_temp=Range(60, 75),
    thermal_expansion=Range(80e-6, 110e-6),
    thermal_conductivity=Range(0.15, 0.22),
)


# ===========================================================================
# Nylon (PA) -- includes a powder-bed printed variant + glass-filled composite
# ===========================================================================

PA6 = Material(
    name="PA6",
    density=1140,
    tensile_strength=Range(50, 90),
    yield_strength=Range(45, 85),
    modulus_of_elasticity=Range(2.0, 3.5),
    shear_modulus=Range(0.8, 1.3),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(30, 60),
    elongation_at_break=Range(20, 150),
    hardness=Range(75, 85),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1600, 1700),
    glass_transition_temperature=Range(45, 60),
    heat_deflection_temperature=Range(60, 100),
    max_service_temp=Range(80, 100),
    thermal_expansion=Range(70e-6, 100e-6),
    thermal_conductivity=Range(0.24, 0.30),
)

PA12 = Material(
    name="PA12",
    density=1010,
    tensile_strength=Range(40, 55),
    yield_strength=Range(40, 50),
    modulus_of_elasticity=Range(1.2, 1.8),
    shear_modulus=Range(0.5, 0.8),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(25, 40),
    elongation_at_break=Range(50, 300),
    hardness=Range(70, 80),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1700, 1800),
    glass_transition_temperature=Range(40, 50),
    heat_deflection_temperature=Range(45, 80),
    max_service_temp=Range(70, 95),
    thermal_expansion=Range(100e-6, 150e-6),
    thermal_conductivity=Range(0.23, 0.28),
)

# Generic powder-bed PA12 (covers SLS and MJF-class high-speed sintering); the
# bands span both processes.
PA12_SINTERED = Material(
    name="PA12_SINTERED",
    density=1000,
    tensile_strength=Range(45, 50),
    yield_strength=Range(40, 48),
    modulus_of_elasticity=Range(1.5, 1.9),
    shear_modulus=Range(0.5, 0.75),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(25, 40),
    elongation_at_break=Range(5, 25),
    hardness=Range(70, 80),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1700, 1800),
    glass_transition_temperature=Range(40, 50),
    heat_deflection_temperature=Range(70, 95),
    max_service_temp=Range(80, 110),
    thermal_expansion=Range(90e-6, 150e-6),
    thermal_conductivity=Range(0.2, 0.3),
)

PA12_GF35 = Material(
    name="PA12_GF35",
    density=1300,
    tensile_strength=Range(40, 70),
    yield_strength=Range(40, 65),
    modulus_of_elasticity=Range(2.5, 4.5),
    shear_modulus=Range(1.0, 1.8),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(30, 50),
    elongation_at_break=Range(3, 10),
    hardness=Range(78, 85),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1200, 1400),
    glass_transition_temperature=Range(40, 50),
    heat_deflection_temperature=Range(140, 175),
    max_service_temp=Range(100, 140),
    thermal_expansion=Range(40e-6, 80e-6),
    thermal_conductivity=Range(0.25, 0.40),
)


# ===========================================================================
# PEEK -- molded + printed
# ===========================================================================

PEEK_MOLDED = Material(
    name="PEEK_MOLDED",
    density=1300,
    tensile_strength=Range(90, 110),
    yield_strength=Range(90, 100),
    modulus_of_elasticity=Range(3.5, 4.2),
    shear_modulus=Range(1.3, 1.6),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(50, 75),
    elongation_at_break=Range(20, 60),
    hardness=Range(85, 90),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1300, 1400),
    glass_transition_temperature=Range(143, 150),
    heat_deflection_temperature=Range(140, 160),
    max_service_temp=Range(240, 260),
    thermal_expansion=Range(45e-6, 60e-6),
    thermal_conductivity=Range(0.24, 0.29),
)

PEEK_PRINTED = Material(
    name="PEEK_PRINTED",
    density=1300,
    tensile_strength=Range(80, 100),
    yield_strength=Range(80, 95),
    modulus_of_elasticity=Range(3.5, 4.2),
    shear_modulus=Range(1.3, 1.6),
    poisson_ratio=Range(0.38, 0.42),
    shear_strength=Range(45, 70),
    elongation_at_break=Range(5, 30),
    hardness=Range(85, 90),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1300, 1400),
    glass_transition_temperature=Range(143, 150),
    heat_deflection_temperature=Range(140, 160),
    max_service_temp=Range(200, 250),
    thermal_expansion=Range(45e-6, 60e-6),
    thermal_conductivity=Range(0.24, 0.29),
)


# ===========================================================================
# TPU -- cast/extruded + sintered (elastomers; yield/HDT are nominal)
# ===========================================================================

TPU_95A = Material(
    name="TPU_95A",
    density=1200,
    tensile_strength=Range(25, 55),
    yield_strength=NOT_SUITABLE,
    modulus_of_elasticity=Range(0.01, 0.05),
    shear_modulus=Range(0.003, 0.02),
    poisson_ratio=Range(0.45, 0.49),
    shear_strength=Range(10, 30),
    elongation_at_break=Range(300, 700),
    hardness=Range(93, 97),
    hardness_scale="Shore A",
    specific_heat_capacity=Range(1700, 1900),
    glass_transition_temperature=Range(-40, -20),
    heat_deflection_temperature=NOT_SUITABLE,
    max_service_temp=Range(70, 90),
    thermal_expansion=Range(120e-6, 200e-6),
    thermal_conductivity=Range(0.15, 0.25),
)

TPU_SINTERED = Material(
    name="TPU_SINTERED",
    density=1200,
    tensile_strength=Range(5, 25),
    yield_strength=NOT_SUITABLE,
    modulus_of_elasticity=Range(0.02, 0.1),
    shear_modulus=Range(0.007, 0.03),
    poisson_ratio=Range(0.45, 0.49),
    shear_strength=Range(5, 20),
    elongation_at_break=Range(100, 400),
    hardness=Range(88, 92),
    hardness_scale="Shore A",
    specific_heat_capacity=Range(1700, 1900),
    glass_transition_temperature=Range(-40, -20),
    heat_deflection_temperature=NOT_SUITABLE,
    max_service_temp=Range(70, 90),
    thermal_expansion=Range(120e-6, 200e-6),
    thermal_conductivity=Range(0.15, 0.25),
)


# ===========================================================================
# Single-variant thermoplastics
# ===========================================================================

PC = Material(
    name="PC",
    density=1200,
    tensile_strength=Range(55, 75),
    yield_strength=Range(55, 70),
    modulus_of_elasticity=Range(2.2, 2.5),
    shear_modulus=Range(0.8, 0.95),
    poisson_ratio=Range(0.37, 0.42),
    shear_strength=Range(35, 50),
    elongation_at_break=Range(80, 130),
    hardness=Range(75, 85),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1150, 1250),
    glass_transition_temperature=Range(145, 150),
    heat_deflection_temperature=Range(125, 140),
    max_service_temp=Range(115, 130),
    thermal_expansion=Range(65e-6, 75e-6),
    thermal_conductivity=Range(0.19, 0.22),
)

PP = Material(
    name="PP",
    density=905,
    tensile_strength=Range(25, 40),
    yield_strength=Range(25, 38),
    modulus_of_elasticity=Range(1.1, 1.8),
    shear_modulus=Range(0.4, 0.7),
    poisson_ratio=Range(0.40, 0.45),
    shear_strength=Range(15, 30),
    elongation_at_break=Range(100, 600),
    hardness=Range(70, 80),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1800, 2000),
    glass_transition_temperature=Range(-20, -10),
    heat_deflection_temperature=Range(50, 65),
    max_service_temp=Range(80, 105),
    thermal_expansion=Range(100e-6, 180e-6),
    thermal_conductivity=Range(0.11, 0.22),
)

POM = Material(
    name="POM",
    density=1410,
    tensile_strength=Range(60, 75),
    yield_strength=Range(60, 70),
    modulus_of_elasticity=Range(2.8, 3.6),
    shear_modulus=Range(1.0, 1.4),
    poisson_ratio=Range(0.35, 0.40),
    shear_strength=Range(35, 55),
    elongation_at_break=Range(10, 45),
    hardness=Range(80, 90),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1400, 1500),
    glass_transition_temperature=Range(-60, -50),
    heat_deflection_temperature=Range(90, 110),
    max_service_temp=Range(90, 105),
    thermal_expansion=Range(100e-6, 130e-6),
    thermal_conductivity=Range(0.30, 0.40),
)

PTFE = Material(
    name="PTFE",
    density=2170,
    tensile_strength=Range(20, 35),
    yield_strength=Range(15, 25),
    modulus_of_elasticity=Range(0.4, 0.75),
    shear_modulus=Range(0.15, 0.28),
    poisson_ratio=Range(0.42, 0.47),
    shear_strength=Range(10, 20),
    elongation_at_break=Range(200, 400),
    hardness=Range(50, 65),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1000, 1050),
    glass_transition_temperature=NOT_SUITABLE,
    heat_deflection_temperature=Range(50, 80),
    max_service_temp=Range(250, 270),
    thermal_expansion=Range(100e-6, 160e-6),
    thermal_conductivity=Range(0.23, 0.27),
)

PMMA = Material(
    name="PMMA",
    density=1180,
    tensile_strength=Range(50, 77),
    yield_strength=Range(50, 72),
    modulus_of_elasticity=Range(2.4, 3.3),
    shear_modulus=Range(0.9, 1.2),
    poisson_ratio=Range(0.35, 0.40),
    shear_strength=Range(30, 50),
    elongation_at_break=Range(2, 6),
    hardness=Range(85, 90),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1400, 1500),
    glass_transition_temperature=Range(100, 110),
    heat_deflection_temperature=Range(85, 105),
    max_service_temp=Range(65, 80),
    thermal_expansion=Range(60e-6, 90e-6),
    thermal_conductivity=Range(0.17, 0.21),
)

PE = Material(
    name="PE",
    density=960,
    tensile_strength=Range(20, 35),
    yield_strength=Range(20, 30),
    modulus_of_elasticity=Range(0.8, 1.3),
    shear_modulus=Range(0.3, 0.5),
    poisson_ratio=Range(0.40, 0.46),
    shear_strength=Range(12, 25),
    elongation_at_break=Range(100, 700),
    hardness=Range(55, 65),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1800, 2100),
    glass_transition_temperature=Range(-120, -100),
    heat_deflection_temperature=Range(40, 55),
    max_service_temp=Range(60, 90),
    thermal_expansion=Range(100e-6, 200e-6),
    thermal_conductivity=Range(0.35, 0.50),
)


# ===========================================================================
# Thermosets & elastomers
# ===========================================================================

PHENOLIC_BAKELITE = Material(
    name="PHENOLIC_BAKELITE",
    density=1300,
    tensile_strength=Range(40, 70),
    yield_strength=NOT_SUITABLE,
    modulus_of_elasticity=Range(5, 9),
    shear_modulus=Range(2.0, 3.5),
    poisson_ratio=Range(0.30, 0.40),
    shear_strength=Range(25, 45),
    elongation_at_break=Range(0.5, 2),
    hardness=Range(88, 95),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1200, 1600),
    glass_transition_temperature=Range(150, 200),
    heat_deflection_temperature=Range(150, 200),
    max_service_temp=Range(120, 180),
    thermal_expansion=Range(30e-6, 50e-6),
    thermal_conductivity=Range(0.15, 0.30),
)

RUBBER = Material(
    name="RUBBER",
    density=1200,
    tensile_strength=Range(10, 25),
    yield_strength=NOT_SUITABLE,
    modulus_of_elasticity=Range(0.001, 0.01),
    shear_modulus=Range(0.0003, 0.003),
    poisson_ratio=Range(0.48, 0.50),
    shear_strength=Range(5, 15),
    elongation_at_break=Range(100, 700),
    hardness=Range(40, 80),
    hardness_scale="Shore A",
    specific_heat_capacity=Range(1800, 2000),
    glass_transition_temperature=Range(-70, -40),
    heat_deflection_temperature=NOT_SUITABLE,
    max_service_temp=Range(60, 100),
    thermal_expansion=Range(100e-6, 200e-6),
    thermal_conductivity=Range(0.13, 0.30),
)


# ===========================================================================
# Fibre-reinforced composites
# ===========================================================================

PETG_CF = Material(
    name="PETG_CF",
    density=1270,
    tensile_strength=Range(40, 60),
    yield_strength=Range(40, 55),
    modulus_of_elasticity=Range(3, 6),
    shear_modulus=Range(1.2, 2.3),
    poisson_ratio=Range(0.37, 0.42),
    shear_strength=Range(25, 45),
    elongation_at_break=Range(2, 6),
    hardness=Range(78, 85),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1100, 1300),
    glass_transition_temperature=Range(75, 85),
    heat_deflection_temperature=Range(65, 80),
    max_service_temp=Range(60, 75),
    thermal_expansion=Range(30e-6, 60e-6),
    thermal_conductivity=Range(0.2, 0.4),
)

PPS_CF = Material(
    name="PPS_CF",
    density=1400,
    tensile_strength=Range(80, 150),
    yield_strength=Range(80, 140),
    modulus_of_elasticity=Range(7, 20),
    shear_modulus=Range(2.5, 7),
    poisson_ratio=Range(0.36, 0.40),
    shear_strength=Range(45, 90),
    elongation_at_break=Range(1, 3),
    hardness=Range(85, 92),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(1000, 1200),
    glass_transition_temperature=Range(85, 95),
    heat_deflection_temperature=Range(200, 270),
    max_service_temp=Range(200, 240),
    thermal_expansion=Range(20e-6, 50e-6),
    thermal_conductivity=Range(0.25, 0.45),
)

FR4 = Material(
    name="FR4",
    density=1850,
    tensile_strength=Range(280, 420),
    yield_strength=NOT_SUITABLE,
    modulus_of_elasticity=Range(18, 24),
    shear_modulus=Range(5, 9),
    poisson_ratio=Range(0.11, 0.18),
    shear_strength=Range(60, 120),
    elongation_at_break=Range(1, 3),
    hardness=Range(85, 90),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(600, 900),
    glass_transition_temperature=Range(130, 180),
    heat_deflection_temperature=Range(130, 180),
    max_service_temp=Range(120, 140),
    thermal_expansion=Range(12e-6, 18e-6),
    thermal_conductivity=Range(0.25, 0.35),
)

CFRP_PLATE = Material(
    name="CFRP_PLATE",
    density=1600,
    tensile_strength=Range(600, 2500),
    yield_strength=NOT_SUITABLE,
    modulus_of_elasticity=Range(50, 180),
    shear_modulus=Range(3, 8),
    poisson_ratio=Range(0.05, 0.15),
    shear_strength=Range(30, 90),
    elongation_at_break=Range(0.5, 2),
    hardness=Range(85, 90),
    hardness_scale="Shore D",
    specific_heat_capacity=Range(800, 1100),
    glass_transition_temperature=Range(100, 200),
    heat_deflection_temperature=Range(100, 200),
    max_service_temp=Range(100, 180),
    thermal_expansion=Range(0, 10e-6),
    thermal_conductivity=Range(1, 6),
)


# ===========================================================================
ALL_PLASTICS = (
    PLA_GENERIC,
    PLA_CARBON_FILLED,
    ABS_GENERIC,
    ABS_FLAME_RETARDANT,
    PA6,
    PA12,
    PA12_SINTERED,
    PA12_GF35,
    PEEK_MOLDED,
    PEEK_PRINTED,
    TPU_95A,
    TPU_SINTERED,
    PC,
    PP,
    POM,
    PTFE,
    PMMA,
    PE,
    PHENOLIC_BAKELITE,
    RUBBER,
    PETG_CF,
    PPS_CF,
    FR4,
    CFRP_PLATE,
)


if __name__ == "__main__":
    print(f"plastics: {len(ALL_PLASTICS)}")
    print()
    print(PLA_GENERIC.describe())
    print(PC.describe())
    print(TPU_95A.describe())

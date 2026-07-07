"""Range-based typical values for metals.

Sibling modules cover other material classes with the same approach (e.g. a
``plastics_ranges`` for plastics). Every mechanical/thermal property is a
**min–max range**, not a single point.
Two reasons:

* **No licensing / vendor trap.** A published band ("6061-T6 tensile ~290-320 MPa")
  is textbook common knowledge; a single precise figure copied from a datasheet is
  the thing that carries provenance/licensing risk.
* **Honesty about variation.** Real values scatter with temper, heat-treatment,
  product form, and (for AM) process. A range states that spread instead of
  pretending a single number is authoritative.

Units are **fixed per property** (see ``PROPERTY_UNITS``) -- they are an intrinsic
property of the quantity, defined once, not repeated on every material. ``density``
is a single representative value (its spread is small); everything else is a
``Range``.

Values seeded from common-knowledge typical-value bands. Where a source gave only
a rule (e.g. shear strength ~0.55-0.65 x tensile) or a family band rather than a
per-grade number, the range was estimated from that rule/band.

This module is standalone: it does not touch the existing point-value library
(``metals``/``plastics``/...) or the finishes/PBR stack.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ranges import Range, RangeMaterial


@dataclass(frozen=True)
class Material(RangeMaterial):
    """A metal described by typical-value ranges.

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
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "HB", "HRC", "HV", ...
    specific_heat_capacity: Range | None  # J/(kg·K)
    melting_temperature: Range | None  # °C
    max_service_temp: Range | None  # °C (engineering guide limit, not a hard max)
    thermal_expansion: Range | None  # 1/K
    thermal_conductivity: Range | None  # W/(m·K)


# ===========================================================================
# Wrought aluminums (Alu.*)
#   density per-grade; E/G/cp/melting/alpha/k are the family bands (narrowed
#   for AlSi10Mg AM). tensile/yield per-grade; shear_strength is the listed
#   value where given, else ~0.55-0.65 x tensile.
# ===========================================================================

Alu_G6061_T6 = Material(
    name="Alu_G6061_T6",
    density=2700,
    tensile_strength=Range(290, 320),
    yield_strength=Range(240, 280),
    modulus_of_elasticity=Range(66, 70),
    shear_modulus=Range(25, 28),
    shear_strength=Range(200, 210),
    specific_heat_capacity=Range(875, 950),
    melting_temperature=Range(570, 660),
    thermal_expansion=Range(22e-6, 24e-6),
    thermal_conductivity=Range(130, 180),
    poisson_ratio=Range(0.32, 0.35),
    hardness=Range(85, 100),
    hardness_scale="HB",
    max_service_temp=Range(80, 120),
)

Alu_G7075_T6 = Material(
    name="Alu_G7075_T6",
    density=2810,
    tensile_strength=Range(540, 600),
    yield_strength=Range(480, 510),
    modulus_of_elasticity=Range(68, 72),
    shear_modulus=Range(25, 28),
    shear_strength=Range(330, 350),
    specific_heat_capacity=Range(875, 950),
    melting_temperature=Range(480, 640),
    thermal_expansion=Range(22e-6, 24e-6),
    thermal_conductivity=Range(130, 180),
    poisson_ratio=Range(0.32, 0.35),
    hardness=Range(135, 160),
    hardness_scale="HB",
    max_service_temp=Range(80, 120),
)

Alu_G5052_H32 = Material(
    name="Alu_G5052_H32",
    density=2680,
    tensile_strength=Range(215, 250),
    yield_strength=Range(160, 190),
    modulus_of_elasticity=Range(68, 72),
    shear_modulus=Range(25, 28),
    shear_strength=Range(120, 160),
    specific_heat_capacity=Range(875, 950),
    melting_temperature=Range(570, 660),
    thermal_expansion=Range(22e-6, 24e-6),
    thermal_conductivity=Range(130, 180),
    poisson_ratio=Range(0.32, 0.35),
    hardness=Range(60, 80),
    hardness_scale="HB",
    max_service_temp=Range(80, 120),
)

Alu_G2A12_T4 = Material(
    name="Alu_G2A12_T4",
    density=2800,
    tensile_strength=Range(430, 480),
    yield_strength=Range(300, 340),
    modulus_of_elasticity=Range(68, 72),
    shear_modulus=Range(25, 28),
    shear_strength=Range(240, 310),
    specific_heat_capacity=Range(875, 950),
    melting_temperature=Range(570, 660),
    thermal_expansion=Range(22e-6, 24e-6),
    thermal_conductivity=Range(120, 190),
    poisson_ratio=Range(0.32, 0.35),
    hardness=Range(95, 120),
    hardness_scale="HB",
    max_service_temp=Range(80, 120),
)

Alu_ALSI10MG_AS_BUILT = Material(
    name="Alu_ALSI10MG_AS_BUILT",
    density=2670,
    tensile_strength=Range(250, 330),
    yield_strength=Range(160, 250),
    modulus_of_elasticity=Range(65, 72),
    shear_modulus=Range(25, 28),
    shear_strength=Range(140, 215),
    specific_heat_capacity=Range(875, 950),
    melting_temperature=Range(570, 600),
    thermal_expansion=Range(20e-6, 22e-6),
    thermal_conductivity=Range(100, 150),
    poisson_ratio=Range(0.32, 0.35),
    hardness=Range(80, 110),
    hardness_scale="HB",
    max_service_temp=Range(80, 150),
)

Alu_G2024_AEROSPACE = Material(
    name="Alu_G2024_AEROSPACE",
    density=2780,
    tensile_strength=Range(420, 470),
    yield_strength=Range(260, 320),
    modulus_of_elasticity=Range(70, 73),
    shear_modulus=Range(26, 28),
    shear_strength=Range(230, 280),
    specific_heat_capacity=Range(875, 950),
    melting_temperature=Range(500, 650),
    thermal_expansion=Range(21e-6, 24e-6),
    thermal_conductivity=Range(120, 130),
    poisson_ratio=Range(0.32, 0.35),
    hardness=Range(95, 120),
    hardness_scale="HB",
    max_service_temp=Range(80, 120),
)

ALUMINUMS = (
    Alu_G6061_T6,
    Alu_G7075_T6,
    Alu_G5052_H32,
    Alu_G2A12_T4,
    Alu_ALSI10MG_AS_BUILT,
    Alu_G2024_AEROSPACE,
)


# ===========================================================================
# Stainless steels (Stainless.*)
#   Austenitic (304/316L/303/201): E 190-205, G 73-80, cp 480-500, alpha
#   16-18e-6, k 14-16. Ferritic (430): alpha 11-12e-6, k 25-30.
#   shear_strength ~0.55-0.6 x tensile.
# ===========================================================================

Stainless_G304_ANNEALED = Material(
    name="Stainless_G304_ANNEALED",
    density=7930,
    tensile_strength=Range(515, 620),
    yield_strength=Range(205, 240),
    modulus_of_elasticity=Range(190, 205),
    shear_modulus=Range(73, 80),
    shear_strength=Range(280, 350),
    specific_heat_capacity=Range(480, 500),
    melting_temperature=Range(1400, 1450),
    thermal_expansion=Range(16e-6, 18e-6),
    thermal_conductivity=Range(14, 16),
    poisson_ratio=Range(0.29, 0.31),
    hardness=Range(150, 200),
    hardness_scale="HB",
    max_service_temp=Range(400, 600),
)

Stainless_G316L_ANNEALED = Material(
    name="Stainless_G316L_ANNEALED",
    density=8000,
    tensile_strength=Range(480, 620),
    yield_strength=Range(170, 240),
    modulus_of_elasticity=Range(190, 205),
    shear_modulus=Range(73, 80),
    shear_strength=Range(280, 350),
    specific_heat_capacity=Range(480, 500),
    melting_temperature=Range(1375, 1450),
    thermal_expansion=Range(16e-6, 18e-6),
    thermal_conductivity=Range(14, 16),
    poisson_ratio=Range(0.29, 0.31),
    hardness=Range(150, 200),
    hardness_scale="HB",
    max_service_temp=Range(400, 600),
)

Stainless_G316L_AS_BUILT = Material(
    name="Stainless_G316L_AS_BUILT",
    density=7990,
    tensile_strength=Range(600, 700),
    yield_strength=Range(450, 550),
    modulus_of_elasticity=Range(185, 200),
    shear_modulus=Range(73, 80),
    shear_strength=Range(330, 420),
    specific_heat_capacity=Range(480, 500),
    melting_temperature=Range(1375, 1450),
    thermal_expansion=Range(16e-6, 18e-6),
    thermal_conductivity=Range(14, 16),
    poisson_ratio=Range(0.29, 0.31),
    hardness=Range(200, 250),
    hardness_scale="HB",
    max_service_temp=Range(400, 600),
)

Stainless_G303_ANNEALED = Material(
    name="Stainless_G303_ANNEALED",
    density=8030,
    tensile_strength=Range(500, 600),
    yield_strength=Range(205, 240),
    modulus_of_elasticity=Range(190, 205),
    shear_modulus=Range(73, 80),
    shear_strength=Range(275, 360),
    specific_heat_capacity=Range(480, 500),
    melting_temperature=Range(1400, 1450),
    thermal_expansion=Range(16e-6, 18e-6),
    thermal_conductivity=Range(14, 16),
    poisson_ratio=Range(0.29, 0.31),
    hardness=Range(150, 200),
    hardness_scale="HB",
    max_service_temp=Range(400, 600),
)

Stainless_G430_ANNEALED = Material(
    name="Stainless_G430_ANNEALED",
    density=7750,
    tensile_strength=Range(450, 500),
    yield_strength=Range(275, 310),
    modulus_of_elasticity=Range(190, 205),
    shear_modulus=Range(73, 80),
    shear_strength=Range(250, 300),
    specific_heat_capacity=Range(480, 500),
    melting_temperature=Range(1425, 1510),
    thermal_expansion=Range(11e-6, 12e-6),
    thermal_conductivity=Range(25, 30),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(150, 190),
    hardness_scale="HB",
    max_service_temp=Range(400, 600),
)

Stainless_G201_ANNEALED = Material(
    name="Stainless_G201_ANNEALED",
    density=7860,
    tensile_strength=Range(600, 760),
    yield_strength=Range(275, 450),
    modulus_of_elasticity=Range(190, 205),
    shear_modulus=Range(73, 80),
    shear_strength=Range(380, 515),
    specific_heat_capacity=Range(480, 500),
    melting_temperature=Range(1400, 1450),
    thermal_expansion=Range(16e-6, 18e-6),
    thermal_conductivity=Range(14, 16),
    poisson_ratio=Range(0.29, 0.31),
    hardness=Range(180, 230),
    hardness_scale="HB",
    max_service_temp=Range(400, 600),
)

STAINLESS_STEELS = (
    Stainless_G304_ANNEALED,
    Stainless_G316L_ANNEALED,
    Stainless_G316L_AS_BUILT,
    Stainless_G303_ANNEALED,
    Stainless_G430_ANNEALED,
    Stainless_G201_ANNEALED,
)


# ===========================================================================
# Mild / low-alloy / spring steels
#   density 7850, E 200-210, G 80-81, cp 460-490, melting 1450-1530,
#   alpha 11-13e-6. k: plain carbon 45-55, alloy 30-45.
#   shear_strength ~0.57 x tensile (static design rule).
# ===========================================================================

MildSteel_G1018_COLD_DRAWN = Material(
    name="MildSteel_G1018_COLD_DRAWN",
    density=7850,
    tensile_strength=Range(440, 480),
    yield_strength=Range(345, 380),
    modulus_of_elasticity=Range(200, 210),
    shear_modulus=Range(80, 81),
    shear_strength=Range(250, 275),
    specific_heat_capacity=Range(460, 490),
    melting_temperature=Range(1450, 1530),
    thermal_expansion=Range(11e-6, 13e-6),
    thermal_conductivity=Range(45, 55),
    poisson_ratio=Range(0.28, 0.3),
    hardness=Range(120, 160),
    hardness_scale="HB",
    max_service_temp=Range(200, 500),
)

MildSteel_G1045_COLD_DRAWN = Material(
    name="MildSteel_G1045_COLD_DRAWN",
    density=7850,
    tensile_strength=Range(620, 690),
    yield_strength=Range(480, 550),
    modulus_of_elasticity=Range(200, 210),
    shear_modulus=Range(80, 81),
    shear_strength=Range(355, 395),
    specific_heat_capacity=Range(460, 490),
    melting_temperature=Range(1450, 1530),
    thermal_expansion=Range(11e-6, 13e-6),
    thermal_conductivity=Range(45, 55),
    poisson_ratio=Range(0.28, 0.3),
    hardness=Range(170, 210),
    hardness_scale="HB",
    max_service_temp=Range(200, 500),
)

MildSteel_GA36_HOT_ROLLED = Material(
    name="MildSteel_GA36_HOT_ROLLED",
    density=7850,
    tensile_strength=Range(400, 550),
    yield_strength=Range(250, 350),
    modulus_of_elasticity=Range(200, 210),
    shear_modulus=Range(80, 81),
    shear_strength=Range(230, 315),
    specific_heat_capacity=Range(460, 490),
    melting_temperature=Range(1450, 1530),
    thermal_expansion=Range(11e-6, 13e-6),
    thermal_conductivity=Range(45, 55),
    poisson_ratio=Range(0.28, 0.3),
    hardness=Range(120, 180),
    hardness_scale="HB",
    max_service_temp=Range(200, 500),
)

AlloySteel_G4140_QUENCHED_TEMPERED = Material(
    name="AlloySteel_G4140_QUENCHED_TEMPERED",
    density=7850,
    tensile_strength=Range(800, 1100),
    yield_strength=Range(650, 950),
    modulus_of_elasticity=Range(200, 210),
    shear_modulus=Range(80, 81),
    shear_strength=Range(455, 630),
    specific_heat_capacity=Range(460, 490),
    melting_temperature=Range(1450, 1530),
    thermal_expansion=Range(11e-6, 13e-6),
    thermal_conductivity=Range(30, 45),
    poisson_ratio=Range(0.28, 0.3),
    hardness=Range(28, 40),
    hardness_scale="HRC",
    max_service_temp=Range(200, 500),
)

AlloySteel_G4340_QUENCHED_TEMPERED = Material(
    name="AlloySteel_G4340_QUENCHED_TEMPERED",
    density=7850,
    tensile_strength=Range(980, 1200),
    yield_strength=Range(850, 1080),
    modulus_of_elasticity=Range(200, 210),
    shear_modulus=Range(80, 81),
    shear_strength=Range(560, 685),
    specific_heat_capacity=Range(460, 490),
    melting_temperature=Range(1450, 1530),
    thermal_expansion=Range(11e-6, 13e-6),
    thermal_conductivity=Range(30, 45),
    poisson_ratio=Range(0.28, 0.3),
    hardness=Range(35, 45),
    hardness_scale="HRC",
    max_service_temp=Range(200, 500),
)

AlloySteel_G1215_COLD_DRAWN = Material(
    name="AlloySteel_G1215_COLD_DRAWN",
    density=7850,
    tensile_strength=Range(440, 550),
    yield_strength=Range(340, 380),
    modulus_of_elasticity=Range(200, 210),
    shear_modulus=Range(80, 81),
    shear_strength=Range(250, 315),
    specific_heat_capacity=Range(460, 490),
    melting_temperature=Range(1450, 1530),
    thermal_expansion=Range(11e-6, 13e-6),
    thermal_conductivity=Range(45, 55),
    poisson_ratio=Range(0.28, 0.3),
    hardness=Range(120, 160),
    hardness_scale="HB",
    max_service_temp=Range(200, 500),
)

SpringSteel_GENERIC_QUENCHED_TEMPERED = Material(
    name="SpringSteel_GENERIC_QUENCHED_TEMPERED",
    density=7850,
    tensile_strength=Range(1000, 1500),
    yield_strength=Range(850, 1350),
    modulus_of_elasticity=Range(200, 210),
    shear_modulus=Range(80, 81),
    shear_strength=Range(570, 855),
    specific_heat_capacity=Range(460, 490),
    melting_temperature=Range(1450, 1530),
    thermal_expansion=Range(11e-6, 13e-6),
    thermal_conductivity=Range(30, 45),
    poisson_ratio=Range(0.28, 0.3),
    hardness=Range(40, 55),
    hardness_scale="HRC",
    max_service_temp=Range(150, 300),
)

MILD_STEELS = (
    MildSteel_G1018_COLD_DRAWN,
    MildSteel_G1045_COLD_DRAWN,
    MildSteel_GA36_HOT_ROLLED,
)
ALLOY_STEELS = (
    AlloySteel_G4140_QUENCHED_TEMPERED,
    AlloySteel_G4340_QUENCHED_TEMPERED,
    AlloySteel_G1215_COLD_DRAWN,
)
SPRING_STEELS = (SpringSteel_GENERIC_QUENCHED_TEMPERED,)


# ===========================================================================
# Tool steels (ToolSteel.*)  -- hardened states
#   density per-grade (~7700-7860), E 200-215, G 80-83, cp 460-500,
#   melting 1450-1520, alpha 12-13e-6, k 20-35 (grade-specific band).
#   yield rarely tabulated distinct from UTS in hardened states -> DERIVED
#   (~0.85-0.95 x UTS). shear_strength DERIVED (~0.57 x UTS).
# ===========================================================================

ToolSteel_D2_HARDENED = Material(
    name="ToolSteel_D2_HARDENED",
    density=7700,
    tensile_strength=Range(1500, 2000),
    yield_strength=Range(1300, 1900),
    modulus_of_elasticity=Range(200, 215),
    shear_modulus=Range(80, 83),
    shear_strength=Range(855, 1140),
    specific_heat_capacity=Range(460, 500),
    melting_temperature=Range(1450, 1520),
    thermal_expansion=Range(12e-6, 13e-6),
    thermal_conductivity=Range(18, 25),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(55, 62),
    hardness_scale="HRC",
    max_service_temp=Range(200, 350),
)

ToolSteel_A2_HARDENED = Material(
    name="ToolSteel_A2_HARDENED",
    density=7860,
    tensile_strength=Range(1400, 1900),
    yield_strength=Range(1200, 1800),
    modulus_of_elasticity=Range(200, 215),
    shear_modulus=Range(80, 83),
    shear_strength=Range(800, 1085),
    specific_heat_capacity=Range(460, 500),
    melting_temperature=Range(1450, 1520),
    thermal_expansion=Range(12e-6, 13e-6),
    thermal_conductivity=Range(20, 28),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(55, 60),
    hardness_scale="HRC",
    max_service_temp=Range(200, 350),
)

ToolSteel_O1_HARDENED = Material(
    name="ToolSteel_O1_HARDENED",
    density=7830,
    tensile_strength=Range(1400, 1900),
    yield_strength=Range(1200, 1800),
    modulus_of_elasticity=Range(200, 215),
    shear_modulus=Range(80, 83),
    shear_strength=Range(800, 1085),
    specific_heat_capacity=Range(460, 500),
    melting_temperature=Range(1450, 1520),
    thermal_expansion=Range(12e-6, 13e-6),
    thermal_conductivity=Range(30, 40),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(55, 60),
    hardness_scale="HRC",
    max_service_temp=Range(200, 350),
)

ToolSteel_A3_HARDENED = Material(
    name="ToolSteel_A3_HARDENED",
    density=7860,
    tensile_strength=Range(1400, 1900),
    yield_strength=Range(1200, 1800),
    modulus_of_elasticity=Range(200, 215),
    shear_modulus=Range(80, 83),
    shear_strength=Range(800, 1085),
    specific_heat_capacity=Range(460, 500),
    melting_temperature=Range(1450, 1520),
    thermal_expansion=Range(12e-6, 13e-6),
    thermal_conductivity=Range(32, 40),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(55, 60),
    hardness_scale="HRC",
    max_service_temp=Range(200, 350),
)

ToolSteel_S7_HARDENED = Material(
    name="ToolSteel_S7_HARDENED",
    density=7830,
    tensile_strength=Range(1400, 1800),
    yield_strength=Range(1200, 1700),
    modulus_of_elasticity=Range(200, 215),
    shear_modulus=Range(80, 83),
    shear_strength=Range(800, 1025),
    specific_heat_capacity=Range(460, 500),
    melting_temperature=Range(1450, 1520),
    thermal_expansion=Range(12e-6, 13e-6),
    thermal_conductivity=Range(30, 40),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(50, 56),
    hardness_scale="HRC",
    max_service_temp=Range(200, 350),
)

ToolSteel_H13_HARDENED = Material(
    name="ToolSteel_H13_HARDENED",
    density=7800,
    tensile_strength=Range(1300, 1600),
    yield_strength=Range(1100, 1500),
    modulus_of_elasticity=Range(200, 215),
    shear_modulus=Range(80, 83),
    shear_strength=Range(740, 912),
    specific_heat_capacity=Range(460, 500),
    melting_temperature=Range(1450, 1520),
    thermal_expansion=Range(12e-6, 13e-6),
    thermal_conductivity=Range(22, 28),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(44, 52),
    hardness_scale="HRC",
    max_service_temp=Range(500, 650),
)

ToolSteel_GENERIC_AS_BUILT = Material(
    name="ToolSteel_GENERIC_AS_BUILT",
    density=7800,
    tensile_strength=Range(1000, 1400),
    yield_strength=Range(850, 1300),
    modulus_of_elasticity=Range(200, 215),
    shear_modulus=Range(80, 83),
    shear_strength=Range(570, 800),
    specific_heat_capacity=Range(460, 500),
    melting_temperature=Range(1450, 1520),
    thermal_expansion=Range(12e-6, 13e-6),
    thermal_conductivity=Range(18, 28),
    poisson_ratio=Range(0.27, 0.3),
    hardness=Range(45, 60),
    hardness_scale="HRC",
    max_service_temp=Range(200, 350),
)

TOOL_STEELS = (
    ToolSteel_D2_HARDENED,
    ToolSteel_A2_HARDENED,
    ToolSteel_O1_HARDENED,
    ToolSteel_A3_HARDENED,
    ToolSteel_S7_HARDENED,
    ToolSteel_H13_HARDENED,
    ToolSteel_GENERIC_AS_BUILT,
)


# ===========================================================================
# Titanium alloys (Titanium.*)  -- Ti-6Al-4V (GR5 / TC4)
#   E 110-120, G 42-45, cp 520-560, melting 1600-1660, alpha 8.5-9.5e-6,
#   k 6-9. shear_strength ~0.55-0.6 x UTS.
# ===========================================================================

Titanium_GR5_ANNEALED = Material(
    name="Titanium_GR5_ANNEALED",
    density=4430,
    tensile_strength=Range(900, 950),
    yield_strength=Range(830, 880),
    modulus_of_elasticity=Range(110, 120),
    shear_modulus=Range(42, 45),
    shear_strength=Range(500, 570),
    specific_heat_capacity=Range(520, 560),
    melting_temperature=Range(1600, 1660),
    thermal_expansion=Range(8.5e-6, 9.5e-6),
    thermal_conductivity=Range(6, 9),
    poisson_ratio=Range(0.29, 0.32),
    hardness=Range(30, 38),
    hardness_scale="HRC",
    max_service_temp=Range(250, 350),
)

Titanium_TC4_AS_BUILT = Material(
    name="Titanium_TC4_AS_BUILT",
    density=4430,
    tensile_strength=Range(950, 1100),
    yield_strength=Range(860, 1000),
    modulus_of_elasticity=Range(110, 120),
    shear_modulus=Range(42, 45),
    shear_strength=Range(525, 660),
    specific_heat_capacity=Range(520, 560),
    melting_temperature=Range(1600, 1660),
    thermal_expansion=Range(8.5e-6, 9.5e-6),
    thermal_conductivity=Range(6, 9),
    poisson_ratio=Range(0.29, 0.32),
    hardness=Range(32, 40),
    hardness_scale="HRC",
    max_service_temp=Range(250, 350),
)

TITANIUMS = (Titanium_GR5_ANNEALED, Titanium_TC4_AS_BUILT)


# ===========================================================================
# Copper & brass (Brass.* / Copper.*)
#   cp 380-390. shear_strength ~0.55-0.6 x tensile.
# ===========================================================================

Brass_C360_HALF_HARD = Material(
    name="Brass_C360_HALF_HARD",
    density=8500,
    tensile_strength=Range(380, 450),
    yield_strength=Range(200, 250),
    modulus_of_elasticity=Range(100, 110),
    shear_modulus=Range(37, 40),
    shear_strength=Range(210, 270),
    specific_heat_capacity=Range(380, 390),
    melting_temperature=Range(880, 950),
    thermal_expansion=Range(19e-6, 21e-6),
    thermal_conductivity=Range(110, 130),
    poisson_ratio=Range(0.32, 0.35),
    hardness=Range(90, 120),
    hardness_scale="HB",
    max_service_temp=Range(150, 250),
)

Copper_C110_ANNEALED = Material(
    name="Copper_C110_ANNEALED",
    density=8900,
    tensile_strength=Range(200, 250),
    yield_strength=Range(50, 70),
    modulus_of_elasticity=Range(115, 130),
    shear_modulus=Range(45, 50),
    shear_strength=Range(110, 150),
    specific_heat_capacity=Range(380, 390),
    melting_temperature=Range(1080, 1085),
    thermal_expansion=Range(16e-6, 17e-6),
    thermal_conductivity=Range(390, 400),
    poisson_ratio=Range(0.34, 0.36),
    hardness=Range(45, 80),
    hardness_scale="HB",
    max_service_temp=Range(150, 250),
)

BRASSES = (Brass_C360_HALF_HARD,)
COPPERS = (Copper_C110_ANNEALED,)


# ===========================================================================
# Magnesium (structural, AZ31-ish)
# ===========================================================================

Magnesium_GENERIC_STRUCTURAL = Material(
    name="Magnesium_GENERIC_STRUCTURAL",
    density=1810,
    tensile_strength=Range(200, 280),
    yield_strength=Range(130, 200),
    modulus_of_elasticity=Range(43, 45),
    shear_modulus=Range(16, 18),
    shear_strength=Range(120, 170),
    specific_heat_capacity=Range(1000, 1100),
    melting_temperature=Range(430, 630),
    thermal_expansion=Range(25e-6, 27e-6),
    thermal_conductivity=Range(70, 120),
    poisson_ratio=Range(0.33, 0.37),
    hardness=Range(60, 80),
    hardness_scale="HB",
    max_service_temp=Range(80, 150),
)

MAGNESIUMS = (Magnesium_GENERIC_STRUCTURAL,)


# ===========================================================================
ALL_METALS = (
    *ALUMINUMS,
    *STAINLESS_STEELS,
    *MILD_STEELS,
    *ALLOY_STEELS,
    *TOOL_STEELS,
    *SPRING_STEELS,
    *TITANIUMS,
    *BRASSES,
    *COPPERS,
    *MAGNESIUMS,
)


if __name__ == "__main__":
    print(f"metals: {len(ALL_METALS)}")
    _families = {
        "aluminum": ALUMINUMS,
        "stainless": STAINLESS_STEELS,
        "mild_steel": MILD_STEELS,
        "alloy_steel": ALLOY_STEELS,
        "tool_steel": TOOL_STEELS,
        "spring_steel": SPRING_STEELS,
        "titanium": TITANIUMS,
        "brass": BRASSES,
        "copper": COPPERS,
        "magnesium": MAGNESIUMS,
    }
    for _fam, _items in _families.items():
        print(f"  {_fam:12s}: {len(_items)}")
    print()
    print(Alu_G6061_T6.describe())
    print(Titanium_GR5_ANNEALED.describe())

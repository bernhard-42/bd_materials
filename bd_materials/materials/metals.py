"""Typical-value property ranges for metals.

A ``MetalMaterial`` holds a single representative ``density`` plus min-max ``Range``
bands for each mechanical/thermal property, capturing the typical spread across temper,
product form and process. On top of the shared solid-material fields, metals add
``yield_strength``, ``shear_strength``, ``hardness`` (read on its ``hardness_scale`` --
HB / HRC / HV) and a ``melting_temperature``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import Range, SolidMaterial


@dataclass(frozen=True)
class MetalMaterial(SolidMaterial):
    """A metal: the shared solid ranges (from ``SolidMaterial``) plus yield,
    shear strength, hardness (HB/HRC/HV), and a melting range.

    ``family`` is the PBR/identity key; metals are opaque (``transparent`` False)
    and have no ``color`` -- a metal's colour comes from a finish.
    """

    category: ClassVar[str] = "metal"
    yield_strength: Range | None  # MPa
    shear_strength: Range | None  # MPa
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "HB", "HRC", "HV", ...
    melting_temperature: Range | None  # °C
    family: str | None = None
    transparent: bool = False


# --- Aluminium ---------------------------------------------------------------
class Alu(Enum):
    G6061_T6 = auto()
    G7075_T6 = auto()
    G5052_H32 = auto()
    G2A12_T4 = auto()
    ALSI10MG_AS_BUILT = auto()
    G2024_AEROSPACE = auto()


ALU_MATERIALS: dict[Alu, MetalMaterial] = {
    Alu.G6061_T6: MetalMaterial(
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
        family="aluminum",
    ),
    Alu.G7075_T6: MetalMaterial(
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
        family="aluminum",
    ),
    Alu.G5052_H32: MetalMaterial(
        name="Alu_G5052_H32",
        density=2680,
        tensile_strength=Range(215, 250),
        yield_strength=Range(160, 195),
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
        family="aluminum",
    ),
    Alu.G2A12_T4: MetalMaterial(
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
        family="aluminum",
    ),
    Alu.ALSI10MG_AS_BUILT: MetalMaterial(
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
        family="aluminum",
    ),
    Alu.G2024_AEROSPACE: MetalMaterial(
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
        family="aluminum",
    ),
}


def aluminum(
    grade: Alu = Alu.G6061_T6,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(ALU_MATERIALS[grade], finish, process=process)


# --- Stainless steel ---------------------------------------------------------
class Stainless(Enum):
    G304_ANNEALED = auto()
    G316L_ANNEALED = auto()
    G316L_AS_BUILT = auto()
    G303_ANNEALED = auto()
    G430_ANNEALED = auto()
    G430_COLD_WORKED = auto()
    G201_ANNEALED = auto()


STAINLESS_MATERIALS: dict[Stainless, MetalMaterial] = {
    Stainless.G304_ANNEALED: MetalMaterial(
        name="Stainless_G304_ANNEALED",
        density=7930,
        tensile_strength=Range(515, 620),
        yield_strength=Range(205, 240),
        modulus_of_elasticity=Range(190, 200),
        shear_modulus=Range(75, 82),
        shear_strength=Range(280, 350),
        specific_heat_capacity=Range(480, 500),
        melting_temperature=Range(1400, 1450),
        thermal_expansion=Range(16e-6, 18e-6),
        thermal_conductivity=Range(14, 17),
        poisson_ratio=Range(0.29, 0.31),
        hardness=Range(150, 200),
        hardness_scale="HB",
        max_service_temp=Range(400, 600),
        family="stainless",
    ),
    Stainless.G316L_ANNEALED: MetalMaterial(
        name="Stainless_G316L_ANNEALED",
        density=8000,
        tensile_strength=Range(480, 620),
        yield_strength=Range(170, 310),
        modulus_of_elasticity=Range(190, 200),
        shear_modulus=Range(75, 82),
        shear_strength=Range(280, 350),
        specific_heat_capacity=Range(480, 500),
        melting_temperature=Range(1375, 1450),
        thermal_expansion=Range(16e-6, 18e-6),
        thermal_conductivity=Range(14, 17),
        poisson_ratio=Range(0.29, 0.31),
        hardness=Range(150, 200),
        hardness_scale="HB",
        max_service_temp=Range(400, 600),
        family="stainless",
    ),
    Stainless.G316L_AS_BUILT: MetalMaterial(
        name="Stainless_G316L_AS_BUILT",
        density=7990,
        tensile_strength=Range(550, 700),
        yield_strength=Range(450, 550),
        modulus_of_elasticity=Range(185, 200),
        shear_modulus=Range(75, 82),
        shear_strength=Range(330, 420),
        specific_heat_capacity=Range(480, 500),
        melting_temperature=Range(1375, 1450),
        thermal_expansion=Range(16e-6, 18e-6),
        thermal_conductivity=Range(14, 16),
        poisson_ratio=Range(0.29, 0.31),
        hardness=Range(200, 250),
        hardness_scale="HB",
        max_service_temp=Range(400, 600),
        family="stainless",
    ),
    Stainless.G303_ANNEALED: MetalMaterial(
        name="Stainless_G303_ANNEALED",
        density=8030,
        tensile_strength=Range(500, 625),
        yield_strength=Range(205, 290),
        modulus_of_elasticity=Range(190, 200),
        shear_modulus=Range(75, 82),
        shear_strength=Range(275, 360),
        specific_heat_capacity=Range(480, 500),
        melting_temperature=Range(1400, 1450),
        thermal_expansion=Range(16e-6, 18e-6),
        thermal_conductivity=Range(14, 17),
        poisson_ratio=Range(0.29, 0.31),
        hardness=Range(150, 200),
        hardness_scale="HB",
        max_service_temp=Range(400, 600),
        family="stainless",
    ),
    Stainless.G430_ANNEALED: MetalMaterial(
        name="Stainless_G430_ANNEALED",
        density=7750,
        tensile_strength=Range(450, 500),
        yield_strength=Range(275, 310),
        modulus_of_elasticity=Range(190, 205),
        shear_modulus=Range(75, 82),
        shear_strength=Range(250, 300),
        specific_heat_capacity=Range(480, 500),
        melting_temperature=Range(1425, 1510),
        thermal_expansion=Range(11e-6, 12e-6),
        thermal_conductivity=Range(25, 30),
        poisson_ratio=Range(0.27, 0.3),
        hardness=Range(150, 190),
        hardness_scale="HB",
        max_service_temp=Range(400, 600),
        family="stainless",
    ),
    Stainless.G430_COLD_WORKED: MetalMaterial(
        name="Stainless_G430_COLD_WORKED",
        density=7750,
        tensile_strength=Range(500, 650),
        yield_strength=Range(350, 550),
        modulus_of_elasticity=Range(190, 205),
        shear_modulus=Range(75, 82),
        shear_strength=Range(300, 400),
        specific_heat_capacity=Range(480, 500),
        melting_temperature=Range(1425, 1510),
        thermal_expansion=Range(11e-6, 12e-6),
        thermal_conductivity=Range(25, 30),
        poisson_ratio=Range(0.27, 0.3),
        hardness=Range(185, 230),
        hardness_scale="HB",
        max_service_temp=Range(400, 600),
        family="stainless",
    ),
    Stainless.G201_ANNEALED: MetalMaterial(
        name="Stainless_G201_ANNEALED",
        density=7860,
        tensile_strength=Range(600, 760),
        yield_strength=Range(275, 450),
        modulus_of_elasticity=Range(190, 200),
        shear_modulus=Range(75, 82),
        shear_strength=Range(380, 515),
        specific_heat_capacity=Range(480, 500),
        melting_temperature=Range(1400, 1450),
        thermal_expansion=Range(16e-6, 18e-6),
        thermal_conductivity=Range(14, 16),
        poisson_ratio=Range(0.27, 0.31),
        hardness=Range(180, 230),
        hardness_scale="HB",
        max_service_temp=Range(400, 600),
        family="stainless",
    ),
}


def stainless(
    grade: Stainless = Stainless.G304_ANNEALED,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(STAINLESS_MATERIALS[grade], finish, process=process)


# --- Mild steel --------------------------------------------------------------
class MildSteel(Enum):
    G1018_COLD_DRAWN = auto()
    G1045_COLD_DRAWN = auto()
    GA36_HOT_ROLLED = auto()


MILD_STEEL_MATERIALS: dict[MildSteel, MetalMaterial] = {
    MildSteel.G1018_COLD_DRAWN: MetalMaterial(
        name="MildSteel_G1018_COLD_DRAWN",
        density=7850,
        tensile_strength=Range(440, 480),
        yield_strength=Range(345, 410),
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
        family="mild_steel",
    ),
    MildSteel.G1045_COLD_DRAWN: MetalMaterial(
        name="MildSteel_G1045_COLD_DRAWN",
        density=7850,
        tensile_strength=Range(620, 690),
        yield_strength=Range(480, 600),
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
        family="mild_steel",
    ),
    MildSteel.GA36_HOT_ROLLED: MetalMaterial(
        name="MildSteel_GA36_HOT_ROLLED",
        density=7850,
        tensile_strength=Range(400, 550),
        yield_strength=Range(250, 350),
        modulus_of_elasticity=Range(200, 210),
        shear_modulus=Range(79, 81),
        shear_strength=Range(230, 315),
        specific_heat_capacity=Range(460, 490),
        melting_temperature=Range(1450, 1530),
        thermal_expansion=Range(11e-6, 13e-6),
        thermal_conductivity=Range(45, 55),
        poisson_ratio=Range(0.28, 0.3),
        hardness=Range(120, 180),
        hardness_scale="HB",
        max_service_temp=Range(200, 500),
        family="mild_steel",
    ),
}


def mild_steel(
    grade: MildSteel = MildSteel.G1018_COLD_DRAWN,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(MILD_STEEL_MATERIALS[grade], finish, process=process)


# --- Alloy steel -------------------------------------------------------------
class AlloySteel(Enum):
    G4140_QUENCHED_TEMPERED = auto()
    G4340_QUENCHED_TEMPERED = auto()
    G1215_COLD_DRAWN = auto()


ALLOY_STEEL_MATERIALS: dict[AlloySteel, MetalMaterial] = {
    AlloySteel.G4140_QUENCHED_TEMPERED: MetalMaterial(
        name="AlloySteel_G4140_QUENCHED_TEMPERED",
        density=7850,
        tensile_strength=Range(800, 1150),
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
        family="alloy_steel",
    ),
    AlloySteel.G4340_QUENCHED_TEMPERED: MetalMaterial(
        name="AlloySteel_G4340_QUENCHED_TEMPERED",
        density=7850,
        tensile_strength=Range(980, 1200),
        yield_strength=Range(850, 1080),
        modulus_of_elasticity=Range(200, 215),
        shear_modulus=Range(80, 81),
        shear_strength=Range(560, 780),
        specific_heat_capacity=Range(460, 490),
        melting_temperature=Range(1450, 1530),
        thermal_expansion=Range(11e-6, 13e-6),
        thermal_conductivity=Range(30, 45),
        poisson_ratio=Range(0.28, 0.3),
        hardness=Range(35, 45),
        hardness_scale="HRC",
        max_service_temp=Range(200, 500),
        family="alloy_steel",
    ),
    AlloySteel.G1215_COLD_DRAWN: MetalMaterial(
        name="AlloySteel_G1215_COLD_DRAWN",
        density=7850,
        tensile_strength=Range(440, 550),
        yield_strength=Range(340, 420),
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
        family="alloy_steel",
    ),
}


def alloy_steel(
    grade: AlloySteel = AlloySteel.G4140_QUENCHED_TEMPERED,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(ALLOY_STEEL_MATERIALS[grade], finish, process=process)


# --- Spring steel ------------------------------------------------------------
class SpringSteel(Enum):
    GENERIC_QUENCHED_TEMPERED = auto()


SPRING_STEEL_MATERIALS: dict[SpringSteel, MetalMaterial] = {
    SpringSteel.GENERIC_QUENCHED_TEMPERED: MetalMaterial(
        name="SpringSteel_GENERIC_QUENCHED_TEMPERED",
        density=7850,
        tensile_strength=Range(980, 1500),
        yield_strength=Range(780, 1350),
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
        family="spring_steel",
    ),
}


def spring_steel(
    grade: SpringSteel = SpringSteel.GENERIC_QUENCHED_TEMPERED,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(SPRING_STEEL_MATERIALS[grade], finish, process=process)


# --- Tool steel --------------------------------------------------------------
class ToolSteel(Enum):
    D2_HARDENED = auto()
    A2_HARDENED = auto()
    O1_HARDENED = auto()
    A3_HARDENED = auto()
    S7_HARDENED = auto()
    H13_HARDENED = auto()
    GENERIC_AS_BUILT = auto()


TOOL_STEEL_MATERIALS: dict[ToolSteel, MetalMaterial] = {
    ToolSteel.D2_HARDENED: MetalMaterial(
        name="ToolSteel_D2_HARDENED",
        density=7700,
        tensile_strength=Range(1500, 2200),
        yield_strength=Range(1300, 2000),
        modulus_of_elasticity=Range(200, 215),
        shear_modulus=Range(80, 83),
        shear_strength=Range(855, 1140),
        specific_heat_capacity=Range(460, 500),
        melting_temperature=Range(1450, 1520),
        thermal_expansion=Range(12e-6, 13e-6),
        thermal_conductivity=Range(18, 32),
        poisson_ratio=Range(0.27, 0.3),
        hardness=Range(55, 62),
        hardness_scale="HRC",
        max_service_temp=Range(200, 350),
        family="tool_steel",
    ),
    ToolSteel.A2_HARDENED: MetalMaterial(
        name="ToolSteel_A2_HARDENED",
        density=7860,
        tensile_strength=Range(1400, 1900),
        yield_strength=Range(1200, 1700),
        modulus_of_elasticity=Range(200, 220),
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
        family="tool_steel",
    ),
    ToolSteel.O1_HARDENED: MetalMaterial(
        name="ToolSteel_O1_HARDENED",
        density=7830,
        tensile_strength=Range(1400, 1900),
        yield_strength=Range(1200, 1700),
        modulus_of_elasticity=Range(200, 220),
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
        family="tool_steel",
    ),
    ToolSteel.A3_HARDENED: MetalMaterial(
        name="ToolSteel_A3_HARDENED",
        density=7860,
        tensile_strength=Range(1400, 1900),
        yield_strength=Range(1200, 1700),
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
        family="tool_steel",
    ),
    ToolSteel.S7_HARDENED: MetalMaterial(
        name="ToolSteel_S7_HARDENED",
        density=7830,
        tensile_strength=Range(1400, 1900),
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
        family="tool_steel",
    ),
    ToolSteel.H13_HARDENED: MetalMaterial(
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
        family="tool_steel",
    ),
    ToolSteel.GENERIC_AS_BUILT: MetalMaterial(
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
        family="tool_steel",
    ),
}


def tool_steel(
    grade: ToolSteel = ToolSteel.D2_HARDENED,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(TOOL_STEEL_MATERIALS[grade], finish, process=process)


# --- Titanium ----------------------------------------------------------------
class Titanium(Enum):
    GR5_ANNEALED = auto()
    TC4_AS_BUILT = auto()


TITANIUM_MATERIALS: dict[Titanium, MetalMaterial] = {
    Titanium.GR5_ANNEALED: MetalMaterial(
        name="Titanium_GR5_ANNEALED",
        density=4430,
        tensile_strength=Range(900, 1000),
        yield_strength=Range(830, 960),
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
        max_service_temp=Range(300, 400),
        family="titanium",
    ),
    Titanium.TC4_AS_BUILT: MetalMaterial(
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
        family="titanium",
    ),
}


def titanium(
    grade: Titanium = Titanium.GR5_ANNEALED,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(TITANIUM_MATERIALS[grade], finish, process=process)


# --- Brass -------------------------------------------------------------------
class Brass(Enum):
    C360_HALF_HARD = auto()
    C360_SOFT_ANNEALED = auto()


BRASS_MATERIALS: dict[Brass, MetalMaterial] = {
    Brass.C360_HALF_HARD: MetalMaterial(
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
        family="brass",
    ),
    Brass.C360_SOFT_ANNEALED: MetalMaterial(
        name="Brass_C360_SOFT_ANNEALED",
        density=8500,
        tensile_strength=Range(300, 360),
        yield_strength=Range(100, 160),
        modulus_of_elasticity=Range(97, 110),
        shear_modulus=Range(37, 40),
        shear_strength=Range(180, 230),
        specific_heat_capacity=Range(380, 390),
        melting_temperature=Range(880, 950),
        thermal_expansion=Range(19e-6, 21e-6),
        thermal_conductivity=Range(110, 130),
        poisson_ratio=Range(0.32, 0.35),
        hardness=Range(50, 75),
        hardness_scale="HB",
        max_service_temp=Range(150, 250),
        family="brass",
    ),
}


def brass(
    grade: Brass = Brass.C360_HALF_HARD,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(BRASS_MATERIALS[grade], finish, process=process)


# --- Copper ------------------------------------------------------------------
class Copper(Enum):
    C110_ANNEALED = auto()


COPPER_MATERIALS: dict[Copper, MetalMaterial] = {
    Copper.C110_ANNEALED: MetalMaterial(
        name="Copper_C110_ANNEALED",
        density=8900,
        tensile_strength=Range(200, 250),
        yield_strength=Range(50, 70),
        modulus_of_elasticity=Range(115, 130),
        shear_modulus=Range(44, 48),
        shear_strength=Range(110, 150),
        specific_heat_capacity=Range(380, 390),
        melting_temperature=Range(1080, 1085),
        thermal_expansion=Range(16e-6, 17e-6),
        thermal_conductivity=Range(390, 400),
        poisson_ratio=Range(0.34, 0.36),
        hardness=Range(40, 60),
        hardness_scale="HB",
        max_service_temp=Range(150, 250),
        family="copper",
    ),
}


def copper(
    grade: Copper = Copper.C110_ANNEALED,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(COPPER_MATERIALS[grade], finish, process=process)


# --- Magnesium ---------------------------------------------------------------
class Magnesium(Enum):
    GENERIC_STRUCTURAL = auto()


MAGNESIUM_MATERIALS: dict[Magnesium, MetalMaterial] = {
    Magnesium.GENERIC_STRUCTURAL: MetalMaterial(
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
        family="magnesium",
    ),
}


def magnesium(
    grade: Magnesium = Magnesium.GENERIC_STRUCTURAL,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[MetalMaterial]:
    return FinishedMaterial(MAGNESIUM_MATERIALS[grade], finish, process=process)


ALL_METALS = (
    *ALU_MATERIALS.values(),
    *STAINLESS_MATERIALS.values(),
    *MILD_STEEL_MATERIALS.values(),
    *ALLOY_STEEL_MATERIALS.values(),
    *SPRING_STEEL_MATERIALS.values(),
    *TOOL_STEEL_MATERIALS.values(),
    *TITANIUM_MATERIALS.values(),
    *BRASS_MATERIALS.values(),
    *COPPER_MATERIALS.values(),
    *MAGNESIUM_MATERIALS.values(),
)


if __name__ == "__main__":
    print(f"metals: {len(ALL_METALS)}")
    _families = {
        "aluminum": ALU_MATERIALS,
        "stainless": STAINLESS_MATERIALS,
        "mild_steel": MILD_STEEL_MATERIALS,
        "alloy_steel": ALLOY_STEEL_MATERIALS,
        "spring_steel": SPRING_STEEL_MATERIALS,
        "tool_steel": TOOL_STEEL_MATERIALS,
        "titanium": TITANIUM_MATERIALS,
        "brass": BRASS_MATERIALS,
        "copper": COPPER_MATERIALS,
        "magnesium": MAGNESIUM_MATERIALS,
    }
    for _fam, _dct in _families.items():
        print(f"  {_fam:12s}: {len(_dct)}")
    print()
    print(ALU_MATERIALS[Alu.G6061_T6])
    print(TITANIUM_MATERIALS[Titanium.GR5_ANNEALED])

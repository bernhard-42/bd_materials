"""Typical-value property ranges for plastics.

A ``PlasticMaterial`` holds a single representative ``density`` plus min-max ``Range``
bands for the mechanical/thermal properties. The set adds
``glass_transition_temperature`` (the transition that governs polymer service, in place
of a melting point), ``heat_deflection_temperature``, ``elongation_at_break`` and a
Shore ``hardness`` on its ``hardness_scale`` ("Shore D" for rigid grades, "Shore A" for
elastomers).

For a brittle thermoplastic or short-fibre grade that fractures with little yielding,
``yield_strength`` ~equals ``tensile_strength``. A field is ``NOT_SUITABLE`` where the
property does not apply (an elastomer's yield or heat-deflection, a laminate's isotropic
yield) and ``None`` where a value is simply not filled in.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import NOT_SUITABLE, PolymerMaterial, Range


@dataclass(frozen=True)
class PlasticMaterial(PolymerMaterial):
    """A plastic: the shared polymer ranges (from ``PolymerMaterial``) plus a Shore
    hardness. ``family`` is the PBR/identity key; ``transparent`` is True for clear
    grades (PMMA, PC). A part's colour lives on ``FinishedMaterial``, not here.
    """

    category: ClassVar[str] = "plastic"
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "Shore D", "Shore A", ...
    family: str | None = None
    transparent: bool = False


_Finish = AppliedFinish | list[AppliedFinish] | None


# --- PLA ---------------------------------------------------------------------
class PLA(Enum):
    GENERIC = auto()
    CARBON_FILLED = auto()


PLA_MATERIALS: dict[PLA, PlasticMaterial] = {
    PLA.GENERIC: PlasticMaterial(
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
        max_service_temp=Range(50, 60),
        thermal_expansion=Range(60e-6, 90e-6),
        thermal_conductivity=Range(0.11, 0.16),
        family="PLA",
    ),
    PLA.CARBON_FILLED: PlasticMaterial(
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
        max_service_temp=Range(55, 65),
        thermal_expansion=Range(25e-6, 50e-6),
        thermal_conductivity=Range(0.15, 0.30),
        family="PLA",
    ),
}


def pla(
    grade: PLA = PLA.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(PLA_MATERIALS[grade], finish, color=color, process=process)


# --- ABS ---------------------------------------------------------------------
class ABS(Enum):
    GENERIC = auto()
    FLAME_RETARDANT = auto()


ABS_MATERIALS: dict[ABS, PlasticMaterial] = {
    ABS.GENERIC: PlasticMaterial(
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
        family="ABS",
    ),
    ABS.FLAME_RETARDANT: PlasticMaterial(
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
        family="ABS",
    ),
}


def abs_(
    grade: ABS = ABS.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(ABS_MATERIALS[grade], finish, color=color, process=process)


# --- Nylon (PA) --------------------------------------------------------------
class Nylon(Enum):
    PA6 = auto()
    PA12 = auto()
    PA12_SINTERED = auto()
    PA12_GF35 = auto()


NYLON_MATERIALS: dict[Nylon, PlasticMaterial] = {
    Nylon.PA6: PlasticMaterial(
        name="Nylon_PA6",
        density=1140,
        tensile_strength=Range(50, 90),
        yield_strength=Range(45, 85),
        modulus_of_elasticity=Range(1.9, 3.5),
        shear_modulus=Range(0.8, 1.3),
        poisson_ratio=Range(0.38, 0.42),
        shear_strength=Range(30, 60),
        elongation_at_break=Range(20, 300),
        hardness=Range(75, 85),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1600, 1700),
        glass_transition_temperature=Range(45, 60),
        heat_deflection_temperature=Range(60, 100),
        max_service_temp=Range(80, 130),
        thermal_expansion=Range(70e-6, 100e-6),
        thermal_conductivity=Range(0.24, 0.31),
        family="PA",
    ),
    Nylon.PA12: PlasticMaterial(
        name="Nylon_PA12",
        density=1010,
        tensile_strength=Range(30, 55),
        yield_strength=Range(30, 50),
        modulus_of_elasticity=Range(1.2, 1.8),
        shear_modulus=Range(0.5, 0.8),
        poisson_ratio=Range(0.38, 0.42),
        shear_strength=Range(25, 40),
        elongation_at_break=Range(5, 300),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1700, 1800),
        glass_transition_temperature=Range(40, 50),
        heat_deflection_temperature=Range(45, 80),
        max_service_temp=Range(70, 95),
        thermal_expansion=Range(100e-6, 150e-6),
        thermal_conductivity=Range(0.23, 0.28),
        family="PA",
    ),
    Nylon.PA12_SINTERED: PlasticMaterial(
        name="Nylon_PA12_SINTERED",
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
        family="PA",
    ),
    Nylon.PA12_GF35: PlasticMaterial(
        name="Nylon_PA12_GF35",
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
        family="PA",
    ),
}


def nylon(
    grade: Nylon = Nylon.PA12,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(
        NYLON_MATERIALS[grade], finish, color=color, process=process
    )


# --- PEEK --------------------------------------------------------------------
class Peek(Enum):
    MOLDED = auto()
    PRINTED = auto()


PEEK_MATERIALS: dict[Peek, PlasticMaterial] = {
    Peek.MOLDED: PlasticMaterial(
        name="Peek_MOLDED",
        density=1300,
        tensile_strength=Range(90, 110),
        yield_strength=Range(90, 100),
        modulus_of_elasticity=Range(3.5, 4.2),
        shear_modulus=Range(1.3, 1.6),
        poisson_ratio=Range(0.38, 0.42),
        shear_strength=Range(50, 75),
        elongation_at_break=Range(20, 100),
        hardness=Range(85, 90),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1300, 1400),
        glass_transition_temperature=Range(143, 150),
        heat_deflection_temperature=Range(140, 160),
        max_service_temp=Range(240, 260),
        thermal_expansion=Range(45e-6, 60e-6),
        thermal_conductivity=Range(0.24, 0.29),
        family="PEEK",
    ),
    Peek.PRINTED: PlasticMaterial(
        name="Peek_PRINTED",
        density=1300,
        tensile_strength=Range(80, 120),
        yield_strength=Range(80, 105),
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
        max_service_temp=Range(160, 250),
        thermal_expansion=Range(45e-6, 60e-6),
        thermal_conductivity=Range(0.24, 0.29),
        family="PEEK",
    ),
}


def peek(
    grade: Peek = Peek.MOLDED,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(PEEK_MATERIALS[grade], finish, color=color, process=process)


# --- TPU ---------------------------------------------------------------------
class TPU(Enum):
    SHORE_95A = auto()
    SINTERED = auto()


TPU_MATERIALS: dict[TPU, PlasticMaterial] = {
    TPU.SHORE_95A: PlasticMaterial(
        name="TPU_SHORE_95A",
        density=1200,
        tensile_strength=Range(25, 55),
        yield_strength=NOT_SUITABLE,
        modulus_of_elasticity=Range(0.007, 0.10),
        shear_modulus=Range(0.002, 0.035),
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
        family="TPU",
    ),
    TPU.SINTERED: PlasticMaterial(
        name="TPU_SINTERED",
        density=1200,
        tensile_strength=Range(10, 25),
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
        family="TPU",
    ),
}


def tpu(
    grade: TPU = TPU.SHORE_95A,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(TPU_MATERIALS[grade], finish, color=color, process=process)


# --- PC (polycarbonate) ------------------------------------------------------
class PC(Enum):
    GENERIC = auto()


PC_MATERIALS: dict[PC, PlasticMaterial] = {
    PC.GENERIC: PlasticMaterial(
        name="PC_GENERIC",
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
        max_service_temp=Range(115, 145),
        thermal_expansion=Range(65e-6, 75e-6),
        thermal_conductivity=Range(0.19, 0.22),
        family="PC",
        transparent=True,
    ),
}


def pc(
    grade: PC = PC.GENERIC,
    color=None,
    thickness_mm=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(
        PC_MATERIALS[grade],
        finish,
        color=color,
        thickness_mm=thickness_mm,
        process=process,
    )


# --- PP (polypropylene) ------------------------------------------------------
class PP(Enum):
    GENERIC = auto()


PP_MATERIALS: dict[PP, PlasticMaterial] = {
    PP.GENERIC: PlasticMaterial(
        name="PP_GENERIC",
        density=905,
        tensile_strength=Range(25, 40),
        yield_strength=Range(25, 38),
        modulus_of_elasticity=Range(1.1, 1.8),
        shear_modulus=Range(0.4, 0.7),
        poisson_ratio=Range(0.40, 0.45),
        shear_strength=Range(15, 30),
        elongation_at_break=Range(10, 600),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1800, 2000),
        glass_transition_temperature=Range(-20, -10),
        heat_deflection_temperature=Range(50, 65),
        max_service_temp=Range(80, 130),
        thermal_expansion=Range(100e-6, 180e-6),
        thermal_conductivity=Range(0.11, 0.27),
        family="PP",
    ),
}


def pp(
    grade: PP = PP.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(PP_MATERIALS[grade], finish, color=color, process=process)


# --- POM (acetal) ------------------------------------------------------------
class POM(Enum):
    GENERIC = auto()


POM_MATERIALS: dict[POM, PlasticMaterial] = {
    POM.GENERIC: PlasticMaterial(
        name="POM_GENERIC",
        density=1410,
        tensile_strength=Range(60, 90),
        yield_strength=Range(60, 73),
        modulus_of_elasticity=Range(2.8, 4.0),
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
        thermal_expansion=Range(80e-6, 140e-6),
        thermal_conductivity=Range(0.30, 0.40),
        family="POM",
    ),
}


def pom(
    grade: POM = POM.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(POM_MATERIALS[grade], finish, color=color, process=process)


# --- PTFE --------------------------------------------------------------------
class PTFE(Enum):
    GENERIC = auto()


PTFE_MATERIALS: dict[PTFE, PlasticMaterial] = {
    PTFE.GENERIC: PlasticMaterial(
        name="PTFE_GENERIC",
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
        thermal_expansion=Range(100e-6, 200e-6),
        thermal_conductivity=Range(0.23, 0.27),
        family="PTFE",
    ),
}


def ptfe(
    grade: PTFE = PTFE.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(PTFE_MATERIALS[grade], finish, color=color, process=process)


# --- PMMA (acrylic) ----------------------------------------------------------
class PMMA(Enum):
    GENERIC = auto()


PMMA_MATERIALS: dict[PMMA, PlasticMaterial] = {
    PMMA.GENERIC: PlasticMaterial(
        name="PMMA_GENERIC",
        density=1180,
        tensile_strength=Range(50, 83),
        yield_strength=Range(50, 80),
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
        family="PMMA",
        transparent=True,
    ),
}


def pmma(
    grade: PMMA = PMMA.GENERIC,
    color=None,
    thickness_mm=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(
        PMMA_MATERIALS[grade],
        finish,
        color=color,
        thickness_mm=thickness_mm,
        process=process,
    )


# --- PE (polyethylene) -------------------------------------------------------
class PE(Enum):
    HDPE = auto()


PE_MATERIALS: dict[PE, PlasticMaterial] = {
    PE.HDPE: PlasticMaterial(
        name="PE_HDPE",
        density=960,
        tensile_strength=Range(20, 35),
        yield_strength=Range(20, 31),
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
        max_service_temp=Range(60, 110),
        thermal_expansion=Range(100e-6, 200e-6),
        thermal_conductivity=Range(0.35, 0.51),
        family="PE",
    ),
}


def pe(
    grade: PE = PE.HDPE,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(PE_MATERIALS[grade], finish, color=color, process=process)


# --- Phenolic ----------------------------------------------------------------
class Phenolic(Enum):
    BAKELITE = auto()


PHENOLIC_MATERIALS: dict[Phenolic, PlasticMaterial] = {
    Phenolic.BAKELITE: PlasticMaterial(
        name="Phenolic_BAKELITE",
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
        family="phenolic",
    ),
}


def phenolic(
    grade: Phenolic = Phenolic.BAKELITE,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(
        PHENOLIC_MATERIALS[grade], finish, color=color, process=process
    )


# --- Rubber ------------------------------------------------------------------
class Rubber(Enum):
    GENERIC = auto()


RUBBER_MATERIALS: dict[Rubber, PlasticMaterial] = {
    Rubber.GENERIC: PlasticMaterial(
        name="Rubber_GENERIC",
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
        family="rubber",
    ),
}


def rubber(
    grade: Rubber = Rubber.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(
        RUBBER_MATERIALS[grade], finish, color=color, process=process
    )


# --- PETG --------------------------------------------------------------------
class PETG(Enum):
    GENERIC = auto()
    CF = auto()


PETG_MATERIALS: dict[PETG, PlasticMaterial] = {
    PETG.GENERIC: PlasticMaterial(
        name="PETG_GENERIC",
        density=1270,
        tensile_strength=Range(45, 55),
        yield_strength=Range(45, 53),
        modulus_of_elasticity=Range(2.0, 2.2),
        shear_modulus=Range(0.7, 0.85),
        poisson_ratio=Range(0.38, 0.43),
        shear_strength=Range(30, 40),
        elongation_at_break=Range(50, 120),
        hardness=Range(75, 82),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1200, 1400),
        glass_transition_temperature=Range(75, 85),
        heat_deflection_temperature=Range(65, 75),
        max_service_temp=Range(60, 70),
        thermal_expansion=Range(60e-6, 80e-6),
        thermal_conductivity=Range(0.15, 0.25),
        family="PETG",
    ),
    PETG.CF: PlasticMaterial(
        name="PETG_CF",
        density=1320,
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
        family="PETG",
    ),
}


def petg(
    grade: PETG = PETG.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(PETG_MATERIALS[grade], finish, color=color, process=process)


# --- ASA ---------------------------------------------------------------------
class Asa(Enum):
    GENERIC = auto()


# Weathering-resistant amorphous thermoplastic, a UV-stable relative of ABS; the
# property bands are typical for the class.
ASA_MATERIALS: dict[Asa, PlasticMaterial] = {
    Asa.GENERIC: PlasticMaterial(
        name="Asa_GENERIC",
        density=1070,
        tensile_strength=Range(40, 55),
        yield_strength=Range(40, 50),
        modulus_of_elasticity=Range(1.9, 2.6),
        shear_modulus=Range(0.7, 0.95),
        poisson_ratio=Range(0.35, 0.40),
        shear_strength=Range(25, 38),
        elongation_at_break=Range(10, 40),
        hardness=Range(70, 80),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1300, 1500),
        glass_transition_temperature=Range(100, 110),
        heat_deflection_temperature=Range(85, 100),
        max_service_temp=Range(65, 85),
        thermal_expansion=Range(80e-6, 100e-6),
        thermal_conductivity=Range(0.15, 0.20),
        family="ASA",
    ),
}


def asa(
    grade: Asa = Asa.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(ASA_MATERIALS[grade], finish, color=color, process=process)


# --- PPS ---------------------------------------------------------------------
class PPS(Enum):
    CF = auto()


PPS_MATERIALS: dict[PPS, PlasticMaterial] = {
    PPS.CF: PlasticMaterial(
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
        # Tg ~85-105 but HDT 200-270: reinforced semi-crystalline HDT tracks Tm (~280), not Tg
        glass_transition_temperature=Range(85, 105),
        heat_deflection_temperature=Range(200, 270),
        max_service_temp=Range(200, 240),
        thermal_expansion=Range(20e-6, 50e-6),
        thermal_conductivity=Range(0.25, 0.45),
        family="PPS",
    ),
}


def pps(
    grade: PPS = PPS.CF,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(PPS_MATERIALS[grade], finish, color=color, process=process)


# --- FR4 ---------------------------------------------------------------------
class FR4(Enum):
    GENERIC = auto()


FR4_MATERIALS: dict[FR4, PlasticMaterial] = {
    FR4.GENERIC: PlasticMaterial(
        name="FR4_GENERIC",
        density=1850,
        tensile_strength=Range(260, 340),
        yield_strength=NOT_SUITABLE,
        modulus_of_elasticity=Range(18, 24),
        shear_modulus=Range(3, 7),
        # FR4's Poisson ratio is genuinely this low for the anisotropic laminate
        poisson_ratio=Range(0.11, 0.18),
        shear_strength=Range(60, 120),
        elongation_at_break=Range(1, 3),
        hardness=Range(85, 90),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(600, 900),
        glass_transition_temperature=Range(130, 180),
        heat_deflection_temperature=Range(130, 180),
        max_service_temp=Range(120, 160),
        thermal_expansion=Range(12e-6, 18e-6),
        thermal_conductivity=Range(0.25, 0.35),
        family="FR4",
    ),
}


def fr4(
    grade: FR4 = FR4.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(FR4_MATERIALS[grade], finish, color=color, process=process)


# --- CFRP --------------------------------------------------------------------
class CFRP(Enum):
    PLATE = auto()


CFRP_MATERIALS: dict[CFRP, PlasticMaterial] = {
    CFRP.PLATE: PlasticMaterial(
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
        thermal_conductivity=Range(0.5, 10),
        family="CFRP",
    ),
}


def cfrp(
    grade: CFRP = CFRP.PLATE,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PlasticMaterial]:
    return FinishedMaterial(CFRP_MATERIALS[grade], finish, color=color, process=process)


ALL_PLASTICS = (
    *PLA_MATERIALS.values(),
    *ABS_MATERIALS.values(),
    *NYLON_MATERIALS.values(),
    *PEEK_MATERIALS.values(),
    *TPU_MATERIALS.values(),
    *PC_MATERIALS.values(),
    *PP_MATERIALS.values(),
    *POM_MATERIALS.values(),
    *PTFE_MATERIALS.values(),
    *PMMA_MATERIALS.values(),
    *PE_MATERIALS.values(),
    *PHENOLIC_MATERIALS.values(),
    *RUBBER_MATERIALS.values(),
    *PETG_MATERIALS.values(),
    *ASA_MATERIALS.values(),
    *PPS_MATERIALS.values(),
    *FR4_MATERIALS.values(),
    *CFRP_MATERIALS.values(),
)


if __name__ == "__main__":
    print(f"plastics: {len(ALL_PLASTICS)}")
    print()
    print(PLA_MATERIALS[PLA.GENERIC])
    print(PC_MATERIALS[PC.GENERIC])
    print(TPU_MATERIALS[TPU.SHORE_95A])

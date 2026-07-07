"""Range-based typical values for photopolymer resins (SLA / DLP).

Sibling of the metals/plastics modules using the same approach and the
shared :mod:`..core` primitives (``Range``, ``PROPERTY_UNITS``, ``RangeMaterial``).

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
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import PolymerMaterial, Range


@dataclass(frozen=True)
class ResinMaterial(PolymerMaterial):
    """A photopolymer resin: the shared polymer ranges (from ``PolymerMaterial``)
    plus a fixed-scale ``shore_hardness`` (Shore D). ``transparent`` is True for the
    clear resin; a part's colour lives on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "resin"
    shore_hardness: Range | None  # Shore D
    family: str | None = None
    transparent: bool = False


class Resin(Enum):
    STANDARD = auto()
    TOUGH = auto()
    HIGH_TEMP = auto()
    CERAMIC = auto()
    CASTABLE = auto()
    ESD = auto()
    TRANSPARENT = auto()


RESIN_MATERIALS: dict[Resin, ResinMaterial] = {
    Resin.STANDARD: ResinMaterial(
        name="Resin_STANDARD",
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
        family="resin",
    ),
    Resin.TOUGH: ResinMaterial(
        name="Resin_TOUGH",
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
        family="resin",
    ),
    Resin.HIGH_TEMP: ResinMaterial(
        name="Resin_HIGH_TEMP",
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
        family="resin",
    ),
    Resin.CERAMIC: ResinMaterial(
        name="Resin_CERAMIC",
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
        family="resin",
    ),
    Resin.CASTABLE: ResinMaterial(
        name="Resin_CASTABLE",
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
        family="resin",
    ),
    Resin.ESD: ResinMaterial(
        name="Resin_ESD",
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
        family="resin",
    ),
    Resin.TRANSPARENT: ResinMaterial(
        name="Resin_TRANSPARENT",
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
        family="resin",
        transparent=True,
    ),
}


_Finish = AppliedFinish | list[AppliedFinish] | None


def resin(
    grade: Resin = Resin.STANDARD,
    color=None,
    thickness_mm=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial:
    return FinishedMaterial(
        RESIN_MATERIALS[grade],
        finish,
        color=color,
        thickness_mm=thickness_mm,
        process=process,
    )


ALL_RESINS = tuple(RESIN_MATERIALS.values())


if __name__ == "__main__":
    print(f"resins: {len(ALL_RESINS)}")
    print()
    print(RESIN_MATERIALS[Resin.STANDARD])
    print(RESIN_MATERIALS[Resin.CERAMIC])

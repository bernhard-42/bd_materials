"""Range-based typical values for photopolymer resins (SLA / DLP).

Sibling of the metals/plastics modules using the same approach and the
shared :mod:`..core` primitives (``Range``, ``PROPERTY_UNITS``, ``RangeMaterial``).

Resins are grouped into **vendor-neutral functional families** (standard, tough,
high-temp, flexible, ...) rather than individual products. The property set mirrors
plastics: ``glass_transition_temperature``, ``heat_deflection_temperature``,
``elongation_at_break``, and ``hardness`` + ``hardness_scale`` -- rigid resins are
quoted on **Shore D**, flexible/elastomeric ones on **Shore A**.

``yield_strength`` ~equals tensile strength for the rigid families (cast
photopolymers fail with little distinct yielding); it is ``NOT_SUITABLE`` for the
flexible/elastomeric family.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import NOT_SUITABLE, PolymerMaterial, Range


@dataclass(frozen=True)
class ResinMaterial(PolymerMaterial):
    """A photopolymer resin: the shared polymer ranges (from ``PolymerMaterial``) plus
    a Shore hardness. ``hardness_scale`` is "Shore D" for rigid resins, "Shore A" for
    flexible ones. ``transparent`` is True for the clear resin; a part's colour lives
    on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "resin"
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "Shore D" (rigid) / "Shore A" (flexible)
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
    FLEXIBLE = auto()


# For rigid photopolymers Tg and HDT bands nearly coincide: these resins are
# tested near Tg, so HDT (usually ~5-15C below Tg) overlaps it -- not a duplication.
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
        hardness=Range(80, 86),
        hardness_scale="Shore D",
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
        hardness=Range(78, 84),
        hardness_scale="Shore D",
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
        elongation_at_break=Range(1, 10),
        hardness=Range(80, 86),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1400, 1600),
        glass_transition_temperature=Range(110, 245),
        heat_deflection_temperature=Range(100, 230),
        max_service_temp=Range(100, 200),
        thermal_expansion=Range(70e-6, 120e-6),
        thermal_conductivity=Range(0.18, 0.25),
        family="resin",
    ),
    Resin.CERAMIC: ResinMaterial(
        name="Resin_CERAMIC",
        density=1650,
        tensile_strength=Range(60, 80),
        yield_strength=Range(55, 72),
        modulus_of_elasticity=Range(5, 9),
        shear_modulus=Range(3.0, 4.5),
        poisson_ratio=Range(0.30, 0.35),
        shear_strength=Range(36, 48),
        elongation_at_break=Range(1, 3),
        hardness=Range(88, 95),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1100, 1300),
        glass_transition_temperature=Range(150, 250),
        # ceramic-filled: HDT is filler-controlled and can exceed the matrix Tg (not an inversion)
        heat_deflection_temperature=Range(200, 280),
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
        hardness=Range(76, 83),
        hardness_scale="Shore D",
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
        # hardness is an ESTIMATE -- ESD datasheets (e.g. Formlabs) list no Shore value
        hardness=Range(80, 88),
        hardness_scale="Shore D",
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
        hardness=Range(80, 88),
        hardness_scale="Shore D",
        specific_heat_capacity=Range(1400, 1600),
        glass_transition_temperature=Range(45, 62),
        heat_deflection_temperature=Range(45, 60),
        max_service_temp=Range(40, 55),
        thermal_expansion=Range(80e-6, 130e-6),
        thermal_conductivity=Range(0.18, 0.25),
        family="resin",
        transparent=True,
    ),
    Resin.FLEXIBLE: ResinMaterial(
        name="Resin_FLEXIBLE",
        density=1150,
        tensile_strength=Range(5, 30),
        yield_strength=NOT_SUITABLE,
        modulus_of_elasticity=Range(0.001, 0.5),
        shear_modulus=Range(0.0003, 0.17),
        poisson_ratio=Range(0.40, 0.49),
        shear_strength=Range(3, 18),
        elongation_at_break=Range(25, 120),
        hardness=Range(55, 85),
        hardness_scale="Shore A",
        specific_heat_capacity=Range(1400, 1600),
        glass_transition_temperature=Range(-20, 25),
        heat_deflection_temperature=NOT_SUITABLE,
        max_service_temp=Range(40, 70),
        thermal_expansion=Range(100e-6, 200e-6),
        thermal_conductivity=Range(0.15, 0.25),
        family="resin",
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

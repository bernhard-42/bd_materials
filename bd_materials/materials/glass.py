"""Typical-value property ranges for glass.

Glass is an amorphous, brittle inorganic solid, so the field set is tailored: it omits
``yield_strength``, ``shear_strength``, ``elongation_at_break`` and
``heat_deflection_temperature`` (a brittle solid has no ductile yield or elongation, and
HDT is a polymer test). ``tensile_strength`` is the practical **flaw-limited** annealed
strength -- surface flaws dominate, so pristine fibre is far higher. ``hardness`` is on
the Vickers (HV) scale. A ``glass_transition_temperature`` and a ``melting_temperature``
are both carried; the latter is the furnace-melt range (glass has no sharp melt point),
not a service limit -- use ``max_service_temp`` for that.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import Range, SolidMaterial


@dataclass(frozen=True)
class GlassMaterial(SolidMaterial):
    """A glass: the shared solid ranges (from ``SolidMaterial``; ``tensile_strength``
    is flaw-limited, annealed) plus Vickers hardness, a glass-transition and a
    furnace-melt range (see below). Brittle, so no yield/shear-strength fields.

    Glass is ``transparent``; the optional colour + pane ``thickness_mm`` are
    per-part and live on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "glass"
    hardness: Range | None  # on the `hardness_scale` scale
    hardness_scale: str  # "HV" (Vickers)
    glass_transition_temperature: Range | None  # °C
    melting_temperature: Range | None  # °C -- furnace-melt range, not a service
    # limit (glass softens far lower, ~730/820C -- see max_service_temp)
    family: str | None = None
    transparent: bool = False


class Glass(Enum):
    SODA_LIME = auto()
    BOROSILICATE = auto()


GLASS_MATERIALS: dict[Glass, GlassMaterial] = {
    Glass.SODA_LIME: GlassMaterial(
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
        max_service_temp=Range(150, 300),
        thermal_expansion=Range(8.5e-6, 9.5e-6),
        thermal_conductivity=Range(0.9, 1.1),
        family="soda_lime",
        transparent=True,
    ),
    Glass.BOROSILICATE: GlassMaterial(
        name="GLASS_BOROSILICATE",
        density=2230,
        tensile_strength=Range(30, 90),
        modulus_of_elasticity=Range(60, 66),
        shear_modulus=Range(24, 28),
        poisson_ratio=Range(0.19, 0.22),
        hardness=Range(480, 600),
        hardness_scale="HV",
        specific_heat_capacity=Range(750, 830),
        glass_transition_temperature=Range(490, 565),
        melting_temperature=Range(1500, 1650),
        max_service_temp=Range(230, 400),
        thermal_expansion=Range(3.0e-6, 3.5e-6),
        thermal_conductivity=Range(1.0, 1.2),
        family="borosilicate",
        transparent=True,
    ),
}


def glass(
    grade: Glass = Glass.SODA_LIME,
    color=None,
    thickness_mm=None,
    finish: AppliedFinish | list[AppliedFinish] | None = None,
    process: Process | None = None,
) -> FinishedMaterial[GlassMaterial]:
    return FinishedMaterial(
        GLASS_MATERIALS[grade],
        finish,
        color=color,
        thickness_mm=thickness_mm,
        process=process,
    )


ALL_GLASSES = tuple(GLASS_MATERIALS.values())


if __name__ == "__main__":
    print(f"glasses: {len(ALL_GLASSES)}")
    print()
    for _g in ALL_GLASSES:
        print(_g)
        print()

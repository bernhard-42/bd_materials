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

from ..finished import Color, FinishedMaterial, FinishSpec, Process
from ..core import Range, SolidMaterial, with_density


@dataclass(frozen=True, kw_only=True)
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


# --- Soda-lime ---------------------------------------------------------------
class SodaLime(Enum):
    GENERIC = auto()


SODA_LIME_MATERIALS: dict[SodaLime, GlassMaterial] = {
    SodaLime.GENERIC: GlassMaterial(
        # identity
        name="SodaLime_GENERIC",
        family="soda_lime",
        transparent=True,
        # mechanical properties
        density=2500,
        hardness=Range(470, 570),
        hardness_scale="HV",
        modulus_of_elasticity=Range(68, 74),
        poisson_ratio=Range(0.21, 0.24),
        shear_modulus=Range(26, 30),
        tensile_strength=Range(30, 90),
        # thermal properties
        glass_transition_temperature=Range(520, 570),
        max_service_temp=Range(150, 300),
        melting_temperature=Range(1400, 1600),
        specific_heat_capacity=Range(750, 880),
        thermal_conductivity=Range(0.9, 1.1),
        thermal_expansion=Range(8.5e-6, 9.5e-6),
    ),
}


def soda_lime(
    grade: SodaLime = SodaLime.GENERIC,
    color: Color | None = None,
    thickness_mm: float | None = None,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[GlassMaterial]:
    """Soda-lime glass as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base colour for the part -- a standard-palette name, a hex string, or an
            RGB tuple.
        thickness_mm: Pane thickness in mm; used for the transmissive look (the material
            is transparent).
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process``.
        process: As-made surface hint (e.g. ``Process.FDM``). Mutually exclusive with
            ``finish``.
        density: Override the material's single representative density (kg/m³) for this
            part.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(SODA_LIME_MATERIALS[grade], density),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        process=process,
    )


# --- Borosilicate ------------------------------------------------------------
class Borosilicate(Enum):
    GENERIC = auto()


BOROSILICATE_MATERIALS: dict[Borosilicate, GlassMaterial] = {
    Borosilicate.GENERIC: GlassMaterial(
        # identity
        name="Borosilicate_GENERIC",
        family="borosilicate",
        transparent=True,
        # mechanical properties
        density=2230,
        hardness=Range(480, 600),
        hardness_scale="HV",
        modulus_of_elasticity=Range(60, 66),
        poisson_ratio=Range(0.19, 0.22),
        shear_modulus=Range(24, 28),
        tensile_strength=Range(30, 90),
        # thermal properties
        glass_transition_temperature=Range(490, 565),
        max_service_temp=Range(230, 400),
        melting_temperature=Range(1500, 1650),
        specific_heat_capacity=Range(750, 830),
        thermal_conductivity=Range(1.0, 1.2),
        thermal_expansion=Range(3.0e-6, 3.5e-6),
    ),
}


def borosilicate(
    grade: Borosilicate = Borosilicate.GENERIC,
    color: Color | None = None,
    thickness_mm: float | None = None,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[GlassMaterial]:
    """Borosilicate glass as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base colour for the part -- a standard-palette name, a hex string, or an
            RGB tuple.
        thickness_mm: Pane thickness in mm; used for the transmissive look (the material
            is transparent).
        finish: Surface finish -- an ``AppliedFinish`` or a list of them. Mutually
            exclusive with ``process``.
        process: As-made surface hint (e.g. ``Process.FDM``). Mutually exclusive with
            ``finish``.
        density: Override the material's single representative density (kg/m³) for this
            part.

    Returns:
        A ``FinishedMaterial`` for the selected grade.
    """
    return FinishedMaterial(
        with_density(BOROSILICATE_MATERIALS[grade], density),
        finish,
        color=color,
        thickness_mm=thickness_mm,
        process=process,
    )


ALL_GLASSES = (
    *SODA_LIME_MATERIALS.values(),
    *BOROSILICATE_MATERIALS.values(),
)


if __name__ == "__main__":
    print(f"glasses: {len(ALL_GLASSES)}")
    print()
    for _g in ALL_GLASSES:
        print(_g)
        print()

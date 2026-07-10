"""Typical-value property ranges for paper goods (paper, cardboard, foamboard).

These are **areal goods**: the primary mass metric is grammage (``areal_density``,
g/m2), not volumetric density -- a cut sheet's mass is grammage x area, and the
``density`` field is only the effective bulk value. ``tensile_strength`` is the in-plane
(machine-direction) value and is approximate for these layered materials; grade and
supplier variation is large, so treat all values as rough typicals.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import Color, FinishedMaterial, FinishSpec, Process
from ..core import ArealMaterial, Range, with_density


@dataclass(frozen=True, kw_only=True)
class PaperMaterial(ArealMaterial):
    """A paper good: the shared areal ranges (from ``ArealMaterial``). ``family`` is
    the three.js paper factory key; a part's colour lives on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "paper"


# --- Paper -------------------------------------------------------------------
class Paper(Enum):
    OFFICE = auto()


PAPER_MATERIALS: dict[Paper, PaperMaterial] = {
    Paper.OFFICE: PaperMaterial(
        # identity
        name="Paper_OFFICE",
        family="paper",
        # mechanical properties
        areal_density=Range(70, 90),
        density=800,
        tensile_strength=Range(20, 60),
        thickness=Range(0.09, 0.12),
        # thermal properties
        specific_heat_capacity=Range(1300, 1400),
        thermal_conductivity=Range(0.05, 0.10),
    ),
}


def paper(
    grade: Paper = Paper.OFFICE,
    color: Color | None = "white",
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[PaperMaterial]:
    """Office paper as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to office.
        color: Base colour for the part -- a standard-palette name, a hex string, or an
            RGB tuple.
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
        with_density(PAPER_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


# --- Cardboard ---------------------------------------------------------------
class Cardboard(Enum):
    CORRUGATED = auto()


CARDBOARD_MATERIALS: dict[Cardboard, PaperMaterial] = {
    Cardboard.CORRUGATED: PaperMaterial(
        # identity
        name="Cardboard_CORRUGATED",
        family="corrugated_cardboard",
        # mechanical properties
        areal_density=Range(400, 700),
        # effective panel density (incl. flute voids); areal_density is the primary mass metric
        density=140,
        tensile_strength=Range(5, 25),
        thickness=Range(3, 5),
        # thermal properties
        specific_heat_capacity=Range(1300, 1400),
        thermal_conductivity=Range(0.05, 0.10),
    ),
}


def cardboard(
    grade: Cardboard = Cardboard.CORRUGATED,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[PaperMaterial]:
    """Corrugated cardboard as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to corrugated.
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
        with_density(CARDBOARD_MATERIALS[grade], density),
        finish,
        process=process,
    )


# --- Foamboard ---------------------------------------------------------------
class Foamboard(Enum):
    GENERIC = auto()


FOAMBOARD_MATERIALS: dict[Foamboard, PaperMaterial] = {
    Foamboard.GENERIC: PaperMaterial(
        # identity
        name="Foamboard_GENERIC",
        family="foamboard",
        # mechanical properties
        areal_density=Range(400, 550),
        density=120,
        tensile_strength=Range(2, 10),
        thickness=Range(3, 6),
        # thermal properties
        specific_heat_capacity=Range(1300, 1500),
        thermal_conductivity=Range(0.03, 0.06),
    ),
}


def foamboard(
    grade: Foamboard = Foamboard.GENERIC,
    color: Color | None = "white",
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[PaperMaterial]:
    """Foamboard as a ``FinishedMaterial``.

    Args:
        grade: Grade to select; defaults to generic.
        color: Base colour for the part -- a standard-palette name, a hex string, or an
            RGB tuple.
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
        with_density(FOAMBOARD_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


ALL_PAPERS = (
    *PAPER_MATERIALS.values(),
    *CARDBOARD_MATERIALS.values(),
    *FOAMBOARD_MATERIALS.values(),
)


if __name__ == "__main__":
    print(f"papers: {len(ALL_PAPERS)}")
    print()
    for _p in ALL_PAPERS:
        print(_p)
        print()

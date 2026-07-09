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

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import ArealMaterial, Range


@dataclass(frozen=True)
class PaperMaterial(ArealMaterial):
    """A paper good: the shared areal ranges (from ``ArealMaterial``). ``family`` is
    the three.js paper factory key; a part's colour lives on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "paper"


_Finish = AppliedFinish | list[AppliedFinish] | None


# --- Paper -------------------------------------------------------------------
class Paper(Enum):
    OFFICE = auto()


PAPER_MATERIALS: dict[Paper, PaperMaterial] = {
    Paper.OFFICE: PaperMaterial(
        name="Paper_OFFICE",
        density=800,
        areal_density=Range(70, 90),
        thickness=Range(0.09, 0.12),
        tensile_strength=Range(20, 60),
        thermal_conductivity=Range(0.05, 0.10),
        specific_heat_capacity=Range(1300, 1400),
        family="paper",
    ),
}


def paper(
    grade: Paper = Paper.OFFICE,
    color="white",
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PaperMaterial]:
    return FinishedMaterial(
        PAPER_MATERIALS[grade], finish, color=color, process=process
    )


# --- Cardboard ---------------------------------------------------------------
class Cardboard(Enum):
    CORRUGATED = auto()


CARDBOARD_MATERIALS: dict[Cardboard, PaperMaterial] = {
    Cardboard.CORRUGATED: PaperMaterial(
        name="Cardboard_CORRUGATED",
        # effective panel density (incl. flute voids); areal_density is the primary mass metric
        density=140,
        areal_density=Range(400, 700),
        thickness=Range(3, 5),
        tensile_strength=Range(5, 25),
        thermal_conductivity=Range(0.05, 0.10),
        specific_heat_capacity=Range(1300, 1400),
        family="corrugated_cardboard",
    ),
}


def cardboard(
    grade: Cardboard = Cardboard.CORRUGATED,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PaperMaterial]:
    return FinishedMaterial(CARDBOARD_MATERIALS[grade], finish, process=process)


# --- Foamboard ---------------------------------------------------------------
class Foamboard(Enum):
    GENERIC = auto()


FOAMBOARD_MATERIALS: dict[Foamboard, PaperMaterial] = {
    Foamboard.GENERIC: PaperMaterial(
        name="Foamboard_GENERIC",
        density=120,
        areal_density=Range(400, 550),
        thickness=Range(3, 6),
        tensile_strength=Range(2, 10),
        thermal_conductivity=Range(0.03, 0.06),
        specific_heat_capacity=Range(1300, 1500),
        family="foamboard",
    ),
}


def foamboard(
    grade: Foamboard = Foamboard.GENERIC,
    color="white",
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[PaperMaterial]:
    return FinishedMaterial(
        FOAMBOARD_MATERIALS[grade], finish, color=color, process=process
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

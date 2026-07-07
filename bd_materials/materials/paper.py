"""Range-based typical values for paper goods (paper, cardboard, foamboard).

Sibling of the other range modules using the shared :mod:`..core` primitives.
These are **areal goods**: the primary mass metric is grammage (``areal_density``,
g/m²), not volumetric density, and a cut sheet's mass is grammage x area.
``tensile_strength`` is the in-plane (machine-direction) value and is approximate
for these structured/layered materials. Grade and supplier variation is large --
treat as rough typicals.

Split into three single-grade families -- :class:`Paper`, :class:`Cardboard`,
:class:`Foamboard`. Paper and foamboard take a selectable ``color`` (default
white, the predominant shade). Corrugated cardboard is effectively only sold as
kraft, so it has no ``color`` -- the fixed look comes from its three.js
``corrugated_cardboard`` factory (case 1, like wood/metals).

Standalone: does not touch the point-value library or the finishes/PBR stack.
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


class Cardboard(Enum):
    CORRUGATED = auto()


CARDBOARD_MATERIALS: dict[Cardboard, PaperMaterial] = {
    Cardboard.CORRUGATED: PaperMaterial(
        name="Cardboard_CORRUGATED",
        density=140,
        areal_density=Range(400, 700),
        thickness=Range(3, 5),
        tensile_strength=Range(5, 25),
        thermal_conductivity=Range(0.05, 0.10),
        specific_heat_capacity=Range(1300, 1400),
        family="corrugated_cardboard",
    ),
}


class Foamboard(Enum):
    GENERIC = auto()


FOAMBOARD_MATERIALS: dict[Foamboard, PaperMaterial] = {
    Foamboard.GENERIC: PaperMaterial(
        name="Foamboard_GENERIC",
        density=100,
        areal_density=Range(400, 550),
        thickness=Range(3, 6),
        tensile_strength=Range(2, 10),
        thermal_conductivity=Range(0.03, 0.06),
        specific_heat_capacity=Range(1300, 1500),
        family="foamboard",
    ),
}


# ===========================================================================
# Family functions -- each defaults to its predominant intrinsic colour.
# ===========================================================================

_Finish = AppliedFinish | list[AppliedFinish] | None


def paper(
    grade: Paper = Paper.OFFICE,
    color="white",
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial:
    return FinishedMaterial(
        PAPER_MATERIALS[grade], finish, color=color, process=process
    )


def cardboard(
    grade: Cardboard = Cardboard.CORRUGATED,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial:
    return FinishedMaterial(CARDBOARD_MATERIALS[grade], finish, process=process)


def foamboard(
    grade: Foamboard = Foamboard.GENERIC,
    color="white",
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial:
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

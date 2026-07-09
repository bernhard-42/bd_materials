"""Typical-value property ranges for textiles (woven fabric, felt, leather).

Textiles are **areal goods**: the primary mass metric is grammage (``areal_density``,
g/m2), not volumetric density; the ``density`` field is only the effective bulk value.
``tensile_strength`` is the in-plane value and is approximate for these flexible
materials, so treat all values as rough typicals. (Leather isn't strictly a textile but
is grouped here as a soft areal good.)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from ..finished import FinishedMaterial, Process
from ..finishes import AppliedFinish
from ..core import ArealMaterial, Range


@dataclass(frozen=True)
class TextileMaterial(ArealMaterial):
    """A textile: the shared areal ranges (from ``ArealMaterial``). ``family`` is the
    three.js textile factory key; a part's colour lives on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "textile"


_Finish = AppliedFinish | list[AppliedFinish] | None


# --- Woven -------------------------------------------------------------------
class Woven(Enum):
    GENERIC = auto()


WOVEN_MATERIALS: dict[Woven, TextileMaterial] = {
    Woven.GENERIC: TextileMaterial(
        # identity
        name="Woven_GENERIC",
        family="fabric_weave",
        # mechanical properties
        areal_density=Range(150, 300),
        density=500,
        tensile_strength=Range(10, 50),
        thickness=Range(0.3, 0.6),
        # thermal properties
        specific_heat_capacity=Range(1300, 1700),
        thermal_conductivity=Range(0.03, 0.07),
    ),
}


def woven(
    grade: Woven = Woven.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[TextileMaterial]:
    return FinishedMaterial(
        WOVEN_MATERIALS[grade], finish, color=color, process=process
    )


# --- Felt --------------------------------------------------------------------
class Felt(Enum):
    GENERIC = auto()


FELT_MATERIALS: dict[Felt, TextileMaterial] = {
    Felt.GENERIC: TextileMaterial(
        # identity
        name="Felt_GENERIC",
        family="felt",
        # mechanical properties
        areal_density=Range(200, 400),
        density=120,
        tensile_strength=Range(2, 10),
        thickness=Range(2, 4),
        # thermal properties
        specific_heat_capacity=Range(1300, 1700),
        thermal_conductivity=Range(0.04, 0.08),
    ),
}


def felt(
    grade: Felt = Felt.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[TextileMaterial]:
    return FinishedMaterial(FELT_MATERIALS[grade], finish, color=color, process=process)


# --- Leather -----------------------------------------------------------------
class Leather(Enum):
    GENERIC = auto()


LEATHER_MATERIALS: dict[Leather, TextileMaterial] = {
    Leather.GENERIC: TextileMaterial(
        # identity
        name="Leather_GENERIC",
        family="leather",
        # mechanical properties
        areal_density=Range(800, 1600),
        density=950,
        tensile_strength=Range(10, 30),
        thickness=Range(1, 3),
        # thermal properties
        specific_heat_capacity=Range(1500, 2000),
        thermal_conductivity=Range(0.14, 0.20),
    ),
}


def leather(
    grade: Leather = Leather.GENERIC,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[TextileMaterial]:
    return FinishedMaterial(
        LEATHER_MATERIALS[grade], finish, color=color, process=process
    )


ALL_TEXTILES = (
    *WOVEN_MATERIALS.values(),
    *FELT_MATERIALS.values(),
    *LEATHER_MATERIALS.values(),
)


if __name__ == "__main__":
    print(f"textiles: {len(ALL_TEXTILES)}")
    print()
    for _t in ALL_TEXTILES:
        print(_t)
        print()

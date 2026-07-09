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


class Textile(Enum):
    WOVEN = auto()
    FELT = auto()
    LEATHER = auto()


TEXTILE_MATERIALS: dict[Textile, TextileMaterial] = {
    Textile.WOVEN: TextileMaterial(
        name="Textile_WOVEN",
        density=500,
        areal_density=Range(150, 300),
        thickness=Range(0.3, 0.6),
        tensile_strength=Range(10, 50),
        thermal_conductivity=Range(0.03, 0.07),
        specific_heat_capacity=Range(1300, 1700),
        family="fabric_weave",
    ),
    Textile.FELT: TextileMaterial(
        name="Textile_FELT",
        density=120,
        areal_density=Range(200, 400),
        thickness=Range(2, 4),
        tensile_strength=Range(2, 10),
        thermal_conductivity=Range(0.04, 0.08),
        specific_heat_capacity=Range(1300, 1700),
        family="felt",
    ),
    Textile.LEATHER: TextileMaterial(
        name="Textile_LEATHER",
        density=950,
        areal_density=Range(800, 1600),
        thickness=Range(1, 3),
        tensile_strength=Range(10, 30),
        thermal_conductivity=Range(0.14, 0.20),
        specific_heat_capacity=Range(1500, 2000),
        family="leather",
    ),
}


_Finish = AppliedFinish | list[AppliedFinish] | None


def textile(
    grade: Textile = Textile.WOVEN,
    color=None,
    finish: _Finish = None,
    process: Process | None = None,
) -> FinishedMaterial[TextileMaterial]:
    return FinishedMaterial(
        TEXTILE_MATERIALS[grade], finish, color=color, process=process
    )


ALL_TEXTILES = tuple(TEXTILE_MATERIALS.values())


if __name__ == "__main__":
    print(f"textiles: {len(ALL_TEXTILES)}")
    print()
    for _t in ALL_TEXTILES:
        print(_t)
        print()

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

from ..finished import Color, FinishedMaterial, FinishSpec, Process
from ..core import ArealMaterial, Range, with_density


@dataclass(frozen=True, kw_only=True)
class TextileMaterial(ArealMaterial):
    """A textile: the shared areal ranges (from ``ArealMaterial``). ``family`` is the
    three.js textile factory key; a part's colour lives on the ``FinishedMaterial``.
    """

    category: ClassVar[str] = "textile"


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
    color: Color | None = None,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[TextileMaterial]:
    """Woven fabric as a ``FinishedMaterial``.

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
        with_density(WOVEN_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
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
    color: Color | None = None,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[TextileMaterial]:
    """Felt as a ``FinishedMaterial``.

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
        with_density(FELT_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
    )


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
    color: Color | None = None,
    finish: FinishSpec = None,
    process: Process | None = None,
    density: float | None = None,
) -> FinishedMaterial[TextileMaterial]:
    """Leather as a ``FinishedMaterial``.

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
        with_density(LEATHER_MATERIALS[grade], density),
        finish,
        color=color,
        process=process,
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

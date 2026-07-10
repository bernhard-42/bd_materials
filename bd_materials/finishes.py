"""Surface finishes: the finish catalog + the ergonomic finish functions.

Finishes are grouped by process into enums (:class:`Mechanical`, :class:`Chemical`,
:class:`MetalPlating`, :class:`Coating`, :class:`Marking`), each backed by a
``<GROUP>_FINISHES`` dict keyed by that enum -- the maintenance backbone. The
**public API is the flat verb functions** (``anodize("blue")``, ``powder_coat(...)``),
which bind a colour (and, for paints/coatings, a :class:`Sheen`) to a finish and
return an :class:`AppliedFinish`.

A ``Finish`` is purely its intrinsic spec (name + optional notes). Where a finish is
*typically* used (its substrates) is a separate concern and lives in
:mod:`.applicability` -- one central material<->finish table.

Finishes are advisory, not gated: **any finish may be specified on any material**.

Which colours a finish is typically offered in is advisory and deliberately not
modelled on the ``Finish`` -- any colour may be applied per part (a name in
``pbr._COLOR_HEX`` renders as that swatch; anything else passes through). Sheen
(matte/gloss) is a per-application choice like colour -- it rides on the
``AppliedFinish``, not the ``Finish``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Sheen(Enum):
    """Surface sheen of a paint/coating -- a per-application choice like colour."""

    GLOSS = auto()
    MATTE = auto()


@dataclass(frozen=True)
class Finish:
    """A surface finish's intrinsic spec (name + optional notes). Which colours a
    finish is typically offered in is advisory and not modelled here; substrate
    applicability lives in :mod:`.applicability`, not here."""

    name: str
    notes: str | None = None


# ===========================================================================
# Finish catalog: one group enum + one <GROUP>_FINISHES dict per process family.
# ===========================================================================


class Mechanical(Enum):
    BEAD_BLAST = auto()
    BRUSHED = auto()
    FINE_SANDING = auto()
    SMOOTH_MACHINING = auto()
    ELECTROPOLISHED = auto()


MECHANICAL_FINISHES: dict[Mechanical, Finish] = {
    Mechanical.BEAD_BLAST: Finish("Bead Blast"),
    Mechanical.BRUSHED: Finish("Brushed"),
    Mechanical.FINE_SANDING: Finish("Fine Sanding"),
    Mechanical.SMOOTH_MACHINING: Finish(
        "Smooth machining (Ra1.6µm)", notes="as-machined roughness spec"
    ),
    Mechanical.ELECTROPOLISHED: Finish("Electropolished"),
}


class Chemical(Enum):
    ANODIZED = auto()
    CHEM_FILM = auto()
    CONDUCTIVE_OXIDATION = auto()
    BLACK_OXIDE = auto()
    PASSIVATION = auto()
    PICKLING = auto()
    DYEING = auto()


CHEMICAL_FINISHES: dict[Chemical, Finish] = {
    Chemical.ANODIZED: Finish("Anodized"),
    Chemical.CHEM_FILM: Finish("Chemical conversion coat (Chem film)"),
    Chemical.CONDUCTIVE_OXIDATION: Finish("Electrically conductive oxidation"),
    Chemical.BLACK_OXIDE: Finish("Black oxide"),
    Chemical.PASSIVATION: Finish("Passivation"),
    Chemical.PICKLING: Finish("Pickling"),
    Chemical.DYEING: Finish(
        "Dyeing", notes="anodized aluminum, or dyeable polymers (esp. nylon)"
    ),
}


class MetalPlating(Enum):
    CHROME_PLATING = auto()
    GOLD_PLATING = auto()
    NICKEL_PLATING = auto()
    SILVER_PLATING = auto()
    TIN_PLATING = auto()
    PVD = auto()
    ZINC_PLATING = auto()
    VACUUM_PLATING = auto()


METAL_PLATING_FINISHES: dict[MetalPlating, Finish] = {
    MetalPlating.CHROME_PLATING: Finish("Chrome plating"),
    MetalPlating.GOLD_PLATING: Finish("Gold plating"),
    MetalPlating.NICKEL_PLATING: Finish("Nickel plating"),
    MetalPlating.SILVER_PLATING: Finish("Silver plating"),
    MetalPlating.TIN_PLATING: Finish("Tin plating"),
    MetalPlating.PVD: Finish("PVD (Physical Vapor Deposition)"),
    MetalPlating.ZINC_PLATING: Finish(
        "Zinc plating", notes="corrosion protection for ferrous steels"
    ),
    MetalPlating.VACUUM_PLATING: Finish("Vacuum plating"),
}


class Coating(Enum):
    POWDER_COAT = auto()
    ELECTROPHORESIS = auto()
    SPRAY_PAINT = auto()


COATING_FINISHES: dict[Coating, Finish] = {
    Coating.POWDER_COAT: Finish("Powder coat"),
    Coating.ELECTROPHORESIS: Finish("Electrophoresis"),
    Coating.SPRAY_PAINT: Finish("Spray painting"),
}


class Marking(Enum):
    LASER_ENGRAVING = auto()
    ETCHING = auto()
    SILKSCREEN = auto()


MARKING_FINISHES: dict[Marking, Finish] = {
    Marking.LASER_ENGRAVING: Finish("Laser engraving"),
    Marking.ETCHING: Finish("Etching"),
    Marking.SILKSCREEN: Finish("Silkscreen"),
}


# All finishes flattened; used by :mod:`.applicability`.
ALL_FINISHES = (
    *MECHANICAL_FINISHES.values(),
    *CHEMICAL_FINISHES.values(),
    *METAL_PLATING_FINISHES.values(),
    *COATING_FINISHES.values(),
    *MARKING_FINISHES.values(),
)


# ===========================================================================
# Applied finishes: the flat verb functions bind colour/sheen to a finish.
# ===========================================================================


@dataclass(frozen=True)
class AppliedFinish:
    """A finish plus its per-application appearance choices (colour, sheen) --
    produced by the finish functions below."""

    finish: Finish
    color: str | None = None
    sheen: Sheen | None = None  # None = finish has no sheen choice


# --- mechanical (no colour) ------------------------------------------------
def bead_blast() -> AppliedFinish:
    """Bead-blasted matte finish."""
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.BEAD_BLAST])


def brushed() -> AppliedFinish:
    """Brushed directional-satin finish."""
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.BRUSHED])


def fine_sanding() -> AppliedFinish:
    """Fine-sanded smooth-matte finish."""
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.FINE_SANDING])


def smooth_machining() -> AppliedFinish:
    """Smooth as-machined finish (Ra 1.6 µm)."""
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.SMOOTH_MACHINING])


def electropolish() -> AppliedFinish:
    """Electropolished bright finish."""
    return AppliedFinish(MECHANICAL_FINISHES[Mechanical.ELECTROPOLISHED])


# --- chemical --------------------------------------------------------------
def anodize(color: str) -> AppliedFinish:
    """Anodized finish in ``color``.

    Args:
        color: The anodize colour. Mandatory -- anodising is done to add colour
            ("natural" is still an explicit choice, not the absence of one).

    Returns:
        The applied finish.
    """
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.ANODIZED], color)


def chem_film() -> AppliedFinish:
    """Chromate conversion coating (chem film)."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.CHEM_FILM])


def conductive_oxidation() -> AppliedFinish:
    """Electrically-conductive oxidation coating."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.CONDUCTIVE_OXIDATION])


def black_oxide() -> AppliedFinish:
    """Black-oxide conversion finish."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.BLACK_OXIDE])


def passivate() -> AppliedFinish:
    """Passivation finish (stainless corrosion resistance)."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.PASSIVATION])


def pickle() -> AppliedFinish:
    """Pickling finish (oxide / scale removal)."""
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.PICKLING])


def dye(color: str) -> AppliedFinish:
    """Dyed finish in ``color`` (anodized aluminium or dyeable polymers).

    Args:
        color: The dye colour.

    Returns:
        The applied finish.
    """
    return AppliedFinish(CHEMICAL_FINISHES[Chemical.DYEING], color)


# --- metal plating ---------------------------------------------------------
def chrome() -> AppliedFinish:
    """Chrome plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.CHROME_PLATING])


def gold_plate() -> AppliedFinish:
    """Gold plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.GOLD_PLATING])


def nickel_plate() -> AppliedFinish:
    """Nickel plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.NICKEL_PLATING])


def silver_plate() -> AppliedFinish:
    """Silver plating."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.SILVER_PLATING])


def tin_plate() -> AppliedFinish:
    """Tin plating (matte, solderable)."""
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.TIN_PLATING])


def pvd(color: str = "clear") -> AppliedFinish:
    """PVD coating in ``color``.

    Args:
        color: "clear" (default) is bright natural PVD, with the substrate showing
            through; colours are opt-in.

    Returns:
        The applied finish.
    """
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.PVD], color)


def zinc_plate(color: str = "clear") -> AppliedFinish:
    """Zinc plating in ``color``.

    Args:
        color: "clear" (default) is the clear/bright chromate -- the natural zinc look;
            others are chromate tints.

    Returns:
        The applied finish.
    """
    return AppliedFinish(METAL_PLATING_FINISHES[MetalPlating.ZINC_PLATING], color)


def vacuum_plating(color: str, sheen: Sheen = Sheen.GLOSS) -> AppliedFinish:
    """Vacuum-metallised plating in ``color``.

    Args:
        color: The plating colour.
        sheen: Gloss (default) or matte.

    Returns:
        The applied finish.
    """
    return AppliedFinish(
        METAL_PLATING_FINISHES[MetalPlating.VACUUM_PLATING], color, sheen
    )


# --- coating / paint (sheen: gloss default, matte optional) ----------------
def powder_coat(color: str, sheen: Sheen = Sheen.GLOSS) -> AppliedFinish:
    """Powder coat in ``color``.

    Args:
        color: The coat colour (any, to spec).
        sheen: Gloss (default) or matte.

    Returns:
        The applied finish.
    """
    return AppliedFinish(COATING_FINISHES[Coating.POWDER_COAT], color, sheen)


def spray_paint(color: str, sheen: Sheen = Sheen.GLOSS) -> AppliedFinish:
    """Spray paint in ``color``.

    Args:
        color: The paint colour (any, to spec).
        sheen: Gloss (default) or matte.

    Returns:
        The applied finish.
    """
    return AppliedFinish(COATING_FINISHES[Coating.SPRAY_PAINT], color, sheen)


def electrophoresis() -> AppliedFinish:
    """Electrophoretic e-coat -- always black (no colour choice)."""
    return AppliedFinish(COATING_FINISHES[Coating.ELECTROPHORESIS])


# --- marking ---------------------------------------------------------------
def laser_engrave() -> AppliedFinish:
    """Laser-engraved marking."""
    return AppliedFinish(MARKING_FINISHES[Marking.LASER_ENGRAVING])


def etch() -> AppliedFinish:
    """Etched marking."""
    return AppliedFinish(MARKING_FINISHES[Marking.ETCHING])


def silkscreen(color: str = "black") -> AppliedFinish:
    """Silkscreen marking in ``color`` (default black).

    Args:
        color: The ink colour. Note PBR ignores markings, so this is metadata.

    Returns:
        The applied finish.
    """
    return AppliedFinish(MARKING_FINISHES[Marking.SILKSCREEN], color)


__all__ = [
    # types + vocab
    "Finish",
    "AppliedFinish",
    "Sheen",
    # catalog (maintenance backbone)
    "Mechanical",
    "Chemical",
    "MetalPlating",
    "Coating",
    "Marking",
    "MECHANICAL_FINISHES",
    "CHEMICAL_FINISHES",
    "METAL_PLATING_FINISHES",
    "COATING_FINISHES",
    "MARKING_FINISHES",
    "ALL_FINISHES",
    # finish functions (the public API)
    "bead_blast",
    "brushed",
    "fine_sanding",
    "smooth_machining",
    "electropolish",
    "anodize",
    "chem_film",
    "conductive_oxidation",
    "black_oxide",
    "passivate",
    "pickle",
    "dye",
    "chrome",
    "gold_plate",
    "nickel_plate",
    "silver_plate",
    "tin_plate",
    "pvd",
    "zinc_plate",
    "vacuum_plating",
    "powder_coat",
    "spray_paint",
    "electrophoresis",
    "laser_engrave",
    "etch",
    "silkscreen",
]

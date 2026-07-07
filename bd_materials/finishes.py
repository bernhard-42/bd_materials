"""Surface finishes, with *typical-use* hints and standard colour options.

Finishes are advisory, not gated: **any finish may be specified on any
material** -- a given manufacturer may anodize titanium, powder-coat a polymer,
etc. Each ``Finish`` only carries a *hint* of the substrates it is typically used
on (by material ``category`` and/or ``family``). ``is_typical_for(material)``
answers the hint; it never restricts. Hints are generic (chemistry/industry
norms), not any one vendor's menu.

``colors`` is a standard palette per finish drawn from ``STANDARD_COLORS``:
``()`` = no colour choice (N/A / substrate colour), ``("black",)`` = single,
``("champagne", "rose gold", ...)`` = palette, and ``CUSTOM`` = any colour to
spec (RAL/Pantone paint & powder).
"""

from __future__ import annotations

from dataclasses import dataclass

from collections.abc import Iterable

from .core import RangeMaterial

# --- substrate groups (for hints only) -------------------------------------
FERROUS = frozenset({"mild_steel", "alloy_steel", "tool_steel", "spring_steel"})
METAL = frozenset({"metal"})
NON_FERROUS_METALS = frozenset({"aluminum", "stainless", "brass", "copper", "titanium"})
PAINTABLE = frozenset({"metal", "plastic", "composite", "resin", "wood"})
COATABLE_POLY = frozenset({"metal", "plastic", "composite", "resin"})
EVERYTHING = frozenset(
    {"metal", "plastic", "composite", "resin", "wood", "glass", "paper", "textile"}
)

# --- standard finish colours (controlled vocabulary) -----------------------
CUSTOM = "custom"  # any colour to specification (RAL / Pantone)
STANDARD_COLORS = frozenset(
    {
        "natural",
        "clear",
        "black",
        "white",
        "gray",
        "gunmetal",
        "silver",
        "nickel",
        "chrome",
        "gold",
        "rose gold",
        "champagne",
        "brown",
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple",
        CUSTOM,
    }
)


@dataclass(frozen=True)
class Finish:
    name: str
    kind: str  # mechanical | conversion | plating | coating | paint | color | marking
    typical_categories: frozenset[str] = (
        frozenset()
    )  # hint: material.category in here ...
    typical_families: frozenset[str] = frozenset()  # ... or material.family in here
    colors: tuple[str, ...] = ()  # standard palette; () = N/A / substrate colour
    notes: str | None = None

    def is_typical_for(self, material: RangeMaterial) -> bool:
        """Hint only -- is this finish *typically* used on this material?

        Never a constraint: any finish may still be applied to any material.
        """
        return (
            material.category in self.typical_categories
            or material.family in self.typical_families
        )


FINISHES: dict[str, Finish] = {}


def _slug(text: str) -> str:
    """Lowercase, alnum-only slug (spaces/punctuation collapse to single '-')."""
    out: list[str] = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def _f(finish: Finish) -> Finish:
    unknown = set(finish.colors) - STANDARD_COLORS
    if unknown:
        raise ValueError(f"{finish.name}: non-standard colours {sorted(unknown)}")
    FINISHES[_slug(finish.name)] = finish
    return finish


# --- mechanical (no added colour) ------------------------------------------
BEAD_BLAST = _f(
    Finish(
        "Bead Blast",
        "mechanical",
        typical_categories=frozenset({"metal", "plastic", "composite"}),
    )
)
BRUSHED = _f(Finish("Brushed", "mechanical", typical_categories=METAL))
FINE_SANDING = _f(
    Finish(
        "Fine Sanding",
        "mechanical",
        typical_categories=frozenset({"metal", "plastic", "composite", "wood"}),
    )
)
SMOOTH_MACHINING = _f(
    Finish(
        "Smooth machining (Ra1.6µm)",
        "mechanical",
        typical_categories=frozenset({"metal", "plastic", "composite", "wood"}),
        notes="as-machined roughness spec",
    )
)
ELECTROPOLISHED = _f(
    Finish(
        "Electropolished",
        "mechanical",
        typical_families=frozenset({"stainless", "titanium"}),
    )
)

# --- conversion / oxide ----------------------------------------------------
ANODIZED = _f(
    Finish(
        "Anodized",
        "conversion",
        typical_families=frozenset({"aluminum", "titanium"}),
        colors=(
            "natural",
            "black",
            "gray",
            "gold",
            "rose gold",
            "red",
            "blue",
            "champagne",
            "brown",
            "purple",
            "green",
            "orange",
        ),
    )
)
CHEM_FILM = _f(
    Finish(
        "Chemical conversion coat (Chem film)",
        "conversion",
        typical_families=frozenset({"aluminum"}),
        colors=("clear", "gold"),
    )
)
CONDUCTIVE_OXIDATION = _f(
    Finish(
        "Electrically conductive oxidation",
        "conversion",
        typical_families=frozenset({"aluminum"}),
        colors=("clear",),
    )
)
BLACK_OXIDE = _f(
    Finish(
        "Black oxide",
        "conversion",
        typical_families=FERROUS | frozenset({"stainless", "copper", "brass"}),
        colors=("black",),
    )
)
PASSIVATION = _f(
    Finish(
        "Passivation",
        "conversion",
        typical_families=frozenset({"stainless", "titanium"}),
    )
)
PICKLING = _f(
    Finish(
        "Pickling", "conversion", typical_families=FERROUS | frozenset({"stainless"})
    )
)
DYEING = _f(
    Finish(
        "Dyeing",
        "color",
        typical_categories=frozenset({"plastic", "composite", "resin"}),
        typical_families=frozenset({"aluminum"}),
        colors=(CUSTOM,),
        notes="anodized aluminum, or dyeable polymers (esp. nylon)",
    )
)

# --- plating (metallic colour is inherent) ---------------------------------
CHROME_PLATING = _f(
    Finish("Chrome plating", "plating", typical_categories=METAL, colors=("chrome",))
)
GOLD_PLATING = _f(
    Finish("Gold plating", "plating", typical_categories=METAL, colors=("gold",))
)
NICKEL_PLATING = _f(
    Finish("Nickel plating", "plating", typical_categories=METAL, colors=("nickel",))
)
SILVER_PLATING = _f(
    Finish("Silver plating", "plating", typical_categories=METAL, colors=("silver",))
)
TIN_PLATING = _f(
    Finish("Tin plating", "plating", typical_categories=METAL, colors=("silver",))
)
PVD = _f(
    Finish(
        "PVD (Physical Vapor Deposition)",
        "plating",
        typical_categories=METAL,
        colors=("gold", "rose gold", "black", "gunmetal", "blue"),
    )
)
ZINC_PLATING = _f(
    Finish(
        "Zinc plating",
        "plating",
        typical_families=FERROUS,
        colors=("clear", "blue", "yellow", "black"),
        notes="corrosion protection for ferrous steels",
    )
)

# --- coating / paint -------------------------------------------------------
POWDER_COAT_GLOSS = _f(
    Finish(
        "Powder coat - High gloss",
        "coating",
        typical_categories=METAL,
        colors=(CUSTOM,),
    )
)
POWDER_COAT_MATT = _f(
    Finish("Powder coat - Matt", "coating", typical_categories=METAL, colors=(CUSTOM,))
)
ELECTROPHORESIS = _f(
    Finish("Electrophoresis", "coating", typical_categories=METAL, colors=("black",))
)
SPRAY_PAINT_GLOSS = _f(
    Finish(
        "Spray painting - High gloss paint",
        "paint",
        typical_categories=PAINTABLE,
        colors=(CUSTOM,),
    )
)
SPRAY_PAINT_MATT = _f(
    Finish(
        "Spray painting - Matt paint",
        "paint",
        typical_categories=PAINTABLE,
        colors=(CUSTOM,),
    )
)
VACUUM_PLATING_GLOSS = _f(
    Finish(
        "Vacuum plating - High gloss paint",
        "coating",
        typical_categories=COATABLE_POLY,
        colors=(CUSTOM,),
    )
)
VACUUM_PLATING_MATT = _f(
    Finish(
        "Vacuum plating - Matt paint",
        "coating",
        typical_categories=COATABLE_POLY,
        colors=(CUSTOM,),
    )
)

# --- marking ---------------------------------------------------------------
LASER_ENGRAVING = _f(
    Finish("Laser engraving", "marking", typical_categories=EVERYTHING)
)
ETCHING = _f(
    Finish("Etching", "marking", typical_categories=frozenset({"metal", "glass"}))
)
SILKSCREEN = _f(
    Finish(
        "Silkscreen",
        "marking",
        typical_categories=frozenset(
            {"metal", "plastic", "composite", "resin", "glass"}
        ),
        colors=(CUSTOM,),
    )
)


# --- queries (hints, not constraints) --------------------------------------
def typical_finishes_for(material: RangeMaterial) -> list[Finish]:
    """Finishes *typically* used on this material (a hint; not exhaustive)."""
    return [f for f in FINISHES.values() if f.is_typical_for(material)]


def typical_materials_for(
    finish: Finish, materials: Iterable[RangeMaterial]
) -> list[RangeMaterial]:
    """Which of ``materials`` this finish is *typically* used on (a hint).

    Pass the candidate set explicitly (e.g. ``metals.ALL_METALS + plastics.ALL_PLASTICS``);
    there is no central registry to enumerate.
    """
    return [m for m in materials if finish.is_typical_for(m)]


# --- applied finishes: functions bind a colour to a finish (public API) -----


@dataclass(frozen=True)
class AppliedFinish:
    """A finish plus its chosen colour -- produced by the finish functions below."""

    finish: Finish
    color: str | None = None


# mechanical (no colour)


def bead_blast():
    return AppliedFinish(BEAD_BLAST)


def brushed():
    return AppliedFinish(BRUSHED)


def fine_sanding():
    return AppliedFinish(FINE_SANDING)


def smooth_machining():
    return AppliedFinish(SMOOTH_MACHINING)


def electropolish():
    return AppliedFinish(ELECTROPOLISHED)


# conversion / oxide


def anodize(color=None):
    return AppliedFinish(ANODIZED, color)


def chem_film():
    return AppliedFinish(CHEM_FILM)


def conductive_oxidation():
    return AppliedFinish(CONDUCTIVE_OXIDATION)


def black_oxide():
    return AppliedFinish(BLACK_OXIDE)


def passivate():
    return AppliedFinish(PASSIVATION)


def pickle():
    return AppliedFinish(PICKLING)


def dye(color):
    return AppliedFinish(DYEING, color)


# plating


def chrome():
    return AppliedFinish(CHROME_PLATING)


def gold_plate():
    return AppliedFinish(GOLD_PLATING)


def nickel_plate():
    return AppliedFinish(NICKEL_PLATING)


def silver_plate():
    return AppliedFinish(SILVER_PLATING)


def tin_plate():
    return AppliedFinish(TIN_PLATING)


def zinc_plate(color=None):
    return AppliedFinish(ZINC_PLATING, color)


def pvd(color=None):
    return AppliedFinish(PVD, color)


# coating / paint (glossy by default; matt=True for the matt variant)


def powder_coat(color, matt=False):
    return AppliedFinish(POWDER_COAT_MATT if matt else POWDER_COAT_GLOSS, color)


def spray_paint(color, matt=False):
    return AppliedFinish(SPRAY_PAINT_MATT if matt else SPRAY_PAINT_GLOSS, color)


def vacuum_plating(color, matt=False):
    return AppliedFinish(VACUUM_PLATING_MATT if matt else VACUUM_PLATING_GLOSS, color)


def electrophoresis(color=None):
    return AppliedFinish(ELECTROPHORESIS, color)


# marking


def laser_engrave():
    return AppliedFinish(LASER_ENGRAVING)


def etch():
    return AppliedFinish(ETCHING)


def silkscreen(color=None):
    return AppliedFinish(SILKSCREEN, color)


__all__ = [
    "Finish",
    "AppliedFinish",
    "FINISHES",
    "CUSTOM",
    "STANDARD_COLORS",
    "FERROUS",
    "typical_finishes_for",
    "typical_materials_for",
    # finish functions (the public API; raw constants stay module-internal)
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
    "zinc_plate",
    "pvd",
    "powder_coat",
    "spray_paint",
    "vacuum_plating",
    "electrophoresis",
    "laser_engrave",
    "etch",
    "silkscreen",
]

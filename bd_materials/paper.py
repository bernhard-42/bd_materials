"""Paper materials (paper, board, foamboard) -- accessed by functions.

Areal goods: sized by grammage (g/m2) + thickness, semi-rigid in-plane. Mass
comes from area via ``mass_g_from_area_mm2`` (inherited from ``ArealMaterial``),
not volume. Values are rough typicals -- grade/supplier variation is large.

    from bd_materials import paper
    paper.foamboard()
    paper.all()
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import ArealMaterial


@dataclass(frozen=True)
class PaperMaterial(ArealMaterial):
    category: str = "paper"


_PAPER = PaperMaterial(
    name="Paper",
    family="paper",
    grade="office 80gsm",
    source="typical",
    density_kg_m3=800.0,
    areal_density_g_m2=80.0,
    thickness_mm=0.1,
    tensile_strength_md_pa=40e6,
)
_CORRUGATED_CARDBOARD = PaperMaterial(
    name="Corrugated Cardboard",
    family="paper",
    grade="single-wall B-flute",
    source="typical",
    density_kg_m3=140.0,
    areal_density_g_m2=550.0,
    thickness_mm=4.0,
)
_FOAMBOARD = PaperMaterial(
    name="Foamboard",
    family="paper",
    grade="paper-faced foam core",
    source="typical",
    density_kg_m3=100.0,
    areal_density_g_m2=480.0,
    thickness_mm=5.0,
)


def paper() -> PaperMaterial:
    return _PAPER


def corrugated_cardboard() -> PaperMaterial:
    return _CORRUGATED_CARDBOARD


def foamboard() -> PaperMaterial:
    return _FOAMBOARD


_ALL = (_PAPER, _CORRUGATED_CARDBOARD, _FOAMBOARD)


def all() -> tuple[PaperMaterial, ...]:
    """Every curated paper instance (for tooling / the self-check)."""
    return _ALL


__all__ = ["PaperMaterial", "paper", "corrugated_cardboard", "foamboard", "all"]

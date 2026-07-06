"""Paper materials (paper, board, foamboard).

Areal goods: sized by grammage (g/m2) + thickness, semi-rigid in-plane. Mass
comes from area via ``mass_g_from_area_mm2`` (inherited from ``ArealMaterial``),
not volume. Values are rough typicals -- grade/supplier variation is large.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import ArealMaterial, _reg


@dataclass(frozen=True)
class PaperMaterial(ArealMaterial):
    category: str = "paper"


PAPER = _reg(
    PaperMaterial(
        name="Paper",
        family="paper",
        grade="office 80gsm",
        source="typical",
        density_kg_m3=800.0,
        areal_density_g_m2=80.0,
        thickness_mm=0.1,
        tensile_strength_md_pa=40e6,
    )
)
CORRUGATED_CARDBOARD = _reg(
    PaperMaterial(
        name="Corrugated Cardboard",
        family="paper",
        grade="single-wall B-flute",
        source="typical",
        density_kg_m3=140.0,
        areal_density_g_m2=550.0,
        thickness_mm=4.0,
    )
)
FOAMBOARD = _reg(
    PaperMaterial(
        name="Foamboard",
        family="paper",
        grade="paper-faced foam core",
        source="typical",
        density_kg_m3=100.0,
        areal_density_g_m2=480.0,
        thickness_mm=5.0,
    )
)


__all__ = ["PaperMaterial", "PAPER", "CORRUGATED_CARDBOARD", "FOAMBOARD"]

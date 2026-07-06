"""Textile materials (woven/knit fabric, felt, leather).

Areal goods: sized by grammage (g/m2) + thickness, flexible and drapey. Mass
comes from area via ``mass_g_from_area_mm2`` (inherited from ``ArealMaterial``),
not volume. Properties are highly grade-dependent -- treat as rough typicals.
(Leather isn't strictly a textile but is grouped here as a soft areal good.)
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import ArealMaterial, _reg


@dataclass(frozen=True)
class TextileMaterial(ArealMaterial):
    category: str = "textile"


FABRIC_WEAVE = _reg(
    TextileMaterial(
        name="Woven Fabric",
        family="textile",
        grade="plain weave",
        source="typical",
        density_kg_m3=500.0,
        areal_density_g_m2=200.0,
        thickness_mm=0.4,
    )
)
FABRIC_KNIT = _reg(
    TextileMaterial(
        name="Knit Fabric",
        family="textile",
        grade="jersey knit",
        source="typical",
        density_kg_m3=370.0,
        areal_density_g_m2=220.0,
        thickness_mm=0.6,
    )
)
FELT = _reg(
    TextileMaterial(
        name="Felt",
        family="textile",
        grade="wool/synthetic felt",
        source="typical",
        density_kg_m3=120.0,
        areal_density_g_m2=300.0,
        thickness_mm=2.5,
    )
)
LEATHER = _reg(
    TextileMaterial(
        name="Leather",
        family="textile",
        grade="veg-tanned",
        source="typical",
        density_kg_m3=860.0,
        areal_density_g_m2=1400.0,
        thickness_mm=1.6,
        tensile_strength_md_pa=25e6,
    )
)


__all__ = ["TextileMaterial", "FABRIC_WEAVE", "FABRIC_KNIT", "FELT", "LEATHER"]

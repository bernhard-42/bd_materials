"""Textile materials (woven/knit fabric, felt, leather) -- accessed by functions.

Areal goods: sized by grammage (g/m2) + thickness, flexible and drapey. Mass
comes from area via ``mass_g_from_area_mm2`` (inherited from ``ArealMaterial``),
not volume. Properties are highly grade-dependent -- treat as rough typicals.
(Leather isn't strictly a textile but is grouped here as a soft areal good.)

    from bd_materials import textile
    textile.felt()
    textile.all()
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import ArealMaterial


@dataclass(frozen=True)
class TextileMaterial(ArealMaterial):
    category: str = "textile"


_WOVEN = TextileMaterial(
    name="Woven Fabric",
    family="textile",
    grade="plain weave",
    source="typical",
    density_kg_m3=500.0,
    areal_density_g_m2=200.0,
    thickness_mm=0.4,
)
_KNIT = TextileMaterial(
    name="Knit Fabric",
    family="textile",
    grade="jersey knit",
    source="typical",
    density_kg_m3=370.0,
    areal_density_g_m2=220.0,
    thickness_mm=0.6,
)
_FELT = TextileMaterial(
    name="Felt",
    family="textile",
    grade="wool/synthetic felt",
    source="typical",
    density_kg_m3=120.0,
    areal_density_g_m2=300.0,
    thickness_mm=2.5,
)
_LEATHER = TextileMaterial(
    name="Leather",
    family="textile",
    grade="veg-tanned",
    source="typical",
    density_kg_m3=860.0,
    areal_density_g_m2=1400.0,
    thickness_mm=1.6,
    tensile_strength_md_pa=25e6,
)


def woven() -> TextileMaterial:
    return _WOVEN


def knit() -> TextileMaterial:
    return _KNIT


def felt() -> TextileMaterial:
    return _FELT


def leather() -> TextileMaterial:
    return _LEATHER


_ALL = (_WOVEN, _KNIT, _FELT, _LEATHER)


def all() -> tuple[TextileMaterial, ...]:
    """Every curated textile instance (for tooling / the self-check)."""
    return _ALL


__all__ = ["TextileMaterial", "woven", "knit", "felt", "leather", "all"]

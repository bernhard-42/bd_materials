"""Glass -- an isotropic brittle solid, accessed by a family function.

Glass is isotropic linear-elastic, so ``GlassMaterial`` is a thin
``IsotropicSolidMaterial`` subclass; it only adds ``thickness_mm``, the pane
thickness that transmissive PBR rendering needs (refraction / attenuation depend
on how much glass the light travels through). Glass has no yield point (it
fractures), so ``yield_strength_pa`` is unset and ``safety_factor_to_yield``
returns None; practical tensile strength is flaw/surface dependent and quite low.

    from bd_materials import glass
    from bd_materials.glass import Glass

    glass.glass(thickness_mm=5)                    # soda-lime, 5 mm
    glass.glass(Glass.SODA_LIME, thickness_mm=8)
    glass.all()                                    # base instances (thickness unset)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .base import IsotropicSolidMaterial


@dataclass(frozen=True)
class GlassMaterial(IsotropicSolidMaterial):
    category: str = "glass"
    thickness_mm: float | None = None  # pane thickness for transmissive PBR


class Glass(Enum):
    SODA_LIME = auto()


_GLASS = {
    Glass.SODA_LIME: GlassMaterial(
        name="Glass",
        family="glass",
        grade="soda-lime",
        source="typical",
        density_kg_m3=2500.0,
        youngs_modulus_pa=70e9,
        poissons_ratio=0.22,
        ultimate_tensile_strength_pa=50e6,  # flaw-limited; compressive is far higher
        thermal_expansion_per_k=9e-6,
        thermal_conductivity_w_mk=1.0,
        specific_heat_j_kgk=840.0,
        continuous_service_temp_c=500.0,
    ),
}


def glass(variant: Glass = Glass.SODA_LIME, *, thickness_mm: float) -> GlassMaterial:
    return _GLASS[variant].with_overrides(thickness_mm=thickness_mm)


_ALL = tuple(_GLASS.values())


def all() -> tuple[GlassMaterial, ...]:
    """Every curated glass instance (for tooling / the self-check)."""
    return _ALL


__all__ = ["GlassMaterial", "glass", "Glass", "all"]

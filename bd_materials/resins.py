"""Photopolymer resins (SLA / DLP), as vendor-neutral material families.

Rather than tracking individual vendor products, resins are grouped into neutral
functional families, each accessed by a function. Values are typical figures
aggregated across the vendor datasheets in that family (PCBWay scrape + typical
photopolymer nu / rho / cp / k). ``condition="post-cured"`` since datasheet
values are for post-heat-cured parts. Resins are ``PlasticMaterial`` instances
(``category="resin"``) and, like other plastics, accept ``color=``.

    from bd_materials import resins
    resins.tough(color="blue")
    resins.all()
"""

from __future__ import annotations

from .plastics import PlasticMaterial, _colored

_STANDARD = PlasticMaterial(
    name="Standard Photopolymer Resin",
    family="standard_photopolymer",
    category="resin",
    condition="post-cured",
    source="typical",
    density_kg_m3=1150.0,
    youngs_modulus_pa=2.8e9,
    poissons_ratio=0.40,
    ultimate_tensile_strength_pa=52e6,
    flexural_modulus_pa=2.4e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1500.0,
    heat_deflection_temp_c=58.0,
    shore_hardness="83D",
)
_TOUGH = PlasticMaterial(
    name="Tough (ABS-like) Resin",
    family="tough_abs_like",
    category="resin",
    condition="post-cured",
    source="typical",
    density_kg_m3=1150.0,
    youngs_modulus_pa=2.4e9,
    poissons_ratio=0.42,
    ultimate_tensile_strength_pa=46e6,
    flexural_modulus_pa=2.3e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1500.0,
    heat_deflection_temp_c=52.0,
    shore_hardness="81D",
)
_HIGH_TEMP = PlasticMaterial(
    name="High-Temp Resin",
    family="high_temp",
    category="resin",
    condition="post-cured",
    source="typical",
    density_kg_m3=1300.0,
    youngs_modulus_pa=3.2e9,
    poissons_ratio=0.40,
    ultimate_tensile_strength_pa=47e6,
    flexural_modulus_pa=3.2e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1500.0,
    heat_deflection_temp_c=120.0,
    continuous_service_temp_c=110.0,
    shore_hardness="83D",
)
_CERAMIC = PlasticMaterial(
    name="Ceramic-like (High-Stiffness) Resin",
    family="ceramic_like_high_stiffness",
    category="resin",
    condition="post-cured",
    source="typical",
    density_kg_m3=1650.0,
    youngs_modulus_pa=10.0e9,
    poissons_ratio=0.32,
    ultimate_tensile_strength_pa=68e6,
    flexural_modulus_pa=10.0e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1200.0,
    heat_deflection_temp_c=250.0,
    continuous_service_temp_c=200.0,
    shore_hardness="92D",
)
_CASTABLE = PlasticMaterial(
    name="Castable Resin",
    family="castable",
    category="resin",
    condition="post-cured",
    source="typical",
    density_kg_m3=1150.0,
    youngs_modulus_pa=2.6e9,
    poissons_ratio=0.40,
    ultimate_tensile_strength_pa=42e6,
    flexural_modulus_pa=2.7e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1500.0,
    heat_deflection_temp_c=55.0,
    shore_hardness="80D",
)
_ESD = PlasticMaterial(
    name="ESD-Safe Resin",
    family="esd_safe",
    category="resin",
    condition="post-cured",
    source="typical",
    density_kg_m3=1300.0,
    youngs_modulus_pa=1.9e9,
    poissons_ratio=0.40,
    ultimate_tensile_strength_pa=44e6,
    flexural_modulus_pa=1.84e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1500.0,
    heat_deflection_temp_c=62.0,
    shore_hardness="90D",
)
_TRANSPARENT = PlasticMaterial(
    name="Transparent Resin",
    family="transparent_clear",
    category="resin",
    condition="post-cured",
    source="typical",
    density_kg_m3=1300.0,
    youngs_modulus_pa=1.9e9,
    poissons_ratio=0.40,
    ultimate_tensile_strength_pa=42e6,
    flexural_modulus_pa=1.74e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1500.0,
    heat_deflection_temp_c=52.0,
    shore_hardness="84D",
)


def standard(*, color: str) -> PlasticMaterial:
    return _colored(_STANDARD, color)


def tough(*, color: str) -> PlasticMaterial:
    return _colored(_TOUGH, color)


def high_temp(*, color: str) -> PlasticMaterial:
    return _colored(_HIGH_TEMP, color)


def ceramic(*, color: str) -> PlasticMaterial:
    return _colored(_CERAMIC, color)


def castable(*, color: str) -> PlasticMaterial:
    return _colored(_CASTABLE, color)


def esd(*, color: str) -> PlasticMaterial:
    return _colored(_ESD, color)


def transparent(*, color: str) -> PlasticMaterial:
    return _colored(_TRANSPARENT, color)


_ALL = (_STANDARD, _TOUGH, _HIGH_TEMP, _CERAMIC, _CASTABLE, _ESD, _TRANSPARENT)


def all() -> tuple[PlasticMaterial, ...]:
    """Every curated resin instance (for tooling / the self-check)."""
    return _ALL


__all__ = [
    "standard",
    "tough",
    "high_temp",
    "ceramic",
    "castable",
    "esd",
    "transparent",
    "all",
]

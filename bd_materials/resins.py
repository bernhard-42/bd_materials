"""Photopolymer resins (SLA / DLP), as vendor-neutral material families.

Rather than tracking individual vendor products, resins are grouped into neutral
functional families. Each entry carries typical values aggregated across the
vendor datasheets that fall into that family (PCBWay scrape + typical
photopolymer nu / rho / cp / k). ``condition="post-cured"`` since datasheet
values are for post-heat-cured parts.
"""

from __future__ import annotations

from .base import _reg
from .plastics import PlasticMaterial

# neutral resin families (usable with REGISTRY.filter(family=...))
STANDARD = "standard_photopolymer"
TOUGH_ABS = "tough_abs_like"
HIGH_TEMP = "high_temp"
CERAMIC = "ceramic_like_high_stiffness"
CASTABLE = "castable"
ESD = "esd_safe"
TRANSPARENT = "transparent_clear"


STANDARD_RESIN = _reg(
    PlasticMaterial(
        name="Standard Photopolymer Resin",
        family=STANDARD,
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
)
TOUGH_RESIN = _reg(
    PlasticMaterial(
        name="Tough (ABS-like) Resin",
        family=TOUGH_ABS,
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
)
HIGH_TEMP_RESIN = _reg(
    PlasticMaterial(
        name="High-Temp Resin",
        family=HIGH_TEMP,
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
)
CERAMIC_RESIN = _reg(
    PlasticMaterial(
        name="Ceramic-like (High-Stiffness) Resin",
        family=CERAMIC,
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
)
CASTABLE_RESIN = _reg(
    PlasticMaterial(
        name="Castable Resin",
        family=CASTABLE,
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
)
ESD_RESIN = _reg(
    PlasticMaterial(
        name="ESD-Safe Resin",
        family=ESD,
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
)
TRANSPARENT_RESIN = _reg(
    PlasticMaterial(
        name="Transparent Resin",
        family=TRANSPARENT,
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
)


__all__ = [
    # family constants
    "STANDARD",
    "TOUGH_ABS",
    "HIGH_TEMP",
    "CERAMIC",
    "CASTABLE",
    "ESD",
    "TRANSPARENT",
    # instances
    "STANDARD_RESIN",
    "TOUGH_RESIN",
    "HIGH_TEMP_RESIN",
    "CERAMIC_RESIN",
    "CASTABLE_RESIN",
    "ESD_RESIN",
    "TRANSPARENT_RESIN",
]

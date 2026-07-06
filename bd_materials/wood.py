"""Wood materials (orthotropic).

Wood does NOT use the isotropic elastic model: stiffness/strength along the grain
far exceed across-grain, so it extends ``Material`` directly (no
``effective_shear_modulus_pa`` / yield safety factors, which would be wrong here).
``youngs_modulus_parallel_pa`` is along the grain; strength is quoted as modulus
of rupture (bending) since wood has no true yield point. Values are typical for
~12% moisture content and shift substantially when wet. Engineered boards
(MDF/OSB) are ~isotropic in-plane, so their perpendicular modulus ~ parallel.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import Material, _reg


@dataclass(frozen=True)
class WoodMaterial(Material):
    category: str = "wood"
    # typical-wood defaults (override per species where they differ)
    thermal_conductivity_w_mk: float | None = 0.15
    specific_heat_j_kgk: float | None = 1700.0
    moisture_content_percent: float | None = 12.0
    source: str | None = "typical"
    # grain-direction mechanics
    youngs_modulus_parallel_pa: float | None = None  # along grain (longitudinal)
    youngs_modulus_perp_pa: float | None = None  # across grain (radial/tangential)
    modulus_of_rupture_pa: float | None = None  # bending strength (no true yield)
    compressive_strength_parallel_pa: float | None = None
    janka_hardness_n: float | None = None


ASH = _reg(
    WoodMaterial(
        name="Ash",
        family="wood",
        grade="white ash",
        density_kg_m3=670.0,
        youngs_modulus_parallel_pa=12.0e9,
        youngs_modulus_perp_pa=0.8e9,
        modulus_of_rupture_pa=103e6,
        compressive_strength_parallel_pa=51e6,
        janka_hardness_n=5870.0,
    )
)
BEECH = _reg(
    WoodMaterial(
        name="Beech",
        family="wood",
        grade="American beech",
        density_kg_m3=720.0,
        youngs_modulus_parallel_pa=11.9e9,
        youngs_modulus_perp_pa=0.75e9,
        modulus_of_rupture_pa=103e6,
        compressive_strength_parallel_pa=50e6,
        janka_hardness_n=5800.0,
    )
)
BIRCH = _reg(
    WoodMaterial(
        name="Birch",
        family="wood",
        grade="yellow birch",
        density_kg_m3=660.0,
        youngs_modulus_parallel_pa=13.9e9,
        youngs_modulus_perp_pa=0.9e9,
        modulus_of_rupture_pa=114e6,
        compressive_strength_parallel_pa=56e6,
        janka_hardness_n=5600.0,
    )
)
MAPLE = _reg(
    WoodMaterial(
        name="Maple",
        family="wood",
        grade="hard/sugar maple",
        density_kg_m3=705.0,
        youngs_modulus_parallel_pa=12.6e9,
        youngs_modulus_perp_pa=0.8e9,
        modulus_of_rupture_pa=109e6,
        compressive_strength_parallel_pa=54e6,
        janka_hardness_n=6450.0,
    )
)
OAK = _reg(
    WoodMaterial(
        name="Oak",
        family="wood",
        grade="white oak",
        density_kg_m3=755.0,
        youngs_modulus_parallel_pa=12.3e9,
        youngs_modulus_perp_pa=0.8e9,
        modulus_of_rupture_pa=105e6,
        compressive_strength_parallel_pa=51e6,
        janka_hardness_n=6000.0,
    )
)
WALNUT = _reg(
    WoodMaterial(
        name="Walnut",
        family="wood",
        grade="black walnut",
        density_kg_m3=610.0,
        youngs_modulus_parallel_pa=11.6e9,
        youngs_modulus_perp_pa=0.7e9,
        modulus_of_rupture_pa=101e6,
        compressive_strength_parallel_pa=52e6,
        janka_hardness_n=4490.0,
    )
)
SPRUCE = _reg(
    WoodMaterial(
        name="Spruce",
        family="wood",
        grade="Sitka spruce (softwood)",
        density_kg_m3=430.0,
        youngs_modulus_parallel_pa=10.5e9,
        youngs_modulus_perp_pa=0.42e9,
        modulus_of_rupture_pa=70e6,
        compressive_strength_parallel_pa=38e6,
        janka_hardness_n=2270.0,
    )
)
MDF = _reg(
    WoodMaterial(
        name="MDF",
        family="engineered_wood",
        grade="medium-density fibreboard",
        density_kg_m3=750.0,
        thermal_conductivity_w_mk=0.12,
        moisture_content_percent=6.0,
        youngs_modulus_parallel_pa=3.6e9,
        youngs_modulus_perp_pa=3.6e9,  # ~isotropic
        modulus_of_rupture_pa=35e6,
        compressive_strength_parallel_pa=15e6,
    )
)
OSB = _reg(
    WoodMaterial(
        name="OSB",
        family="engineered_wood",
        grade="oriented strand board",
        density_kg_m3=640.0,
        thermal_conductivity_w_mk=0.13,
        moisture_content_percent=6.0,
        youngs_modulus_parallel_pa=5.5e9,
        youngs_modulus_perp_pa=1.5e9,
        modulus_of_rupture_pa=28e6,
        compressive_strength_parallel_pa=15e6,
    )
)


__all__ = [
    "WoodMaterial",
    "ASH",
    "BEECH",
    "BIRCH",
    "MAPLE",
    "OAK",
    "WALNUT",
    "SPRUCE",
    "MDF",
    "OSB",
]

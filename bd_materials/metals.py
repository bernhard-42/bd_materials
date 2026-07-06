"""Metal materials.

Named by grade + temper (``ALU_6061_T6``), never by manufacturing process.
PCBWay strength values backfilled with typical reference (MatWeb-class)
E / nu / G / rho / cp / k. ``condition`` is the heat-treat / temper state and
``hardness`` a self-describing string (e.g. "60 HRC", "197 HB"). Each entry is
one common variant -- clone with ``.with_overrides(...)`` for a different
temper/grade.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import IsotropicSolidMaterial, _reg


@dataclass(frozen=True)
class MetalMaterial(IsotropicSolidMaterial):
    category: str = "metal"
    fatigue_strength_pa: float | None = None
    hardness: str | None = None

    def fatigue_safety_factor(self, alternating_stress_pa: float) -> float | None:
        if self.fatigue_strength_pa is None or alternating_stress_pa <= 0:
            return None
        return self.fatigue_strength_pa / alternating_stress_pa


# ===========================================================================
# Aluminum
# ===========================================================================
ALU_6061_T6 = _reg(
    MetalMaterial(
        name="Aluminum 6061-T6",
        family="aluminum",
        grade="6061",
        condition="T6",
        hardness="95 HB",
        source="curated + PCBWay + MatWeb",
        density_kg_m3=2700.0,
        youngs_modulus_pa=68.9e9,
        poissons_ratio=0.33,
        shear_modulus_pa=26e9,
        yield_strength_pa=276e6,
        ultimate_tensile_strength_pa=310e6,
        fatigue_strength_pa=96.5e6,
        thermal_expansion_per_k=23.6e-6,
        thermal_conductivity_w_mk=167.0,
        specific_heat_j_kgk=896.0,
    )
)
ALU_7075_T6 = _reg(
    MetalMaterial(
        name="Aluminum 7075-T6",
        family="aluminum",
        grade="7075",
        condition="T6",
        hardness="150 HB",
        source="PCBWay + MatWeb",
        density_kg_m3=2820.0,
        youngs_modulus_pa=71.7e9,
        poissons_ratio=0.33,
        shear_modulus_pa=26.9e9,
        yield_strength_pa=503e6,
        ultimate_tensile_strength_pa=572e6,
        fatigue_strength_pa=159e6,
        thermal_expansion_per_k=23.6e-6,
        thermal_conductivity_w_mk=130.0,
        specific_heat_j_kgk=960.0,
    )
)
ALU_5052_H32 = _reg(
    MetalMaterial(
        name="Aluminum 5052-H32",
        family="aluminum",
        grade="5052",
        condition="H32",
        hardness="60 HB",
        source="PCBWay + MatWeb",
        density_kg_m3=2680.0,
        youngs_modulus_pa=70.3e9,
        poissons_ratio=0.33,
        shear_modulus_pa=25.9e9,
        yield_strength_pa=193e6,
        ultimate_tensile_strength_pa=228e6,
        thermal_expansion_per_k=23.8e-6,
        thermal_conductivity_w_mk=138.0,
        specific_heat_j_kgk=880.0,
    )
)
ALU_2A12 = _reg(
    MetalMaterial(
        name="Aluminum 2A12",
        family="aluminum",
        grade="2A12",
        condition="T4",
        hardness="120 HB",
        source="PCBWay + MatWeb",
        density_kg_m3=2800.0,
        youngs_modulus_pa=68e9,
        poissons_ratio=0.33,
        yield_strength_pa=205e6,
        ultimate_tensile_strength_pa=470e6,
        fatigue_strength_pa=105e6,
        thermal_conductivity_w_mk=121.0,
        specific_heat_j_kgk=875.0,
    )
)
ALU_ALSI10MG = _reg(
    MetalMaterial(
        name="Aluminum AlSi10Mg",
        family="aluminum",
        grade="AlSi10Mg",
        condition="as-built",
        hardness="120 HB",
        source="PCBWay + MatWeb",
        density_kg_m3=2670.0,
        youngs_modulus_pa=70e9,
        poissons_ratio=0.33,
        ultimate_tensile_strength_pa=330e6,
        thermal_conductivity_w_mk=130.0,
        specific_heat_j_kgk=900.0,
    )
)


# ===========================================================================
# Stainless steel
# ===========================================================================
STAINLESS_304 = _reg(
    MetalMaterial(
        name="Stainless Steel 304",
        family="stainless",
        grade="304",
        condition="annealed",
        hardness="70 HRB",
        source="curated + PCBWay + MatWeb",
        density_kg_m3=7930.0,
        youngs_modulus_pa=193e9,
        poissons_ratio=0.29,
        yield_strength_pa=205e6,
        ultimate_tensile_strength_pa=515e6,
        thermal_expansion_per_k=17.2e-6,
        thermal_conductivity_w_mk=16.2,
        specific_heat_j_kgk=500.0,
        continuous_service_temp_c=925.0,
    )
)
STAINLESS_316L = _reg(
    MetalMaterial(
        name="Stainless Steel 316/316L",
        family="stainless",
        grade="316/316L",
        condition="annealed",
        hardness="79 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=8000.0,
        youngs_modulus_pa=205e9,
        poissons_ratio=0.29,
        yield_strength_pa=310e6,
        ultimate_tensile_strength_pa=620e6,
        thermal_conductivity_w_mk=16.3,
        specific_heat_j_kgk=500.0,
        continuous_service_temp_c=925.0,
    )
)
STAINLESS_316L_AS_BUILT = _reg(
    MetalMaterial(
        name="Stainless Steel 316L (as-built)",
        family="stainless",
        grade="316L",
        condition="as-built",
        source="PCBWay + MatWeb",
        density_kg_m3=7990.0,
        youngs_modulus_pa=190e9,
        poissons_ratio=0.29,
        ultimate_tensile_strength_pa=560e6,
        thermal_conductivity_w_mk=15.0,
        specific_heat_j_kgk=500.0,
    )
)
STAINLESS_303 = _reg(
    MetalMaterial(
        name="Stainless Steel 303",
        family="stainless",
        grade="303",
        condition="annealed",
        hardness="76 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=8030.0,
        youngs_modulus_pa=193e9,
        poissons_ratio=0.29,
        yield_strength_pa=276e6,
        ultimate_tensile_strength_pa=621e6,
        thermal_expansion_per_k=17.3e-6,
        thermal_conductivity_w_mk=16.3,
        specific_heat_j_kgk=500.0,
    )
)
STAINLESS_430 = _reg(
    MetalMaterial(
        name="Stainless Steel 430",
        family="stainless",
        grade="430",
        condition="annealed",
        hardness="88 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=7750.0,
        youngs_modulus_pa=200e9,
        poissons_ratio=0.28,
        yield_strength_pa=483e6,
        ultimate_tensile_strength_pa=586e6,
        thermal_conductivity_w_mk=26.3,
        specific_heat_j_kgk=460.0,
        continuous_service_temp_c=870.0,
    )
)
STAINLESS_201 = _reg(
    MetalMaterial(
        name="Stainless Steel 201",
        family="stainless",
        grade="201",
        condition="annealed",
        hardness="90 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=7860.0,
        youngs_modulus_pa=197e9,
        poissons_ratio=0.29,
        yield_strength_pa=292e6,
        ultimate_tensile_strength_pa=685e6,
        thermal_conductivity_w_mk=16.0,
        specific_heat_j_kgk=500.0,
    )
)


# ===========================================================================
# Brass / copper
# ===========================================================================
BRASS_C360 = _reg(
    MetalMaterial(
        name="Brass C360",
        family="brass",
        grade="C360",
        condition="half-hard",
        hardness="78 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=8500.0,
        youngs_modulus_pa=97e9,
        poissons_ratio=0.34,
        ultimate_tensile_strength_pa=140e6,
        thermal_conductivity_w_mk=29.0,
        specific_heat_j_kgk=380.0,
    )
)
COPPER_C110 = _reg(
    MetalMaterial(
        name="Copper C110",
        family="copper",
        grade="C110",
        condition="annealed",
        source="PCBWay + MatWeb",
        density_kg_m3=8960.0,
        youngs_modulus_pa=117e9,
        poissons_ratio=0.34,
        thermal_conductivity_w_mk=391.0,
        specific_heat_j_kgk=420.0,
    )
)


# ===========================================================================
# Titanium
# ===========================================================================
TITANIUM_6AL_4V = _reg(
    MetalMaterial(
        name="Titanium Ti-6Al-4V (Gr5/TC4)",
        family="titanium",
        grade="Gr5",
        condition="annealed",
        hardness="334 HB",
        source="PCBWay + MatWeb",
        density_kg_m3=4470.0,
        youngs_modulus_pa=113.8e9,
        poissons_ratio=0.34,
        yield_strength_pa=880e6,
        ultimate_tensile_strength_pa=950e6,
        thermal_conductivity_w_mk=6.7,
        specific_heat_j_kgk=526.0,
    )
)
TITANIUM_6AL_4V_AS_BUILT = _reg(
    MetalMaterial(
        name="Titanium Ti-6Al-4V (as-built)",
        family="titanium",
        grade="TC4",
        condition="as-built",
        hardness="349 HB",
        source="PCBWay + MatWeb",
        density_kg_m3=4430.0,
        youngs_modulus_pa=110e9,
        poissons_ratio=0.34,
        ultimate_tensile_strength_pa=600e6,
        thermal_conductivity_w_mk=7.0,
        specific_heat_j_kgk=526.0,
    )
)


# ===========================================================================
# Carbon / mild / alloy steel
# ===========================================================================
STEEL_1018 = _reg(
    MetalMaterial(
        name="Steel 1018",
        family="mild_steel",
        grade="1018",
        condition="cold-drawn",
        hardness="76 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=7870.0,
        youngs_modulus_pa=205e9,
        poissons_ratio=0.29,
        shear_modulus_pa=80e9,
        yield_strength_pa=400e6,
        ultimate_tensile_strength_pa=440e6,
        thermal_conductivity_w_mk=51.9,
        specific_heat_j_kgk=486.0,
    )
)
STEEL_1045 = _reg(
    MetalMaterial(
        name="Steel 1045",
        family="mild_steel",
        grade="1045",
        condition="cold-drawn",
        hardness="84 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=7870.0,
        youngs_modulus_pa=200e9,
        poissons_ratio=0.29,
        shear_modulus_pa=80e9,
        yield_strength_pa=580e6,
        ultimate_tensile_strength_pa=680e6,
        thermal_conductivity_w_mk=49.8,
        specific_heat_j_kgk=486.0,
    )
)
STEEL_A36 = _reg(
    MetalMaterial(
        name="Steel A36",
        family="mild_steel",
        grade="A36",
        condition="hot-rolled",
        hardness="92 HRB",
        source="PCBWay + MatWeb",
        density_kg_m3=7850.0,
        youngs_modulus_pa=200e9,
        poissons_ratio=0.26,
        shear_modulus_pa=79.3e9,
        yield_strength_pa=290e6,
        ultimate_tensile_strength_pa=550e6,
        thermal_conductivity_w_mk=51.9,
        specific_heat_j_kgk=486.0,
    )
)
STEEL_4140 = _reg(
    MetalMaterial(
        name="Steel 4140",
        family="alloy_steel",
        grade="4140",
        condition="quenched & tempered",
        hardness="28-32 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7850.0,
        youngs_modulus_pa=210e9,
        poissons_ratio=0.29,
        shear_modulus_pa=80e9,
        yield_strength_pa=715e6,
        ultimate_tensile_strength_pa=1130e6,
        thermal_conductivity_w_mk=42.6,
        specific_heat_j_kgk=473.0,
    )
)
STEEL_4340 = _reg(
    MetalMaterial(
        name="Steel 4340",
        family="alloy_steel",
        grade="4340",
        condition="quenched & tempered",
        hardness="24-53 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7850.0,
        youngs_modulus_pa=213e9,
        poissons_ratio=0.29,
        shear_modulus_pa=80e9,
        yield_strength_pa=525e6,
        ultimate_tensile_strength_pa=820e6,
        thermal_conductivity_w_mk=44.5,
        specific_heat_j_kgk=475.0,
    )
)
STEEL_1215 = _reg(
    MetalMaterial(
        name="Steel 1215",
        family="alloy_steel",
        grade="1215",
        condition="cold-drawn",
        hardness="167 HB",
        source="PCBWay + MatWeb",
        density_kg_m3=7870.0,
        youngs_modulus_pa=210e9,
        poissons_ratio=0.29,
        shear_modulus_pa=80e9,
        yield_strength_pa=415e6,
        ultimate_tensile_strength_pa=540e6,
        thermal_conductivity_w_mk=51.9,
        specific_heat_j_kgk=486.0,
    )
)


# ===========================================================================
# Tool / spring steel
# ===========================================================================
TOOL_STEEL_D2 = _reg(
    MetalMaterial(
        name="Tool Steel D2",
        family="tool_steel",
        grade="D2",
        condition="hardened",
        hardness="58-62 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7695.0,
        youngs_modulus_pa=215e9,
        poissons_ratio=0.30,
        yield_strength_pa=2290e6,
        ultimate_tensile_strength_pa=2500e6,
        thermal_conductivity_w_mk=20.0,
        specific_heat_j_kgk=460.0,
        continuous_service_temp_c=245.0,
    )
)
TOOL_STEEL_A2 = _reg(
    MetalMaterial(
        name="Tool Steel A2",
        family="tool_steel",
        grade="A2",
        condition="hardened",
        hardness="57-62 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7861.0,
        youngs_modulus_pa=219e9,
        poissons_ratio=0.30,
        yield_strength_pa=2140e6,
        ultimate_tensile_strength_pa=2360e6,
        thermal_conductivity_w_mk=24.0,
        specific_heat_j_kgk=460.0,
        continuous_service_temp_c=245.0,
    )
)
TOOL_STEEL_O1 = _reg(
    MetalMaterial(
        name="Tool Steel O1",
        family="tool_steel",
        grade="O1",
        condition="hardened",
        hardness="57-62 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7833.0,
        youngs_modulus_pa=219e9,
        poissons_ratio=0.30,
        yield_strength_pa=2140e6,
        ultimate_tensile_strength_pa=2360e6,
        thermal_conductivity_w_mk=45.0,
        specific_heat_j_kgk=460.0,
        continuous_service_temp_c=215.0,
    )
)
TOOL_STEEL_A3 = _reg(
    MetalMaterial(
        name="Tool Steel A3",
        family="tool_steel",
        grade="A3",
        condition="hardened",
        hardness="58-62 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7860.0,
        youngs_modulus_pa=203e9,
        poissons_ratio=0.30,
        yield_strength_pa=2100e6,
        ultimate_tensile_strength_pa=2380e6,
        thermal_conductivity_w_mk=37.0,
        specific_heat_j_kgk=460.0,
    )
)
TOOL_STEEL_S7 = _reg(
    MetalMaterial(
        name="Tool Steel S7",
        family="tool_steel",
        grade="S7",
        condition="hardened",
        hardness="54-56 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7833.0,
        youngs_modulus_pa=215e9,
        poissons_ratio=0.30,
        yield_strength_pa=2050e6,
        ultimate_tensile_strength_pa=2200e6,
        thermal_conductivity_w_mk=44.0,
        specific_heat_j_kgk=460.0,
        continuous_service_temp_c=215.0,
    )
)
TOOL_STEEL_H13 = _reg(
    MetalMaterial(
        name="Tool Steel H13",
        family="tool_steel",
        grade="H13",
        condition="hardened",
        hardness="44-52 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7800.0,
        youngs_modulus_pa=215e9,
        poissons_ratio=0.30,
        yield_strength_pa=1380e6,
        ultimate_tensile_strength_pa=1590e6,
        thermal_conductivity_w_mk=25.5,
        specific_heat_j_kgk=460.0,
    )
)
TOOL_STEEL_AS_BUILT = _reg(
    MetalMaterial(
        name="Tool Steel (as-built)",
        family="tool_steel",
        grade="generic",
        condition="as-built",
        source="PCBWay + MatWeb",
        density_kg_m3=7800.0,
        youngs_modulus_pa=190e9,
        poissons_ratio=0.30,
        ultimate_tensile_strength_pa=1090e6,
        thermal_conductivity_w_mk=20.0,
        specific_heat_j_kgk=460.0,
    )
)
SPRING_STEEL = _reg(
    MetalMaterial(
        name="Spring Steel",
        family="spring_steel",
        grade="generic",
        condition="quenched & tempered",
        hardness="30-50 HRC",
        source="PCBWay + MatWeb",
        density_kg_m3=7800.0,
        youngs_modulus_pa=207e9,
        poissons_ratio=0.29,
        yield_strength_pa=785e6,
        ultimate_tensile_strength_pa=980e6,
        thermal_conductivity_w_mk=25.5,
        specific_heat_j_kgk=480.0,
    )
)


__all__ = [
    "MetalMaterial",
    # aluminum
    "ALU_6061_T6",
    "ALU_7075_T6",
    "ALU_5052_H32",
    "ALU_2A12",
    "ALU_ALSI10MG",
    # stainless
    "STAINLESS_304",
    "STAINLESS_316L",
    "STAINLESS_316L_AS_BUILT",
    "STAINLESS_303",
    "STAINLESS_430",
    "STAINLESS_201",
    # brass / copper
    "BRASS_C360",
    "COPPER_C110",
    # titanium
    "TITANIUM_6AL_4V",
    "TITANIUM_6AL_4V_AS_BUILT",
    # carbon / mild / alloy steel
    "STEEL_1018",
    "STEEL_1045",
    "STEEL_A36",
    "STEEL_4140",
    "STEEL_4340",
    "STEEL_1215",
    # tool / spring steel
    "TOOL_STEEL_D2",
    "TOOL_STEEL_A2",
    "TOOL_STEEL_O1",
    "TOOL_STEEL_A3",
    "TOOL_STEEL_S7",
    "TOOL_STEEL_H13",
    "TOOL_STEEL_AS_BUILT",
    "SPRING_STEEL",
]

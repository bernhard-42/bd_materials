"""Metal materials, accessed by family functions (not by constant name).

Identity (grade + condition) lives only in each material's fields, never in a
Python name. Each family is a dict keyed by its variant enum (``Alu.G6061_T6``);
the function just returns ``_FAMILY[variant]``, defaulting to the common one
(``aluminum()`` -> 6061-T6). Because the enum member *is* the key, the selector
and the data are written together and an invalid combination (6061 + hardened)
is simply unrepresentable. Families follow the source (PCBWay) taxonomy: mild
and alloy steel stay distinct. Every family is modelled the same way regardless
of how many grades it currently holds -- a one-grade family (brass, copper,
spring steel) still has an enum and a default, so adding a grade later is just a
new member, not a signature change.

    from bd_materials import metals
    from bd_materials.metals import Alu, Stainless

    metals.aluminum()                       # 6061-T6 (default)
    metals.aluminum(Alu.G7075_T6)           # 7075-T6
    metals.stainless(Stainless.G316L_AS_BUILT)
    metals.brass()                          # Brass.C360_HALF_HARD (default)
    metals.all()                            # every metal instance
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .base import IsotropicSolidMaterial


@dataclass(frozen=True)
class MetalMaterial(IsotropicSolidMaterial):
    category: str = "metal"
    fatigue_strength_pa: float | None = None
    hardness: str | None = None

    def fatigue_safety_factor(self, alternating_stress_pa: float) -> float | None:
        """Safety factor against fatigue, ``SF = fatigue_strength / S_alt``.

        Margin against failure under cyclic loading: the alternating stress
        amplitude is compared to the material's fatigue (endurance) strength,
        with SF > 1 meaning the part should survive indefinitely. The stored
        ``fatigue_strength_pa`` is a nominal endurance figure with no defined
        cycle count or R-ratio, so treat this as a screening indicator, not a
        certified fatigue-life prediction.

        Args:
            alternating_stress_pa: Alternating stress amplitude in Pa (half the
                peak-to-peak stress range). Must be > 0.

        Returns:
            Dimensionless fatigue safety factor, or ``None`` if
            ``fatigue_strength_pa`` is unset or ``alternating_stress_pa <= 0``.
        """
        if self.fatigue_strength_pa is None or alternating_stress_pa <= 0:
            return None
        return self.fatigue_strength_pa / alternating_stress_pa


# ===========================================================================
# Aluminum
# ===========================================================================
class Alu(Enum):
    G6061_T6 = auto()
    G7075_T6 = auto()
    G5052_H32 = auto()
    G2A12_T4 = auto()
    ALSI10MG_AS_BUILT = auto()


_ALUMINUM = {
    Alu.G6061_T6: MetalMaterial(
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
    ),
    Alu.G7075_T6: MetalMaterial(
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
    ),
    Alu.G5052_H32: MetalMaterial(
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
    ),
    Alu.G2A12_T4: MetalMaterial(
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
    ),
    Alu.ALSI10MG_AS_BUILT: MetalMaterial(
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
    ),
}


def aluminum(variant: Alu = Alu.G6061_T6) -> MetalMaterial:
    return _ALUMINUM[variant]


# ===========================================================================
# Stainless steel
# ===========================================================================
class Stainless(Enum):
    G304_ANNEALED = auto()
    G316L_ANNEALED = auto()
    G316L_AS_BUILT = auto()
    G303_ANNEALED = auto()
    G430_ANNEALED = auto()
    G201_ANNEALED = auto()


_STAINLESS = {
    Stainless.G304_ANNEALED: MetalMaterial(
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
    ),
    Stainless.G316L_ANNEALED: MetalMaterial(
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
    ),
    Stainless.G316L_AS_BUILT: MetalMaterial(
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
    ),
    Stainless.G303_ANNEALED: MetalMaterial(
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
    ),
    Stainless.G430_ANNEALED: MetalMaterial(
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
    ),
    Stainless.G201_ANNEALED: MetalMaterial(
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
    ),
}


def stainless(variant: Stainless = Stainless.G304_ANNEALED) -> MetalMaterial:
    return _STAINLESS[variant]


# ===========================================================================
# Mild / carbon steel
# ===========================================================================
class MildSteel(Enum):
    G1018_COLD_DRAWN = auto()
    G1045_COLD_DRAWN = auto()
    GA36_HOT_ROLLED = auto()


_MILD_STEEL = {
    MildSteel.G1018_COLD_DRAWN: MetalMaterial(
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
    ),
    MildSteel.G1045_COLD_DRAWN: MetalMaterial(
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
    ),
    MildSteel.GA36_HOT_ROLLED: MetalMaterial(
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
    ),
}


def mild_steel(variant: MildSteel = MildSteel.G1018_COLD_DRAWN) -> MetalMaterial:
    return _MILD_STEEL[variant]


# ===========================================================================
# Alloy steel
# ===========================================================================
class AlloySteel(Enum):
    G4140_QUENCHED_TEMPERED = auto()
    G4340_QUENCHED_TEMPERED = auto()
    G1215_COLD_DRAWN = auto()


_ALLOY_STEEL = {
    AlloySteel.G4140_QUENCHED_TEMPERED: MetalMaterial(
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
    ),
    AlloySteel.G4340_QUENCHED_TEMPERED: MetalMaterial(
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
    ),
    AlloySteel.G1215_COLD_DRAWN: MetalMaterial(
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
    ),
}


def alloy_steel(
    variant: AlloySteel = AlloySteel.G4140_QUENCHED_TEMPERED,
) -> MetalMaterial:
    return _ALLOY_STEEL[variant]


# ===========================================================================
# Tool steel
# ===========================================================================
class ToolSteel(Enum):
    D2_HARDENED = auto()
    A2_HARDENED = auto()
    O1_HARDENED = auto()
    A3_HARDENED = auto()
    S7_HARDENED = auto()
    H13_HARDENED = auto()
    GENERIC_AS_BUILT = auto()


_TOOL_STEEL = {
    ToolSteel.D2_HARDENED: MetalMaterial(
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
    ),
    ToolSteel.A2_HARDENED: MetalMaterial(
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
    ),
    ToolSteel.O1_HARDENED: MetalMaterial(
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
    ),
    ToolSteel.A3_HARDENED: MetalMaterial(
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
    ),
    ToolSteel.S7_HARDENED: MetalMaterial(
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
    ),
    ToolSteel.H13_HARDENED: MetalMaterial(
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
    ),
    ToolSteel.GENERIC_AS_BUILT: MetalMaterial(
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
    ),
}


def tool_steel(variant: ToolSteel = ToolSteel.A2_HARDENED) -> MetalMaterial:
    return _TOOL_STEEL[variant]


# ===========================================================================
# Titanium
# ===========================================================================
class Titanium(Enum):
    GR5_ANNEALED = auto()
    TC4_AS_BUILT = auto()


_TITANIUM = {
    Titanium.GR5_ANNEALED: MetalMaterial(
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
    ),
    Titanium.TC4_AS_BUILT: MetalMaterial(
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
    ),
}


def titanium(variant: Titanium = Titanium.GR5_ANNEALED) -> MetalMaterial:
    return _TITANIUM[variant]


# ===========================================================================
# Spring steel
# ===========================================================================
class SpringSteel(Enum):
    GENERIC_QUENCHED_TEMPERED = auto()


_SPRING_STEEL = {
    SpringSteel.GENERIC_QUENCHED_TEMPERED: MetalMaterial(
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
    ),
}


def spring_steel(
    variant: SpringSteel = SpringSteel.GENERIC_QUENCHED_TEMPERED,
) -> MetalMaterial:
    return _SPRING_STEEL[variant]


# ===========================================================================
# Brass
# ===========================================================================
class Brass(Enum):
    C360_HALF_HARD = auto()


_BRASS = {
    Brass.C360_HALF_HARD: MetalMaterial(
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
    ),
}


def brass(variant: Brass = Brass.C360_HALF_HARD) -> MetalMaterial:
    return _BRASS[variant]


# ===========================================================================
# Copper
# ===========================================================================
class Copper(Enum):
    C110_ANNEALED = auto()


_COPPER = {
    Copper.C110_ANNEALED: MetalMaterial(
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
    ),
}


def copper(variant: Copper = Copper.C110_ANNEALED) -> MetalMaterial:
    return _COPPER[variant]


# ===========================================================================
_ALL = (
    *_ALUMINUM.values(),
    *_STAINLESS.values(),
    *_MILD_STEEL.values(),
    *_ALLOY_STEEL.values(),
    *_TOOL_STEEL.values(),
    *_SPRING_STEEL.values(),
    *_TITANIUM.values(),
    *_BRASS.values(),
    *_COPPER.values(),
)


def all() -> tuple[MetalMaterial, ...]:
    """Every curated metal instance (for tooling / the self-check)."""
    return _ALL


__all__ = [
    "MetalMaterial",
    "aluminum",
    "stainless",
    "mild_steel",
    "alloy_steel",
    "tool_steel",
    "spring_steel",
    "titanium",
    "brass",
    "copper",
    "all",
    "Alu",
    "Stainless",
    "MildSteel",
    "AlloySteel",
    "ToolSteel",
    "SpringSteel",
    "Titanium",
    "Brass",
    "Copper",
]

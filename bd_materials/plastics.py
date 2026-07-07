"""Plastic materials -- thermoplastics and fibre-reinforced composites.

Accessed by family functions, never by constant name. Multi-variant families are
a dict keyed by a variant enum (``PLA.CARBON_FILLED``) with a function returning
``_FAMILY[variant]``; single-variant families are just a function. Composites are
the same ``PlasticMaterial`` with ``category="composite"``, kept beside their base
polymer (``pla(PLA.CARBON_FILLED)``). Resins (``category="resin"``) live in
``resins``. Anisotropic prints use the stronger in-plane value as the typical.

Colour. Plastics are the one material class that comes in colours (filaments,
pigmented resins), so ``PlasticMaterial`` carries a ``color`` and every function
*requires* a keyword ``color=``: ``pla(color="red")`` returns a red-tinted clone.
A ``FinishedMaterial`` finish still overrides it at use time. Transmissive
plastics (acrylic ``pmma``, polycarbonate ``pc``) additionally *require*
``thickness_mm=`` -- like glass, their refraction depends on the pane thickness.

    from bd_materials import plastics
    from bd_materials.plastics import PLA, Nylon

    plastics.pla(color="red")                     # red PLA filament
    plastics.pla(PLA.CARBON_FILLED, color="black")
    plastics.nylon(Nylon.G12, color="natural")
    plastics.pp(color="white")                    # single variant -> no enum
    plastics.pmma(color="clear", thickness_mm=3)  # transmissive -> needs thickness
    plastics.all()                                # every plastic instance (uncoloured)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .base import IsotropicSolidMaterial


@dataclass(frozen=True)
class PlasticMaterial(IsotropicSolidMaterial):
    category: str = "plastic"
    flexural_modulus_pa: float | None = None
    heat_deflection_temp_c: float | None = None
    shore_hardness: str | None = None
    color: str | None = None  # plastics come in colours (filament / pigment)
    thickness_mm: float | None = None  # transmissive plastics: pane thickness for PBR

    def is_hdt_ok(self, temp_c: float) -> bool | None:
        """Whether a temperature is within the heat-deflection limit.

        A screening check against ``heat_deflection_temp_c``, the temperature
        at which the plastic deflects a standard amount under a standard
        bending load. It marks where a polymer begins to soften and lose
        stiffness -- a load-dependent index, not a hard maximum-use temperature
        (compare ``is_service_temp_ok`` for the continuous-use limit).

        Args:
            temp_c: Operating temperature in degrees Celsius.

        Returns:
            ``True`` if ``temp_c`` is at or below the HDT, ``False`` if above,
            or ``None`` if ``heat_deflection_temp_c`` is unset.
        """
        if self.heat_deflection_temp_c is None:
            return None
        return temp_c <= self.heat_deflection_temp_c


def _colored(material: PlasticMaterial, color: str) -> PlasticMaterial:
    """Return a colour-tinted clone of the material."""
    return material.with_overrides(color=color)


def _transmissive(
    material: PlasticMaterial, color: str, thickness_mm: float
) -> PlasticMaterial:
    """Clone with colour + render thickness (for transmissive plastics)."""
    return material.with_overrides(color=color, thickness_mm=thickness_mm)


# ===========================================================================
# PLA (+ carbon-filled composite)
# ===========================================================================
class PLA(Enum):
    GENERIC = auto()
    CARBON_FILLED = auto()


_PLA = {
    PLA.GENERIC: PlasticMaterial(
        name="PLA",
        family="PLA",
        grade="generic",
        source="curated + PCBWay + MatWeb",
        density_kg_m3=1240.0,
        youngs_modulus_pa=3.5e9,
        poissons_ratio=0.36,
        yield_strength_pa=45e6,
        continuous_service_temp_c=50.0,
        thermal_expansion_per_k=68e-6,
        thermal_conductivity_w_mk=0.13,
        specific_heat_j_kgk=1800.0,
        heat_deflection_temp_c=55.0,
    ),
    PLA.CARBON_FILLED: PlasticMaterial(
        name="PLA-CF",
        family="PLA",
        grade="carbon-filled",
        category="composite",
        source="curated + PCBWay + MatWeb",
        density_kg_m3=1250.0,
        youngs_modulus_pa=5.5e9,
        poissons_ratio=0.34,
        yield_strength_pa=55e6,
        continuous_service_temp_c=55.0,
        thermal_expansion_per_k=35e-6,
        thermal_conductivity_w_mk=0.20,
        specific_heat_j_kgk=1600.0,
        heat_deflection_temp_c=60.0,
    ),
}


def pla(variant: PLA = PLA.GENERIC, *, color: str) -> PlasticMaterial:
    return _colored(_PLA[variant], color)


# ===========================================================================
# ABS
# ===========================================================================
class ABS(Enum):
    GENERIC = auto()
    FLAME_RETARDANT = auto()
    ESD7 = auto()


_ABS = {
    ABS.GENERIC: PlasticMaterial(
        name="ABS",
        family="ABS",
        grade="generic",
        source="PCBWay + MatWeb",
        density_kg_m3=1050.0,
        youngs_modulus_pa=2.3e9,
        poissons_ratio=0.35,
        ultimate_tensile_strength_pa=28.3e6,
        flexural_modulus_pa=2.096e9,
        thermal_expansion_per_k=100.8e-6,
        thermal_conductivity_w_mk=0.17,
        specific_heat_j_kgk=1400.0,
        heat_deflection_temp_c=80.6,
        continuous_service_temp_c=71.1,
    ),
    ABS.FLAME_RETARDANT: PlasticMaterial(
        name="ABS Flame Retardant",
        family="ABS",
        grade="flame_retardant",
        source="PCBWay + MatWeb",
        density_kg_m3=1200.0,
        youngs_modulus_pa=2.3e9,
        poissons_ratio=0.35,
        ultimate_tensile_strength_pa=37.9e6,
        flexural_modulus_pa=2.275e9,
        thermal_expansion_per_k=100.8e-6,
        thermal_conductivity_w_mk=0.17,
        specific_heat_j_kgk=1400.0,
        heat_deflection_temp_c=87.8,
        continuous_service_temp_c=72.2,
    ),
    ABS.ESD7: PlasticMaterial(
        name="Stratasys ABS-ESD7",
        family="ABS",
        grade="ESD7",
        source="PCBWay + MatWeb",
        density_kg_m3=1300.0,
        youngs_modulus_pa=2.4e9,
        poissons_ratio=0.35,
        ultimate_tensile_strength_pa=36e6,
        flexural_modulus_pa=2.4e9,
        thermal_conductivity_w_mk=0.17,
        specific_heat_j_kgk=1400.0,
        heat_deflection_temp_c=82.0,
    ),
}


def abs_(variant: ABS = ABS.GENERIC, *, color: str) -> PlasticMaterial:
    """ABS thermoplastic (``abs_`` -- trailing underscore avoids the builtin)."""
    return _colored(_ABS[variant], color)


# ===========================================================================
# Nylon (PA) -- includes SLS/HP printed variants + glass-filled composite
# ===========================================================================
class Nylon(Enum):
    G6 = auto()
    G12 = auto()
    G12_SINTERED = auto()
    G12_HP = auto()
    G12_GF35 = auto()


_NYLON = {
    Nylon.G6: PlasticMaterial(
        name="Nylon 6",
        family="PA",
        grade="6",
        condition="dry as molded",
        source="curated + PCBWay + MatWeb",
        density_kg_m3=1140.0,
        youngs_modulus_pa=3.2e9,
        poissons_ratio=0.39,
        yield_strength_pa=80e6,
        ultimate_tensile_strength_pa=79.1e6,
        continuous_service_temp_c=100.0,
        thermal_expansion_per_k=90e-6,
        thermal_conductivity_w_mk=0.30,
        specific_heat_j_kgk=1700.0,
        heat_deflection_temp_c=75.0,
    ),
    Nylon.G12: PlasticMaterial(
        name="Nylon 12",
        family="PA",
        grade="12",
        condition="dry as molded",
        source="PCBWay + MatWeb",
        density_kg_m3=1010.0,
        youngs_modulus_pa=2.9e9,
        poissons_ratio=0.40,
        ultimate_tensile_strength_pa=31e6,
        thermal_conductivity_w_mk=0.25,
        specific_heat_j_kgk=1700.0,
        heat_deflection_temp_c=113.0,
    ),
    Nylon.G12_SINTERED: PlasticMaterial(
        name="PA12 (sintered)",
        family="PA",
        grade="12",
        source="PCBWay + MatWeb",
        density_kg_m3=1010.0,
        youngs_modulus_pa=1.9e9,
        poissons_ratio=0.40,
        ultimate_tensile_strength_pa=47e6,
        thermal_conductivity_w_mk=0.25,
        specific_heat_j_kgk=1700.0,
        heat_deflection_temp_c=150.0,
    ),
    Nylon.G12_HP: PlasticMaterial(
        name="HP-PA-12",
        family="PA",
        grade="12",
        source="PCBWay + MatWeb",
        density_kg_m3=1010.0,
        youngs_modulus_pa=1.8e9,
        poissons_ratio=0.40,
        ultimate_tensile_strength_pa=48e6,
        flexural_modulus_pa=1.73e9,
        thermal_conductivity_w_mk=0.25,
        specific_heat_j_kgk=1700.0,
        heat_deflection_temp_c=95.0,
    ),
    Nylon.G12_GF35: PlasticMaterial(
        name="Glass Fiber Nylon (PA12+35% GF)",
        family="PA",
        grade="12-GF35",
        category="composite",
        source="PCBWay + MatWeb",
        density_kg_m3=1300.0,
        youngs_modulus_pa=2.6e9,
        poissons_ratio=0.40,
        ultimate_tensile_strength_pa=45e6,
        thermal_conductivity_w_mk=0.3,
        specific_heat_j_kgk=1300.0,
        heat_deflection_temp_c=153.0,
    ),
}


def nylon(variant: Nylon = Nylon.G12, *, color: str) -> PlasticMaterial:
    return _colored(_NYLON[variant], color)


# ===========================================================================
# PEEK -- molded + printed
# ===========================================================================
class PEEK(Enum):
    MOLDED = auto()
    PRINTED = auto()


_PEEK = {
    PEEK.MOLDED: PlasticMaterial(
        name="PEEK",
        family="PEEK",
        grade="generic",
        source="PCBWay + MatWeb",
        density_kg_m3=1300.0,
        youngs_modulus_pa=3.95e9,
        poissons_ratio=0.38,
        yield_strength_pa=95e6,
        ultimate_tensile_strength_pa=103e6,
        thermal_expansion_per_k=60e-6,
        thermal_conductivity_w_mk=0.26,
        specific_heat_j_kgk=1340.0,
        continuous_service_temp_c=260.0,
    ),
    PEEK.PRINTED: PlasticMaterial(
        name="PEEK (printed)",
        family="PEEK",
        grade="generic",
        source="PCBWay + MatWeb",
        density_kg_m3=1300.0,
        youngs_modulus_pa=3.95e9,
        poissons_ratio=0.38,
        yield_strength_pa=100e6,
        ultimate_tensile_strength_pa=118e6,
        thermal_expansion_per_k=60e-6,
        thermal_conductivity_w_mk=0.26,
        specific_heat_j_kgk=1340.0,
        continuous_service_temp_c=163.0,
    ),
}


def peek(variant: PEEK = PEEK.MOLDED, *, color: str) -> PlasticMaterial:
    return _colored(_PEEK[variant], color)


# ===========================================================================
# TPU -- cast/extruded + sintered
# ===========================================================================
class TPU(Enum):
    SHORE_95A = auto()
    SINTERED = auto()


_TPU = {
    TPU.SHORE_95A: PlasticMaterial(
        name="TPU",
        family="TPU",
        grade="95A",
        source="curated + PCBWay + MatWeb",
        density_kg_m3=1200.0,
        youngs_modulus_pa=0.12e9,
        poissons_ratio=0.47,
        yield_strength_pa=25e6,
        continuous_service_temp_c=80.0,
        thermal_expansion_per_k=150e-6,
        thermal_conductivity_w_mk=0.20,
        specific_heat_j_kgk=1800.0,
        shore_hardness="95A",
    ),
    TPU.SINTERED: PlasticMaterial(
        name="TPU (sintered)",
        family="TPU",
        grade="88-90A",
        source="PCBWay + MatWeb",
        density_kg_m3=1400.0,
        poissons_ratio=0.45,
        ultimate_tensile_strength_pa=20e6,
        thermal_conductivity_w_mk=0.2,
        specific_heat_j_kgk=1800.0,
        shore_hardness="88-90A",
    ),
}


def tpu(variant: TPU = TPU.SHORE_95A, *, color: str) -> PlasticMaterial:
    return _colored(_TPU[variant], color)


# ===========================================================================
# Single-variant thermoplastics
# ===========================================================================
_PC = PlasticMaterial(
    name="Polycarbonate (PC)",
    family="PC",
    grade="generic",
    source="PCBWay + MatWeb",
    density_kg_m3=1200.0,
    youngs_modulus_pa=2.44e9,
    poissons_ratio=0.37,
    yield_strength_pa=70e6,
    ultimate_tensile_strength_pa=72.4e6,
    thermal_expansion_per_k=137e-6,
    thermal_conductivity_w_mk=0.218,
    specific_heat_j_kgk=1200.0,
    continuous_service_temp_c=144.0,
)
_PP = PlasticMaterial(
    name="Polypropylene (PP)",
    family="PP",
    grade="generic",
    source="PCBWay + MatWeb",
    density_kg_m3=905.0,
    youngs_modulus_pa=1.6e9,
    poissons_ratio=0.42,
    yield_strength_pa=32e6,
    ultimate_tensile_strength_pa=33e6,
    thermal_expansion_per_k=17e-6,
    thermal_conductivity_w_mk=0.27,
    specific_heat_j_kgk=1920.0,
    continuous_service_temp_c=130.0,
)
_POM = PlasticMaterial(
    name="POM",
    family="POM",
    grade="generic",
    source="PCBWay + MatWeb",
    density_kg_m3=1410.0,
    youngs_modulus_pa=4.0e9,
    poissons_ratio=0.35,
    yield_strength_pa=72.4e6,
    ultimate_tensile_strength_pa=89.6e6,
    thermal_expansion_per_k=202e-6,
    thermal_conductivity_w_mk=0.35,
    specific_heat_j_kgk=1470.0,
    continuous_service_temp_c=96.9,
)
_PTFE = PlasticMaterial(
    name="PTFE (Teflon)",
    family="PTFE",
    grade="generic",
    source="PCBWay + MatWeb",
    density_kg_m3=2200.0,
    youngs_modulus_pa=2.25e9,
    poissons_ratio=0.46,
    yield_strength_pa=41.4e6,
    ultimate_tensile_strength_pa=31e6,
    thermal_expansion_per_k=200e-6,
    thermal_conductivity_w_mk=0.25,
    specific_heat_j_kgk=1010.0,
    continuous_service_temp_c=270.0,
    shore_hardness="65D",
)
_PMMA = PlasticMaterial(
    name="PMMA (Acrylic)",
    family="PMMA",
    grade="generic",
    source="PCBWay + MatWeb",
    density_kg_m3=1180.0,
    youngs_modulus_pa=3.3e9,
    poissons_ratio=0.37,
    yield_strength_pa=80e6,
    ultimate_tensile_strength_pa=83e6,
    thermal_expansion_per_k=90e-6,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1470.0,
    continuous_service_temp_c=80.0,
)
_PE = PlasticMaterial(
    name="Polyethylene (PE)",
    family="PE",
    grade="generic",
    source="PCBWay + MatWeb",
    density_kg_m3=960.0,
    youngs_modulus_pa=1.09e9,
    poissons_ratio=0.42,
    yield_strength_pa=31e6,
    ultimate_tensile_strength_pa=31e6,
    thermal_expansion_per_k=198e-6,
    thermal_conductivity_w_mk=0.502,
    specific_heat_j_kgk=1900.0,
    continuous_service_temp_c=129.0,
)
_BAKELITE = PlasticMaterial(
    name="Bakelite",
    family="phenolic",
    grade="Bakelite",
    source="PCBWay + MatWeb",
    density_kg_m3=1300.0,
    youngs_modulus_pa=7e9,
    poissons_ratio=0.35,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=920.0,
)
_RUBBER = PlasticMaterial(
    name="Rubber",
    family="rubber",
    grade="generic",
    source="PCBWay + MatWeb",
    density_kg_m3=1200.0,
    poissons_ratio=0.49,
    specific_heat_j_kgk=2000.0,
    yield_strength_pa=145e6,
    ultimate_tensile_strength_pa=165e6,
)


def pc(*, color: str, thickness_mm: float) -> PlasticMaterial:
    """Polycarbonate -- optically clear, so it needs a render thickness."""
    return _transmissive(_PC, color, thickness_mm)


def pp(*, color: str) -> PlasticMaterial:
    return _colored(_PP, color)


def pom(*, color: str) -> PlasticMaterial:
    return _colored(_POM, color)


def ptfe(*, color: str) -> PlasticMaterial:
    return _colored(_PTFE, color)


def pmma(*, color: str, thickness_mm: float) -> PlasticMaterial:
    """PMMA / acrylic -- transmissive, so it needs a render thickness."""
    return _transmissive(_PMMA, color, thickness_mm)


def pe(*, color: str) -> PlasticMaterial:
    return _colored(_PE, color)


def bakelite(*, color: str) -> PlasticMaterial:
    return _colored(_BAKELITE, color)


def rubber(*, color: str) -> PlasticMaterial:
    return _colored(_RUBBER, color)


# ===========================================================================
# Composites with no base polymer elsewhere in the library
# ===========================================================================
_PETG_CF = PlasticMaterial(
    name="PETG-CF",
    family="PETG",
    grade="carbon-filled",
    category="composite",
    source="PCBWay + MatWeb",
    density_kg_m3=1250.0,
    youngs_modulus_pa=2.46e9,
    poissons_ratio=0.40,
    ultimate_tensile_strength_pa=35e6,
    flexural_modulus_pa=2.91e9,
    thermal_conductivity_w_mk=0.2,
    specific_heat_j_kgk=1200.0,
)
_PPS_CF = PlasticMaterial(
    name="PPS CF",
    family="PPS",
    grade="carbon-filled",
    category="composite",
    source="PCBWay + MatWeb",
    density_kg_m3=1260.0,
    youngs_modulus_pa=8.23e9,
    poissons_ratio=0.38,
    ultimate_tensile_strength_pa=87e6,
    flexural_modulus_pa=7.16e9,
    thermal_conductivity_w_mk=0.3,
    specific_heat_j_kgk=1090.0,
)
_FR4 = PlasticMaterial(
    name="FR4",
    family="FR4",
    grade="generic",
    category="composite",
    source="PCBWay + MatWeb",
    density_kg_m3=1850.0,
    youngs_modulus_pa=24e9,
    poissons_ratio=0.13,
    ultimate_tensile_strength_pa=415e6,
    thermal_conductivity_w_mk=0.3,
    specific_heat_j_kgk=600.0,
    continuous_service_temp_c=140.0,
)
_CARBON_FIBER_PLATE = PlasticMaterial(
    name="Carbon Fiber Plate",
    family="CFRP",
    grade="plate",
    category="composite",
    source="PCBWay + MatWeb",
    density_kg_m3=1600.0,
    youngs_modulus_pa=200e9,
    poissons_ratio=0.30,
    ultimate_tensile_strength_pa=3000e6,
    thermal_conductivity_w_mk=10.0,
    specific_heat_j_kgk=800.0,
    continuous_service_temp_c=121.0,
)


def petg_cf(*, color: str) -> PlasticMaterial:
    return _colored(_PETG_CF, color)


def pps_cf(*, color: str) -> PlasticMaterial:
    return _colored(_PPS_CF, color)


def fr4(*, color: str) -> PlasticMaterial:
    return _colored(_FR4, color)


def carbon_fiber_plate(*, color: str) -> PlasticMaterial:
    return _colored(_CARBON_FIBER_PLATE, color)


# ===========================================================================
_ALL = (
    *_PLA.values(),
    *_ABS.values(),
    *_NYLON.values(),
    *_PEEK.values(),
    *_TPU.values(),
    _PC,
    _PP,
    _POM,
    _PTFE,
    _PMMA,
    _PE,
    _BAKELITE,
    _RUBBER,
    _PETG_CF,
    _PPS_CF,
    _FR4,
    _CARBON_FIBER_PLATE,
)


def all() -> tuple[PlasticMaterial, ...]:
    """Every curated plastic instance (for tooling / the self-check)."""
    return _ALL


__all__ = [
    "PlasticMaterial",
    # multi-variant families (function + enum)
    "pla",
    "abs_",
    "nylon",
    "peek",
    "tpu",
    "PLA",
    "ABS",
    "Nylon",
    "PEEK",
    "TPU",
    # single-variant families
    "pc",
    "pp",
    "pom",
    "ptfe",
    "pmma",
    "pe",
    "bakelite",
    "rubber",
    # composites
    "petg_cf",
    "pps_cf",
    "fr4",
    "carbon_fiber_plate",
    "all",
]

"""Plastic materials -- thermoplastics and fibre-reinforced composites.

Named by material/grade, never by manufacturing process. ``PlasticMaterial`` is
the base type; composites are the same type with ``category="composite"`` and
are kept here beside their base polymer (``PLA_CF`` next to ``PLA``), so related
grades stay together. Resins (``category="resin"``) are genuinely distinct
materials and live in ``resins``. Anisotropic prints use the stronger in-plane value as the typical figure.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import IsotropicSolidMaterial, _reg


@dataclass(frozen=True)
class PlasticMaterial(IsotropicSolidMaterial):
    category: str = "plastic"
    flexural_modulus_pa: float | None = None
    heat_deflection_temp_c: float | None = None
    shore_hardness: str | None = None

    def is_hdt_ok(self, temp_c: float) -> bool | None:
        if self.heat_deflection_temp_c is None:
            return None
        return temp_c <= self.heat_deflection_temp_c


PLA = _reg(
    PlasticMaterial(
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
    )
)
PLA_CF = _reg(
    PlasticMaterial(
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
    )
)
ABS = _reg(
    PlasticMaterial(
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
    )
)
ABS_FR = _reg(
    PlasticMaterial(
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
    )
)
ABS_ESD7 = _reg(
    PlasticMaterial(
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
    )
)
PC = _reg(
    PlasticMaterial(
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
)
NYLON_6 = _reg(
    PlasticMaterial(
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
    )
)
NYLON_12 = _reg(
    PlasticMaterial(
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
    )
)
PA12_SINTERED = _reg(
    PlasticMaterial(
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
    )
)
HP_PA12 = _reg(
    PlasticMaterial(
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
    )
)
GLASS_FIBER_NYLON = _reg(
    PlasticMaterial(
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
    )
)
PP = _reg(
    PlasticMaterial(
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
)
POM = _reg(
    PlasticMaterial(
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
)
PTFE = _reg(
    PlasticMaterial(
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
)
PMMA = _reg(
    PlasticMaterial(
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
)
PE = _reg(
    PlasticMaterial(
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
)
PEEK = _reg(
    PlasticMaterial(
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
    )
)
PEEK_PRINTED = _reg(
    PlasticMaterial(
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
    )
)
TPU = _reg(
    PlasticMaterial(
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
    )
)
TPU_SINTERED = _reg(
    PlasticMaterial(
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
    )
)
BAKELITE = _reg(
    PlasticMaterial(
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
)
RUBBER = _reg(
    PlasticMaterial(
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
)


# ---------------------------------------------------------------------------
# Composites with no base polymer elsewhere in the library
# (PLA_CF lives next to PLA; GLASS_FIBER_NYLON next to the nylons)
# ---------------------------------------------------------------------------
PETG_CF = _reg(
    PlasticMaterial(
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
)
PPS_CF = _reg(
    PlasticMaterial(
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
)
FR4 = _reg(
    PlasticMaterial(
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
)
CARBON_FIBER_PLATE = _reg(
    PlasticMaterial(
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
)


__all__ = [
    "PlasticMaterial",
    # thermoplastics
    "PLA",
    "ABS",
    "ABS_FR",
    "ABS_ESD7",
    "PC",
    "NYLON_6",
    "NYLON_12",
    "PA12_SINTERED",
    "HP_PA12",
    "PP",
    "POM",
    "PTFE",
    "PMMA",
    "PE",
    "PEEK",
    "PEEK_PRINTED",
    "TPU",
    "TPU_SINTERED",
    "BAKELITE",
    "RUBBER",
    # composites (category="composite")
    "PLA_CF",
    "GLASS_FIBER_NYLON",
    "PETG_CF",
    "PPS_CF",
    "FR4",
    "CARBON_FIBER_PLATE",
]

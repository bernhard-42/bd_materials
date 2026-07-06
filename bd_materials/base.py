"""Base material types and registry.

Purpose: quickly *provide or compute* physical characteristics (mass, stiffness,
stress safety factors, thermal response) for a designed build123d part -- not to
be an exhaustive datasheet archive. Every field feeds a calculation or identifies
the material; datasheet trivia is omitted (it lives in the source scrapes).

Units are SI (Pa, kg/m3, K, W/mK, J/kgK); ``*_c`` fields are degrees Celsius.
Scalar values are **room-temperature nominal unless noted** -- e.g. thermal
expansion is a single representative coefficient, not a temperature curve --
so treat them with care in hot designs. ``continuous_service_temp_c`` is a
continuous-use limit, distinct from heat-deflection / softening / melting (which
are not modelled). Fatigue values (``fatigue_strength_pa``) are nominal
endurance figures without a defined cycle count / R-ratio.

Type hierarchy
--------------
* ``Material``               -- universal: identity, density, mass, thermal.
* ``IsotropicSolidMaterial`` -- adds isotropic linear-elastic mechanics (E, nu, G,
                                yield, UTS) and only makes sense for isotropic
                                solids. Parents ``MetalMaterial`` (``metals``),
                                ``PlasticMaterial`` (``plastics``), and glass.
* ``ArealMaterial``          -- thin planar goods sized by grammage, not volume.
                                Parents ``PaperMaterial`` (``paper``) and
                                ``TextileMaterial`` (``textile``: fabric/felt/leather).
* ``WoodMaterial`` (``wood``)   -- orthotropic; its own grain-direction mechanics.

Wood and areal materials extend ``Material`` directly (not the isotropic solid),
so they never inherit methods like ``effective_shear_modulus_pa`` that would be
meaningless or actively wrong for them.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal, get_args

Category = Literal[
    "generic",
    "metal",
    "plastic",
    "resin",
    "composite",
    "wood",
    "glass",
    "paper",
    "textile",
]
ALLOWED_CATEGORIES = frozenset(get_args(Category))


# ---------------------------------------------------------------------------
# Universal base
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Material:
    name: str
    category: Category = "generic"
    density_kg_m3: float | None = None
    thermal_expansion_per_k: float | None = None
    thermal_conductivity_w_mk: float | None = None
    specific_heat_j_kgk: float | None = None
    continuous_service_temp_c: float | None = None  # continuous-use limit
    # identity
    family: str | None = None
    grade: str | None = None
    condition: str | None = None  # heat-treat / temper / cure state, e.g. "T6"
    source: str | None = None

    def __post_init__(self) -> None:
        if self.category not in ALLOWED_CATEGORIES:
            raise ValueError(f"unknown material category: {self.category!r}")

    def with_overrides(self, **kwargs) -> "Material":
        return replace(self, **kwargs)

    @property
    def density_g_cm3(self) -> float | None:
        return None if self.density_kg_m3 is None else self.density_kg_m3 / 1000.0

    def mass_from_volume_m3(self, volume_m3: float) -> float | None:
        if self.density_kg_m3 is None:
            return None
        return self.density_kg_m3 * volume_m3

    def mass_g_from_volume_mm3(self, volume_mm3: float) -> float | None:
        """Convenience for build123d: part volume in mm3 -> mass in grams."""
        if self.density_kg_m3 is None:
            return None
        return self.density_kg_m3 * (volume_mm3 * 1e-9) * 1000.0

    def thermal_strain(self, delta_t_k: float) -> float | None:
        if self.thermal_expansion_per_k is None:
            return None
        return self.thermal_expansion_per_k * delta_t_k

    def heat_energy_for_temperature_rise(
        self, volume_m3: float, delta_t_k: float
    ) -> float | None:
        mass = self.mass_from_volume_m3(volume_m3)
        if mass is None or self.specific_heat_j_kgk is None:
            return None
        return mass * self.specific_heat_j_kgk * delta_t_k

    def thermal_resistance_1d(self, length_m: float, area_m2: float) -> float | None:
        if self.thermal_conductivity_w_mk is None or area_m2 <= 0:
            return None
        return length_m / (self.thermal_conductivity_w_mk * area_m2)

    def is_service_temp_ok(self, temp_c: float) -> bool | None:
        if self.continuous_service_temp_c is None:
            return None
        return temp_c <= self.continuous_service_temp_c

    # --- derived comparison metrics (None if inputs missing) ---
    @property
    def volumetric_heat_capacity_j_m3k(self) -> float | None:
        """rho * cp -- energy to raise 1 m3 by 1 K (J/(m3.K))."""
        if self.density_kg_m3 is None or self.specific_heat_j_kgk is None:
            return None
        return self.density_kg_m3 * self.specific_heat_j_kgk

    @property
    def thermal_diffusivity_m2_s(self) -> float | None:
        """k / (rho * cp) -- how fast temperature diffuses (m2/s)."""
        vhc = self.volumetric_heat_capacity_j_m3k
        if self.thermal_conductivity_w_mk is None or not vhc:
            return None
        return self.thermal_conductivity_w_mk / vhc


# ---------------------------------------------------------------------------
# Isotropic linear-elastic solids (metals, plastics, glass, ...)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class IsotropicSolidMaterial(Material):
    youngs_modulus_pa: float | None = None
    poissons_ratio: float | None = None
    shear_modulus_pa: float | None = None  # measured; else derived from E, nu
    yield_strength_pa: float | None = None
    ultimate_tensile_strength_pa: float | None = None

    def effective_shear_modulus_pa(self) -> float | None:
        """Measured shear modulus if set, else derived from E and nu (isotropic)."""
        if self.shear_modulus_pa is not None:
            return self.shear_modulus_pa
        if self.youngs_modulus_pa is not None and self.poissons_ratio is not None:
            return self.youngs_modulus_pa / (2 * (1 + self.poissons_ratio))
        return None

    def safety_factor_to_yield(self, stress_pa: float) -> float | None:
        if self.yield_strength_pa is None or stress_pa <= 0:
            return None
        return self.yield_strength_pa / stress_pa

    def safety_factor_to_ultimate(self, stress_pa: float) -> float | None:
        if self.ultimate_tensile_strength_pa is None or stress_pa <= 0:
            return None
        return self.ultimate_tensile_strength_pa / stress_pa

    # --- Hooke's law (uniaxial) ---
    def strain_from_stress(self, stress_pa: float) -> float | None:
        """Elastic strain = stress / E."""
        if self.youngs_modulus_pa is None:
            return None
        return stress_pa / self.youngs_modulus_pa

    def stress_from_strain(self, strain: float) -> float | None:
        """Elastic stress = E * strain."""
        if self.youngs_modulus_pa is None:
            return None
        return self.youngs_modulus_pa * strain

    # --- specific (per-density) comparison metrics, m2/s2 (== J/kg) ---
    @property
    def specific_stiffness(self) -> float | None:
        """E / rho -- specific modulus."""
        if self.youngs_modulus_pa is None or not self.density_kg_m3:
            return None
        return self.youngs_modulus_pa / self.density_kg_m3

    @property
    def specific_strength_yield(self) -> float | None:
        """yield / rho."""
        if self.yield_strength_pa is None or not self.density_kg_m3:
            return None
        return self.yield_strength_pa / self.density_kg_m3

    @property
    def specific_strength_uts(self) -> float | None:
        """UTS / rho."""
        if self.ultimate_tensile_strength_pa is None or not self.density_kg_m3:
            return None
        return self.ultimate_tensile_strength_pa / self.density_kg_m3


# ---------------------------------------------------------------------------
# Areal (per-unit-area) planar goods: paper, textiles
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ArealMaterial(Material):
    """Thin planar goods specified by mass-per-area (grammage), not volume.

    Flexible, essentially in-plane only; extends ``Material`` directly (never the
    isotropic solid mechanics). Base for ``PaperMaterial`` and ``TextileMaterial``.
    """

    areal_density_g_m2: float | None = None  # grammage -- primary mass metric
    thickness_mm: float | None = None
    tensile_strength_md_pa: float | None = None  # in-plane, machine direction

    def mass_g_from_area_mm2(self, area_mm2: float) -> float | None:
        """Mass in grams of a flat sheet of the given area (mm2)."""
        if self.areal_density_g_m2 is None:
            return None
        return self.areal_density_g_m2 * (area_mm2 * 1e-6)  # mm2 -> m2


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
def _slug(text: str) -> str:
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


class MaterialRegistry:
    """Central store: register once, look up by key, filter by taxonomy."""

    def __init__(self) -> None:
        self._by_key: dict[str, Material] = {}

    def register(self, material: Material, key: str | None = None) -> Material:
        key = key or self._auto_key(material)
        if key in self._by_key:
            raise KeyError(f"duplicate material key: {key!r}")
        self._by_key[key] = material
        return material

    @staticmethod
    def _auto_key(material: Material) -> str:
        return _slug(material.name)

    def get(self, key: str) -> Material | None:
        return self._by_key.get(key)

    def __getitem__(self, key: str) -> Material:
        return self._by_key[key]

    def __contains__(self, key: str) -> bool:
        return key in self._by_key

    def __len__(self) -> int:
        return len(self._by_key)

    def keys(self) -> list[str]:
        return list(self._by_key)

    def all(self) -> list[Material]:
        return list(self._by_key.values())

    def filter(
        self,
        *,
        category: str | None = None,
        family: str | None = None,
        condition: str | None = None,
    ) -> list[Material]:
        def match(m: Material) -> bool:
            return (
                (category is None or m.category == category)
                and (family is None or m.family == family)
                and (condition is None or m.condition == condition)
            )

        return [m for m in self._by_key.values() if match(m)]

    def families(self) -> set[str]:
        return {m.family for m in self._by_key.values() if m.family}


REGISTRY = MaterialRegistry()


def _reg(material: Material, key: str | None = None) -> Material:
    """Construct-and-register helper so ``NAME = _reg(Material(...))`` also indexes it."""
    return REGISTRY.register(material, key)

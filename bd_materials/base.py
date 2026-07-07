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
from typing import Literal, TypeVar, get_args

# Type-preserving "self" for clone helpers -- py3.10 has no typing.Self, so a
# TypeVar bound to Material lets ``with_overrides`` return the caller's subclass
# (GlassMaterial.with_overrides(...) -> GlassMaterial, not the base Material).
_MaterialT = TypeVar("_MaterialT", bound="Material")

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
        """Validate the taxonomy tag as soon as an instance is built.

        Not a physics calculation -- it guards the ``category`` field so a
        typo (``"metalic"``) fails loudly at construction instead of silently
        breaking later ``REGISTRY.filter(category=...)`` lookups and the PBR
        category dispatch. Runs automatically after the dataclass ``__init__``.

        Raises:
            ValueError: if ``category`` is not one of ``ALLOWED_CATEGORIES``.
        """
        if self.category not in ALLOWED_CATEGORIES:
            raise ValueError(f"unknown material category: {self.category!r}")

    def with_overrides(self: _MaterialT, **kwargs) -> _MaterialT:
        """Clone this material with selected fields changed.

        Every entry in the library is one representative variant; a different
        temper, grade, or condition is expressed as a copy rather than a new
        top-level constant. Because materials are frozen dataclasses this
        delegates to ``dataclasses.replace``, leaving the original untouched
        and keeping the clone immutable.

        Args:
            **kwargs: Field name -> new value, e.g. ``condition="O"`` or
                ``yield_strength_pa=120e6``.

        Returns:
            A new material of the same class with those fields replaced.
        """
        return replace(self, **kwargs)

    @property
    def density_g_cm3(self) -> float | None:
        """Density in g/cm3, the unit materials datasheets usually quote.

        A pure unit conversion of the SI ``density_kg_m3`` (1 g/cm3 = 1000
        kg/m3), offered so a value can be sanity-checked against everyday
        intuition (water ~1, aluminium ~2.7, steel ~7.8) without dividing by
        1000 by hand.

        Returns:
            Density in g/cm3, or ``None`` if ``density_kg_m3`` is unset.
        """
        return None if self.density_kg_m3 is None else self.density_kg_m3 / 1000.0

    def mass_from_volume_m3(self, volume_m3: float) -> float | None:
        """Mass of a part from its volume, via ``m = rho * V``.

        The core mass relation, density times volume. This is the SI-native
        entry point (volume already in cubic metres); for a build123d part,
        whose ``.volume`` is in mm3, use ``mass_g_from_volume_mm3`` instead.

        Args:
            volume_m3: Part volume in cubic metres.

        Returns:
            Mass in kilograms, or ``None`` if ``density_kg_m3`` is unset.
        """
        if self.density_kg_m3 is None:
            return None
        return self.density_kg_m3 * volume_m3

    def mass_g_from_volume_mm3(self, volume_mm3: float) -> float | None:
        """Mass in grams from a build123d part volume in mm3.

        The everyday CAD path: build123d reports a solid's ``.volume`` in
        cubic millimetres, and part masses are most useful in grams. Applies
        ``m = rho * V`` with the unit bridges baked in -- mm3 -> m3 (x1e-9)
        and kg -> g (x1000).

        Args:
            volume_mm3: Part volume in cubic millimetres (e.g. ``part.volume``).

        Returns:
            Mass in grams, or ``None`` if ``density_kg_m3`` is unset.
        """
        if self.density_kg_m3 is None:
            return None
        return self.density_kg_m3 * (volume_mm3 * 1e-9) * 1000.0

    def thermal_strain(self, delta_t_k: float) -> float | None:
        """Free thermal expansion strain, ``epsilon = alpha * dT``.

        The unconstrained (stress-free) fractional length change a part
        undergoes for a temperature swing, using the single representative
        linear expansion coefficient. Use it to predict fit-up / clearance
        changes, or -- multiplied by ``E`` via ``stress_from_strain`` -- the
        thermal stress when the part is fully restrained. Nominal ``alpha``
        only; real expansion is mildly temperature dependent.

        Args:
            delta_t_k: Temperature change in kelvin (a delta is numerically
                identical in degrees Celsius). Positive = heating.

        Returns:
            Dimensionless strain (dL/L), or ``None`` if
            ``thermal_expansion_per_k`` is unset.
        """
        if self.thermal_expansion_per_k is None:
            return None
        return self.thermal_expansion_per_k * delta_t_k

    def heat_energy_for_temperature_rise(
        self, volume_m3: float, delta_t_k: float
    ) -> float | None:
        """Sensible heat to change a part's temperature, ``Q = m * cp * dT``.

        How much energy must be added (or removed) to move a solid part of the
        given volume through a temperature change -- its thermal-mass demand.
        Mass is derived internally from ``volume_m3`` and density, then
        multiplied by specific heat and the temperature swing. Sensible heat
        only: no phase change or latent heat is modelled.

        Args:
            volume_m3: Part volume in cubic metres.
            delta_t_k: Temperature change in kelvin. Positive = heating
                (Q > 0); a negative value returns the heat to remove.

        Returns:
            Energy in joules, or ``None`` if density or ``specific_heat_j_kgk``
            is unset.
        """
        mass = self.mass_from_volume_m3(volume_m3)
        if mass is None or self.specific_heat_j_kgk is None:
            return None
        return mass * self.specific_heat_j_kgk * delta_t_k

    def thermal_resistance_1d(self, length_m: float, area_m2: float) -> float | None:
        """1-D steady-state conductive resistance, ``R = L / (k * A)``.

        The resistance of a uniform slab to heat flowing along its length
        (Fourier conduction through a constant cross-section). Pair it with a
        heat flow to get the temperature drop, ``dT = Q * R``, or sum series
        resistances for a simple stack-up. Steady-state and 1-D only -- no
        convection, contact resistance, or lateral spreading.

        Args:
            length_m: Conduction path length in metres (slab thickness).
            area_m2: Cross-sectional area normal to the flow, in m2. Must
                be > 0.

        Returns:
            Thermal resistance in K/W, or ``None`` if
            ``thermal_conductivity_w_mk`` is unset or ``area_m2 <= 0``.
        """
        if self.thermal_conductivity_w_mk is None or area_m2 <= 0:
            return None
        return length_m / (self.thermal_conductivity_w_mk * area_m2)

    def is_service_temp_ok(self, temp_c: float) -> bool | None:
        """Whether a temperature is within the continuous-use limit.

        A quick screening check against ``continuous_service_temp_c``, the
        temperature the material tolerates in continuous service. It is a
        long-term-use guide, distinct from short-excursion, heat-deflection,
        softening, or melting limits, which are not modelled here.

        Args:
            temp_c: Operating temperature in degrees Celsius.

        Returns:
            ``True`` if ``temp_c`` is at or below the limit, ``False`` if
            above, or ``None`` if ``continuous_service_temp_c`` is unset.
        """
        if self.continuous_service_temp_c is None:
            return None
        return temp_c <= self.continuous_service_temp_c

    # --- derived comparison metrics (None if inputs missing) ---
    @property
    def volumetric_heat_capacity_j_m3k(self) -> float | None:
        """Volumetric heat capacity ``rho * cp`` (J/(m3.K)).

        Energy needed to raise one cubic metre of the material by one kelvin.
        Folding density and specific heat into a per-volume figure makes
        materials directly comparable by the thermal mass of a fixed
        *geometry* (rather than per-kilogram), and it is the denominator of
        the thermal diffusivity below.

        Returns:
            Volumetric heat capacity in J/(m3.K), or ``None`` if density or
            ``specific_heat_j_kgk`` is unset.
        """
        if self.density_kg_m3 is None or self.specific_heat_j_kgk is None:
            return None
        return self.density_kg_m3 * self.specific_heat_j_kgk

    @property
    def thermal_diffusivity_m2_s(self) -> float | None:
        """Thermal diffusivity ``alpha = k / (rho * cp)`` (m2/s).

        How fast a temperature disturbance spreads through the material, as
        opposed to how much energy it stores. High-diffusivity materials
        (metals) reach thermal equilibrium quickly; low ones (plastics, wood)
        lag. It governs transient response -- e.g. the time to heat through a
        thickness ``L`` scales as ``L**2 / alpha`` -- and is computed as
        conductivity over volumetric heat capacity.

        Returns:
            Diffusivity in m2/s, or ``None`` if conductivity is unset or the
            volumetric heat capacity is unavailable/zero.
        """
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
        """Shear modulus G -- measured if given, else derived from E and nu.

        The stiffness relating shear stress to shear strain, needed for
        torsion and transverse-shear calculations. A measured
        ``shear_modulus_pa`` is preferred; when absent it falls back to the
        isotropic elasticity identity ``G = E / (2 * (1 + nu))``, which holds
        only for isotropic linear-elastic solids (which is why this lives here
        and not on ``Material``).

        Returns:
            Shear modulus in Pa, or ``None`` if neither a measured value nor
            both ``youngs_modulus_pa`` and ``poissons_ratio`` are available.
        """
        if self.shear_modulus_pa is not None:
            return self.shear_modulus_pa
        if self.youngs_modulus_pa is not None and self.poissons_ratio is not None:
            return self.youngs_modulus_pa / (2 * (1 + self.poissons_ratio))
        return None

    def safety_factor_to_yield(self, stress_pa: float) -> float | None:
        """Safety factor against yielding, ``SF = yield / applied_stress``.

        How much margin a design has before the onset of permanent (plastic)
        deformation: values > 1 mean the applied stress is below yield, and
        larger is safer. This is the usual acceptance check for ductile metals
        sized to stay elastic.

        Args:
            stress_pa: Applied (von Mises / equivalent) stress in Pa. Must
                be > 0.

        Returns:
            Dimensionless safety factor, or ``None`` if ``yield_strength_pa``
            is unset or ``stress_pa <= 0``.
        """
        if self.yield_strength_pa is None or stress_pa <= 0:
            return None
        return self.yield_strength_pa / stress_pa

    def safety_factor_to_ultimate(self, stress_pa: float) -> float | None:
        """Safety factor against fracture, ``SF = UTS / applied_stress``.

        Margin before ultimate failure (rupture) rather than first yield --
        the relevant check for brittle materials with no meaningful yield
        point, or as a second, larger factor alongside the yield check for
        ductile ones.

        Args:
            stress_pa: Applied stress in Pa. Must be > 0.

        Returns:
            Dimensionless safety factor, or ``None`` if
            ``ultimate_tensile_strength_pa`` is unset or ``stress_pa <= 0``.
        """
        if self.ultimate_tensile_strength_pa is None or stress_pa <= 0:
            return None
        return self.ultimate_tensile_strength_pa / stress_pa

    # --- Hooke's law (uniaxial) ---
    def strain_from_stress(self, stress_pa: float) -> float | None:
        """Elastic strain from stress, Hooke's law ``epsilon = sigma / E``.

        The uniaxial elastic response: the fractional length change produced
        by a given tensile/compressive stress, valid below yield where the
        behaviour is linear. Useful for deflection and interference-fit
        estimates.

        Args:
            stress_pa: Uniaxial stress in Pa (positive in tension).

        Returns:
            Dimensionless strain, or ``None`` if ``youngs_modulus_pa`` is
            unset.
        """
        if self.youngs_modulus_pa is None:
            return None
        return stress_pa / self.youngs_modulus_pa

    def stress_from_strain(self, strain: float) -> float | None:
        """Elastic stress from strain, Hooke's law ``sigma = E * epsilon``.

        The inverse of ``strain_from_stress``: the stress a given elastic
        strain induces. Handy for restrained-thermal-expansion stress (feed it
        ``thermal_strain(dT)``) or press-fit interference, provided the result
        stays below yield.

        Args:
            strain: Dimensionless uniaxial strain (dL/L).

        Returns:
            Stress in Pa, or ``None`` if ``youngs_modulus_pa`` is unset.
        """
        if self.youngs_modulus_pa is None:
            return None
        return self.youngs_modulus_pa * strain

    # --- specific (per-density) comparison metrics, m2/s2 (== J/kg) ---
    @property
    def specific_stiffness(self) -> float | None:
        """Specific modulus ``E / rho`` (m2/s2, i.e. J/kg).

        Stiffness per unit mass -- the figure of merit when choosing a
        material for a lightweight, deflection-limited part. Aluminium, steel,
        and titanium famously have similar specific stiffness, so this exposes
        where an alloy swap actually buys stiffness-per-weight and where it
        does not.

        Returns:
            Specific stiffness in m2/s2, or ``None`` if ``youngs_modulus_pa``
            or density is unset/zero.
        """
        if self.youngs_modulus_pa is None or not self.density_kg_m3:
            return None
        return self.youngs_modulus_pa / self.density_kg_m3

    @property
    def specific_strength_yield(self) -> float | None:
        """Yield specific strength ``yield / rho`` (m2/s2, i.e. J/kg).

        Load capacity per unit mass before permanent deformation -- the
        weight-efficiency metric for strength-limited parts that must stay
        elastic. It lets a heavy strong alloy be compared fairly against a
        light weaker one.

        Returns:
            Specific yield strength in m2/s2, or ``None`` if
            ``yield_strength_pa`` or density is unset/zero.
        """
        if self.yield_strength_pa is None or not self.density_kg_m3:
            return None
        return self.yield_strength_pa / self.density_kg_m3

    @property
    def specific_strength_uts(self) -> float | None:
        """Ultimate specific strength ``UTS / rho`` (m2/s2, i.e. J/kg).

        Load capacity per unit mass before fracture -- the weight-efficiency
        metric at the ultimate limit, and the more meaningful strength ratio
        for materials without a clear yield point.

        Returns:
            Specific ultimate strength in m2/s2, or ``None`` if
            ``ultimate_tensile_strength_pa`` or density is unset/zero.
        """
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
        """Mass in grams of a flat sheet, from grammage x area.

        Thin planar goods (paper, fabric) are specified by mass-per-area
        (grammage, g/m2), not by volume, so a cut sheet's mass is grammage
        times its area. The area is converted mm2 -> m2 (x1e-6) to match the
        g/m2 basis; thickness plays no part.

        Args:
            area_mm2: Flat sheet area in square millimetres (e.g. an A4 face
                is ``210 * 297``).

        Returns:
            Mass in grams, or ``None`` if ``areal_density_g_m2`` is unset.
        """
        if self.areal_density_g_m2 is None:
            return None
        return self.areal_density_g_m2 * (area_mm2 * 1e-6)  # mm2 -> m2


# ---------------------------------------------------------------------------
# Slug helper (used by finishes to key its internal finish table)
# ---------------------------------------------------------------------------
def _slug(text: str) -> str:
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")

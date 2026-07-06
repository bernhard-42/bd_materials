"""Glass -- an isotropic brittle solid.

No new class needed: glass is isotropic linear-elastic, so it is a plain
``IsotropicSolidMaterial`` instance. It has no yield point (it fractures), so
``yield_strength_pa`` is left unset and ``safety_factor_to_yield`` returns None;
its practical tensile strength is flaw/surface dependent and quite low.
"""

from __future__ import annotations

from .base import IsotropicSolidMaterial, _reg

GLASS = _reg(
    IsotropicSolidMaterial(
        name="Glass",
        family="glass",
        grade="soda-lime",
        category="glass",
        source="typical",
        density_kg_m3=2500.0,
        youngs_modulus_pa=70e9,
        poissons_ratio=0.22,
        ultimate_tensile_strength_pa=50e6,  # flaw-limited; compressive is far higher
        thermal_expansion_per_k=9e-6,
        thermal_conductivity_w_mk=1.0,
        specific_heat_j_kgk=840.0,
        continuous_service_temp_c=500.0,
    )
)


__all__ = ["GLASS"]

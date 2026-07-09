"""Shared range primitives and the property-unit table for all range tables.

A material property is a min–max :class:`Range` -- or ``None`` (value missing /
not yet filled) or :data:`NOT_SUITABLE` (``Range(nan, nan)`` -- the property does
not apply to this material). ``density`` is the one single-valued property.

:data:`PROPERTY_UNITS` is the **single** unit table spanning every material class
(metals, plastics, ...); each property name maps to its one fixed unit.
``hardness`` is intentionally absent -- its unit is per-material
(``hardness_scale``, e.g. HB / HRC / Shore D).

:class:`RangeMaterial` is a mixin giving any range-table dataclass a ``mass()``
helper and a pretty ``__str__`` dump aligned with those units.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, fields
from typing import Any, ClassVar, Literal, cast, get_args


@dataclass(frozen=True)
class Range:
    """A closed [min, max] band of typical values for one property."""

    min: float
    max: float

    def __post_init__(self) -> None:
        if self.min > self.max:
            raise ValueError(f"Range min {self.min} > max {self.max}")

    def value_at(self, r: float) -> float:
        """Value at fractional position ``r`` in the band: 0 -> min, 1 -> max.

        Explicit about *where* in the typical range you sample; the band makes no
        claim that the midpoint (``value_at(0.5)``) is the 'right' choice.
        """
        return self.min + r * (self.max - self.min)


# Sentinel: property not applicable to this material (Range(nan, nan)). Distinct
# from a field being None, which means "value missing / not yet filled".
NOT_SUITABLE = Range(math.nan, math.nan)


# Property units, split into the two display groups. __str__ prints them in this
# order -- "# mechanical properties" then "# thermal properties" -- alpha-sorted
# within each (mirroring the definition blocks). density is single-valued; every
# other property is a Range. `hardness`'s unit is per-material, so __str__ shows its
# `hardness_scale` rather than the placeholder here.
MECHANICAL_PROPERTY_UNITS: dict[str, str] = {
    "areal_density": "g/m²",  # areal goods (paper, textile) -- grammage
    "compressive_strength_parallel": "MPa",  # wood, along grain
    "density": "kg/m³",
    "elongation_at_break": "%",
    "hardness": "per hardness_scale",  # per-material unit (its hardness_scale)
    "janka_hardness": "N",  # wood hardness (indentation force)
    "modulus_of_elasticity": "GPa",
    "modulus_of_rupture": "MPa",  # wood bending strength
    "poisson_ratio": "",  # dimensionless
    "shear_modulus": "GPa",
    "shear_strength": "MPa",
    "tensile_strength": "MPa",
    "thickness": "mm",  # areal goods
    "yield_strength": "MPa",
}
THERMAL_PROPERTY_UNITS: dict[str, str] = {
    "glass_transition_temperature": "°C",
    "heat_deflection_temperature": "°C",
    "max_service_temp": "°C",
    "melting_temperature": "°C",
    "specific_heat_capacity": "J/(kg·K)",
    "thermal_conductivity": "W/(m·K)",
    "thermal_expansion": "1/K",
}
# Flat lookup over both groups -- the single per-property unit table used elsewhere.
PROPERTY_UNITS: dict[str, str] = {
    **MECHANICAL_PROPERTY_UNITS,
    **THERMAL_PROPERTY_UNITS,
}


# The category taxonomy: every material's ``category`` ClassVar must be one of
# these. ``pbr.py`` dispatches on it and ``finishes.py`` hints on it, so this is
# the canonical list of valid dispatch keys. ``"generic"`` is the abstract-base
# default (the intermediate SolidMaterial/PolymerMaterial/ArealMaterial bases carry
# it; no concrete material does). Enforced in ``RangeMaterial.__init_subclass__``.
Category = Literal[
    "generic",
    "metal",
    "plastic",
    "resin",
    "wood",
    "glass",
    "paper",
    "textile",
]
ALLOWED_CATEGORIES = frozenset(get_args(Category))

# Informal substrate groupings (not part of the formal Category taxonomy above),
# used by the PBR bridge and finish applicability. FERROUS is a family grouping;
# the rest are category groupings.
FERROUS = frozenset({"mild_steel", "alloy_steel", "tool_steel", "spring_steel"})
METAL = frozenset({"metal"})
PAINTABLE = frozenset({"metal", "plastic", "resin", "wood"})
COATABLE_POLY = frozenset({"metal", "plastic", "resin"})
EVERYTHING = frozenset(
    {"metal", "plastic", "resin", "wood", "glass", "paper", "textile"}
)


class RangeMaterial:
    """Mixin for range-table dataclasses: a ``mass()`` helper and a pretty
    ``__str__`` dump (``print(material)`` shows the aligned range table).

    The subclass must be a dataclass with a ``name`` field and ``Range | None``
    value fields whose names are keys of ``PROPERTY_UNITS``. A ``hardness`` field
    (metals, plastics, glass, resins) takes its unit from a companion
    ``hardness_scale`` string.

    Intrinsic identity/appearance the viz layer reads (not properties, so
    ``__str__`` skips them): ``category`` (fixed per subclass), ``family``
    (PBR key), ``transparent`` (see-through -> needs a part thickness).
    """

    name: str  # identifier (declared by the concrete dataclass)
    density: float  # kg/m³ -- the one universal single-value property
    category: ClassVar[str] = "generic"  # material class, overridden per subclass
    family: str | None = None  # PBR / identity key, e.g. "aluminum" (per instance)
    transparent: bool = False  # intrinsic optical: see-through (needs thickness)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Validate the subclass's ``category`` against the taxonomy at import."""
        super().__init_subclass__(**kwargs)
        if cls.category not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"{cls.__name__}: unknown category {cls.category!r} "
                f"(allowed: {sorted(ALLOWED_CATEGORIES)})"
            )

    def mass(self, volume_mm3: float) -> float:
        """Part mass in grams from a build123d volume in mm³ (m = rho * V).

        ``density`` is kg/m³ and build123d reports ``.volume`` in mm³, so the unit
        bridges are baked in (mm³ -> m³ x1e-9, kg -> g x1000).
        """
        return self.density * volume_mm3 * 1e-6

    def __str__(self) -> str:
        """Aligned 'property  value unit' lines under a '# mechanical properties'
        then '# thermal properties' header (one per non-empty group, taken from the
        two unit dicts in order; mirroring the definition blocks); the ``name`` is
        the title line. 'missing' / 'n/a' for the None / NOT_SUITABLE sentinels."""
        scale = getattr(self, "hardness_scale", "")
        have = {f.name for f in fields(cast(Any, self))}
        width = max(len(n) for n in PROPERTY_UNITS if n in have)
        lines = [getattr(self, "name")]
        for group, units in (
            ("mechanical", MECHANICAL_PROPERTY_UNITS),
            ("thermal", THERMAL_PROPERTY_UNITS),
        ):
            names = [n for n in units if n in have]
            if not names:
                continue
            lines.append(f"  # {group} properties")
            for name in names:
                val = getattr(self, name)
                unit = scale if name == "hardness" else units[name]
                if val is None:
                    body, unit = "missing", ""
                elif isinstance(val, Range) and math.isnan(val.min):
                    body, unit = "n/a", ""
                elif isinstance(val, Range):
                    body = f"{val.min:g} to {val.max:g}"
                else:
                    body = f"{val:g}"
                lines.append(f"  {name:{width}s}  {body} {unit}".rstrip())
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Shared base dataclasses (leaf classes add only their category-specific fields
# + the identity fields family/transparent, which -- being defaulted -- stay
# last). RangeMaterial itself is a non-dataclass mixin, so a branch's first
# dataclass (Solid/Areal) redeclares name/density as real fields.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class SolidMaterial(RangeMaterial):
    """Base for bulk isotropic solids (metals, glass, polymers): the property
    fields common to all of them."""

    name: str
    density: float  # kg/m³ (single representative value)
    tensile_strength: Range | None  # MPa
    modulus_of_elasticity: Range | None  # GPa
    shear_modulus: Range | None  # GPa
    poisson_ratio: Range | None  # dimensionless
    specific_heat_capacity: Range | None  # J/(kg·K)
    max_service_temp: Range | None  # °C (engineering guide limit, not a hard max)
    thermal_expansion: Range | None  # 1/K
    thermal_conductivity: Range | None  # W/(m·K)


@dataclass(frozen=True)
class PolymerMaterial(SolidMaterial):
    """Base for polymers (plastics, resins): adds the ductility/strength and
    thermal-transition fields plastics and resins share (glass has none of them)."""

    yield_strength: Range | None  # MPa
    shear_strength: Range | None  # MPa
    elongation_at_break: Range | None  # %
    glass_transition_temperature: Range | None  # °C
    heat_deflection_temperature: Range | None  # °C


@dataclass(frozen=True)
class ArealMaterial(RangeMaterial):
    """Base for areal goods (paper, textile): grammage-sized planar materials
    (mass from area, not volume). Leaf classes only set ``category``."""

    name: str
    density: float  # kg/m³ (apparent, single representative value)
    areal_density: Range | None  # g/m² (grammage -- primary mass metric)
    thickness: Range | None  # mm
    tensile_strength: Range | None  # MPa (in-plane; approx)
    thermal_conductivity: Range | None  # W/(m·K)
    specific_heat_capacity: Range | None  # J/(kg·K)
    family: str | None = None
    transparent: bool = False

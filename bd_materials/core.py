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


# One unit per property, across every material class, in canonical display order
# (describe() iterates these keys, so this is also the sole source of layout order --
# independent of each material's dataclass field/MRO order). density is single-valued;
# every other property is a Range. `hardness`'s unit is per-material, so describe()
# shows its `hardness_scale` rather than the placeholder listed here.
PROPERTY_UNITS: dict[str, str] = {
    "density": "kg/m³",
    "areal_density": "g/m²",  # areal goods (paper, textile) -- grammage
    "thickness": "mm",  # areal goods
    "tensile_strength": "MPa",
    "yield_strength": "MPa",
    "modulus_of_elasticity": "GPa",
    "modulus_of_rupture": "MPa",  # wood bending strength
    "shear_modulus": "GPa",
    "poisson_ratio": "",  # dimensionless
    "shear_strength": "MPa",
    "compressive_strength_parallel": "MPa",  # wood, along grain
    "elongation_at_break": "%",
    "shore_hardness": "Shore D",  # fixed-scale hardness (resins)
    "hardness": "per hardness_scale",  # metals/plastics/glass; unit is per-material
    "janka_hardness": "N",  # wood hardness (indentation force)
    "specific_heat_capacity": "J/(kg·K)",
    "melting_temperature": "°C",
    "glass_transition_temperature": "°C",
    "heat_deflection_temperature": "°C",
    "max_service_temp": "°C",
    "thermal_expansion": "1/K",
    "thermal_conductivity": "W/(m·K)",
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
    (metals/plastics) takes its unit from a companion ``hardness_scale`` string;
    ``shore_hardness`` (resins) uses its fixed unit like any other property.

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
        """Aligned 'property  value unit' lines in canonical order; 'missing' /
        'n/a' for the None / NOT_SUITABLE sentinels."""
        scale = getattr(self, "hardness_scale", "")
        have = {f.name for f in fields(cast(Any, self))}
        rows: list[tuple[str, str, str]] = []
        for name in PROPERTY_UNITS:  # canonical order == PROPERTY_UNITS order
            if name not in have:
                continue
            val = getattr(self, name)
            unit = scale if name == "hardness" else PROPERTY_UNITS[name]
            if val is None:
                body, unit = "missing", ""
            elif isinstance(val, Range) and math.isnan(val.min):
                body, unit = "n/a", ""
            elif isinstance(val, Range):
                body = f"{val.min:g} to {val.max:g}"
            else:
                body = f"{val:g}"
            rows.append((name, body, unit))
        width = max(len(n) for n, _, _ in rows)
        lines = [getattr(self, "name")]
        lines += [f"  {n:{width}s}  {b} {u}".rstrip() for n, b, u in rows]
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

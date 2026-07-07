"""Shared range primitives and the property-unit table for all range tables.

A material property is a min–max :class:`Range` -- or ``None`` (value missing /
not yet filled) or :data:`NOT_SUITABLE` (``Range(nan, nan)`` -- the property does
not apply to this material). ``density`` is the one single-valued property.

:data:`PROPERTY_UNITS` is the **single** unit table spanning every material class
(metals, plastics, ...); each property name maps to its one fixed unit.
``hardness`` is intentionally absent -- its unit is per-material
(``hardness_scale``, e.g. HB / HRC / Shore D).

:class:`RangeMaterial` is a mixin giving any range-table dataclass a
``describe()`` dump aligned with those units.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, fields
from typing import Any, cast


@dataclass(frozen=True)
class Range:
    """A closed [min, max] band of typical values for one property."""

    min: float
    max: float

    def __post_init__(self) -> None:
        if self.min > self.max:
            raise ValueError(f"Range min {self.min} > max {self.max}")

    @property
    def mid(self) -> float:
        """Midpoint -- a rough single 'nominal' when a calc needs one number."""
        return (self.min + self.max) / 2.0


# Sentinel: property not applicable to this material (Range(nan, nan)). Distinct
# from a field being None, which means "value missing / not yet filled".
NOT_SUITABLE = Range(math.nan, math.nan)


# One unit per property, across every material class. density is single-valued;
# every other property is a Range. hardness is absent (per-material scale).
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
    "janka_hardness": "N",  # wood hardness (indentation force)
    "specific_heat_capacity": "J/(kg·K)",
    "melting_temperature": "°C",
    "glass_transition_temperature": "°C",
    "heat_deflection_temperature": "°C",
    "max_service_temp": "°C",
    "thermal_expansion": "1/K",
    "thermal_conductivity": "W/(m·K)",
}


class RangeMaterial:
    """Mixin: a ``describe()`` dump for a range-table dataclass.

    The subclass must be a dataclass with a ``name`` field and ``Range | None``
    value fields whose names are keys of ``PROPERTY_UNITS``. A ``hardness`` field
    (metals/plastics) takes its unit from a companion ``hardness_scale`` string;
    ``shore_hardness`` (resins) uses its fixed unit like any other property.
    """

    def describe(self) -> str:
        """Aligned 'property  value unit' lines; 'missing'/'n/a' for the sentinels."""
        scale = getattr(self, "hardness_scale", "")
        rows: list[tuple[str, str, str]] = []
        for f in fields(cast(Any, self)):
            if f.name in ("name", "hardness_scale"):
                continue
            val = getattr(self, f.name)
            unit = scale if f.name == "hardness" else PROPERTY_UNITS[f.name]
            if val is None:
                body, unit = "missing", ""
            elif isinstance(val, Range) and math.isnan(val.min):
                body, unit = "n/a", ""
            elif isinstance(val, Range):
                body = f"{val.min:g} to {val.max:g}"
            else:
                body = f"{val:g}"
            rows.append((f.name, body, unit))
        width = max(len(n) for n, _, _ in rows)
        lines = [getattr(self, "name")]
        lines += [f"  {n:{width}s}  {b} {u}".rstrip() for n, b, u in rows]
        return "\n".join(lines)

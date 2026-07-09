"""The user-facing finished material -- the material as applied to a build123d part.

A ``FinishedMaterial`` bundles a range-based ``Material`` (the shared, immutable
typical-values table -- physics) with the **per-part choices**: ``color`` (a
selectable base colour), ``thickness_mm`` (pane thickness, only meaningful when the
material is ``transparent``), ``finish`` (an ``AppliedFinish`` or list of them), and
``process``. ``.material`` gives the physics; ``.pbr`` resolves the three.js look.

Colour precedence (resolved in ``pbr``): a covering finish colour > the selected
``color`` > the material's intrinsic look (derived from ``family``).

Threejs stays out of ``import bd_materials`` -- only ``.pbr`` pulls it in.
"""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Generic, TypeVar

from .finishes import AppliedFinish
from .core import RangeMaterial

if TYPE_CHECKING:  # real types for checkers; never imported at runtime (viz-free)
    from threejs_materials import PbrProperties

# colour input accepted by ``color=`` (name / hex string, or an RGB tuple)
Color = str | tuple[float, float, float]

# the concrete material class a FinishedMaterial carries (MetalMaterial, ...), so
# ``.material`` keeps its category-specific physics fields for type checkers
MaterialT = TypeVar("MaterialT", bound=RangeMaterial)


class Process(enum.Enum):
    """How a part is produced -- a use-time hint for the default surface look."""

    FDM = "fdm"
    SLS = "sls"
    MJF = "mjf"
    SLM = "slm"  # metal powder-bed / additive
    VAT = "vat"  # SLA / DLP resin
    MOLDED = "molded"
    MACHINED = "machined"
    CAST = "cast"
    WROUGHT = "wrought"


class FinishedMaterial(Generic[MaterialT]):
    """A range ``Material`` + per-part colour / thickness / finish(es) / process.

    The material stays a pure typical-values table; everything chosen per part
    lives here. ``pbr=`` supplies a ready-made look and cannot be combined with
    ``finish`` / ``process`` / ``color`` / ``thickness_mm``.

    Generic over the material class: a family function returns e.g.
    ``FinishedMaterial[MetalMaterial]``, so ``.material`` keeps the category's
    physics fields (``.material.tensile_strength``) for type checkers.
    """

    def __init__(
        self,
        material: MaterialT,
        finish: AppliedFinish | list[AppliedFinish] | None = None,
        *,
        color: Color | None = None,
        thickness_mm: float | None = None,
        process: Process | None = None,
        pbr: PbrProperties | None = None,
    ) -> None:
        if not isinstance(material, RangeMaterial):
            raise TypeError(
                "material must be a range Material (e.g. metals.aluminum().material), "
                f"not {type(material).__name__}"
            )
        if pbr is not None and (
            finish is not None
            or process is not None
            or color is not None
            or thickness_mm is not None
        ):
            raise ValueError(
                "pbr=... is a full override; do not combine it with finish, "
                "process, color, or thickness_mm"
            )
        if finish is not None and process is not None:
            raise ValueError(
                "finish and process are mutually exclusive: a finish defines the "
                "surface, so a process (the raw as-made surface) is ignored -- pass "
                "one or the other"
            )
        self.material: MaterialT = material
        self.finish = finish
        self.color = color
        self.thickness_mm = thickness_mm
        self.process = process
        self._pbr = pbr

    @property
    def pbr(self) -> PbrProperties:
        """The resolved three.js ``PbrProperties`` (needs ``threejs_materials``).

        The explicit override if supplied, else derived from the material's
        identity, the selected colour/thickness, the finish(es), and the process.
        The viz stack is imported here and nowhere else.
        """
        if self._pbr is not None:
            return self._pbr
        from .pbr import get_pbr_properties  # lazy: only here is the viz stack needed

        return get_pbr_properties(
            self.material,
            self.finish,
            self.process,
            color=self.color,
            thickness_mm=self.thickness_mm,
        )

    def __str__(self) -> str:
        """The underlying material's typical-value dump (physics only)."""
        return str(self.material)

    def __repr__(self) -> str:
        parts = [self.material.name]
        if self.color is not None:
            parts.append(f"color={self.color!r}")
        if self.thickness_mm is not None:
            parts.append(f"thickness_mm={self.thickness_mm}")
        if self.finish is not None:
            parts.append(f"finish={self.finish!r}")
        if self.process is not None:
            parts.append(f"process={self.process}")
        if self._pbr is not None:
            parts.append("pbr=<override>")
        return f"FinishedMaterial({', '.join(parts)})"

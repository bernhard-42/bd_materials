"""The user-facing finished material.

``FinishedMaterial`` is the main touch point: a base material plus how it is
coloured, finished, and produced. Access ``.material`` (physics/calc), ``.color``,
``.finish``, ``.process``, and ``.pbr`` (the resolved three.js look).

It stays dependency-light: ``threejs_materials`` is imported *lazily* inside the
``.pbr`` property, so ``import bd_materials`` never pulls in the viz stack.

The base material comes from a category function -- there is no string lookup;
the module namespaces are the catalog::

    from bd_materials import FinishedMaterial, Process, metals, plastics, finishes
    from bd_materials.metals import Alu

    FinishedMaterial(metals.aluminum())                      # bare
    FinishedMaterial(metals.aluminum(Alu.G7075_T6), finishes.anodize("champagne"))
    FinishedMaterial(plastics.pla(color="red"))              # coloured filament
    FinishedMaterial(plastics.pla(color="gray"), process=Process.FDM)   # as-printed
    FinishedMaterial(metals.aluminum(), pbr=my_pbr)          # explicit override

Colour vs finish. ``color`` overrides the material's own colour for this part
(a plastic's ``.color``); it only affects the bare / mechanically-textured look,
since a surface finish (paint, powder, anodize, plating) carries its own colour
and covers what's beneath. It does nothing to bare metals, whose colour is
intrinsic.

``pbr`` is a full, pre-built override; it is mutually exclusive with
``finish`` / ``process`` / ``color``.
"""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, overload

from .base import Material
from .finishes import AppliedFinish

if TYPE_CHECKING:  # real types for checkers; never imported at runtime (viz-free)
    from threejs_materials import PbrProperties

# colour input accepted by ``color=`` (name / hex string, or an RGB tuple)
Color = str | tuple[float, float, float]


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


class FinishedMaterial:
    """A base material + colour + finish(es) + process, with a resolved ``.pbr``.

    See the module docstring for the accepted call forms. ``pbr=`` supplies a
    ready-made look and cannot be combined with ``finish`` / ``process`` /
    ``color``.
    """

    @overload
    def __init__(
        self,
        material: Material,
        finish: AppliedFinish | list[AppliedFinish] | None = ...,
        *,
        process: Process | None = ...,
        color: Color | None = ...,
    ) -> None: ...

    @overload
    def __init__(self, material: Material, *, pbr: PbrProperties) -> None: ...

    def __init__(
        self,
        material: Material,
        finish: AppliedFinish | list[AppliedFinish] | None = None,
        *,
        process: Process | None = None,
        color: Color | None = None,
        pbr: PbrProperties | None = None,
    ) -> None:
        """Build a finished material.

        Args:
            material: A :class:`Material` from a category function
                (e.g. ``metals.aluminum()``).
            finish: An ``AppliedFinish`` (from a finish function, e.g.
                ``anodize("red")``) or a list of them; colour rides along in
                the finish.
            process: How the part is produced -- nudges the default surface
                (printed / as-built routes render rough).
            color: Overrides the material's own base colour for this part.
                Ignored for bare metals.
            pbr: A ready-made ``PbrProperties`` to use verbatim. Mutually
                exclusive with ``finish`` / ``process`` / ``color``.

        Raises:
            TypeError: if ``material`` is not a :class:`Material`.
            ValueError: if ``pbr`` is combined with ``finish`` / ``process`` /
                ``color``.
        """
        if not isinstance(material, Material):
            raise TypeError(
                "material must be a Material (from a category function, e.g. "
                f"metals.aluminum()), not {type(material).__name__}"
            )
        if pbr is not None and (
            finish is not None or process is not None or color is not None
        ):
            raise ValueError(
                "pbr=... is a full override; do not combine it with "
                "finish, process, or color"
            )
        self.material = material
        self.finish = finish
        self.process = process
        self.color = color
        self._pbr = pbr

    @property
    def pbr(self) -> PbrProperties:
        """The resolved three.js ``PbrProperties`` (needs ``threejs_materials``).

        Returns the explicit override when one was supplied, otherwise derives
        the look from the material, colour, finish(es), and process. The viz
        stack is imported here and nowhere else, so constructing a
        ``FinishedMaterial`` stays threejs-free.
        """
        if self._pbr is not None:
            return self._pbr
        from .pbr import get_pbr_properties  # lazy: only here is the viz stack needed

        return get_pbr_properties(
            self.material, self.finish, self.process, color=self.color
        )

    def __repr__(self) -> str:
        parts = [repr(self.material.name)]
        if self.color is not None:
            parts.append(f"color={self.color!r}")
        if self.finish is not None:
            parts.append(f"finish={self.finish!r}")
        if self.process is not None:
            parts.append(f"process={self.process}")
        if self._pbr is not None:
            parts.append("pbr=<override>")
        return f"FinishedMaterial({', '.join(parts)})"

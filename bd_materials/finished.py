"""The user-facing finished material.

``FinishedMaterial`` is the main touch point: a material plus how it's finished
and produced. Access ``.material`` (physics/calc), ``.finish``, and ``.pbr``
(the resolved three.js look). It's dependency-light -- ``threejs_materials`` is
imported *lazily* inside the ``.pbr`` property, so ``import bd_materials`` never
pulls in the viz stack. Colour lives in the finish (see the finish functions in
``finishes``), so there's no separate colour argument.

    from bd_materials import metals, FinishedMaterial, Process
    from bd_materials import spray_paint, anodize, brushed

    FinishedMaterial(metals.ALU_6061_T6).pbr                      # bare
    FinishedMaterial(metals.ALU_6061_T6, anodize("champagne")).pbr
    FinishedMaterial(metals.ALU_6061_T6, [brushed(), anodize("blue")]).pbr
    FinishedMaterial(metals.PLA, process=Process.FDM).pbr         # as-printed
    FinishedMaterial(mat, _pbr=my_pbr).pbr                        # explicit override
"""

from __future__ import annotations

import enum
from dataclasses import dataclass

from .base import Material
from .finishes import AppliedFinish


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


@dataclass(frozen=True)
class FinishedMaterial:
    """A material + finish(es) + process, with a resolved ``.pbr`` look.

    Two mutually exclusive ways to give the look:
      * derive it -- ``FinishedMaterial(mat, finish, process=...)``
      * supply it -- ``FinishedMaterial(mat, finish, _pbr=my_pbr)``

    ``finish`` is an ``AppliedFinish`` (from a finish function, e.g.
    ``anodize("red")``) or a list of them; colour rides along in the finish.
    """

    material: Material
    finish: AppliedFinish | list[AppliedFinish] | None = None
    process: Process | None = None
    _pbr: object | None = None  # explicit PbrProperties override

    def __post_init__(self) -> None:
        if self._pbr is not None and self.process is not None:
            raise ValueError("give either _pbr=... or process=..., not both")

    @property
    def pbr(self):
        """The resolved three.js ``PbrProperties`` (needs threejs_materials)."""
        if self._pbr is not None:
            return self._pbr
        from .pbr import get_pbr_properties  # lazy: only here is the viz stack needed

        return get_pbr_properties(self.material, self.finish, self.process)

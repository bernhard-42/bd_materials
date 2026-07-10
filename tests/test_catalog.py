"""Catalog + PBR smoke tests.

The dataclass constructors already validate the data at import: ``Range.__post_init__``
rejects inverted bands and ``RangeMaterial.__init_subclass__`` rejects unknown
categories. These tests target what those do *not* cover:

- the catalog stays the expected size with unique names,
- ``mass()`` scales linearly with volume,
- the ``FinishedMaterial`` guard rails raise, and
- (the main event) every material resolves a three.js PBR look across the
  color / finish / process paths -- the branch-per-category logic in ``pbr.py``,
  which nothing else exercises. These are skipped when ``threejs_materials`` is absent.
"""

import pytest

from bd_materials import finishes
from bd_materials.core import ALLOWED_CATEGORIES
from bd_materials.finished import FinishedMaterial, Process
from bd_materials.finishes import Sheen
from bd_materials.materials import (
    ALL_MATERIALS,
    glass,
    metals,
    paper,
    plastics,
    textile,
    wood,
)

try:  # the PBR tests need the viz stack; the rest run without it
    import threejs_materials  # noqa: F401

    HAS_THREEJS = True
except ImportError:
    HAS_THREEJS = False

requires_threejs = pytest.mark.skipif(
    not HAS_THREEJS, reason="threejs_materials not installed"
)


def test_catalog_size_and_unique_names():
    """The catalog holds the expected 87 materials, each with a unique name."""
    assert len(ALL_MATERIALS) == 87
    names = [m.name for m in ALL_MATERIALS]
    assert len(names) == len(set(names))


@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_category_in_taxonomy(material):
    """Every material's category is a member of the allowed taxonomy."""
    assert material.category in ALLOWED_CATEGORIES


@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_mass_scales_linearly_with_volume(material):
    """``mass()`` is positive and linear in volume (m = rho * V)."""
    assert material.mass(1000) > 0
    assert material.mass(2000) == pytest.approx(2 * material.mass(1000))


def test_family_function_returns_finished_material():
    """A family function returns a ``FinishedMaterial`` wrapping its material."""
    fm = metals.aluminum()
    assert isinstance(fm, FinishedMaterial)
    assert fm.material.category == "metal"
    assert fm.material.family == "aluminum"


def test_density_override_is_per_part_and_cast_free():
    """``density=`` overrides the part copy without touching the shared catalog entry."""
    default = metals.aluminum().material.density
    overridden = metals.aluminum(density=1234).material
    assert overridden.density == 1234
    assert metals.aluminum().material.density == default  # catalog entry unchanged


def test_finish_and_process_are_mutually_exclusive():
    """Passing both ``finish`` and ``process`` raises (a finish defines the surface)."""
    with pytest.raises(ValueError):
        metals.aluminum(finish=finishes.anodize("black"), process=Process.MACHINED)


@requires_threejs
def test_pbr_override_excludes_other_look_inputs():
    """``pbr=`` is a full override and cannot be combined with per-part look inputs."""
    look = metals.aluminum().pbr  # a real resolved PbrProperties
    with pytest.raises(ValueError):
        FinishedMaterial(metals.aluminum().material, color="red", pbr=look)


# --- PBR resolution: every material + a spread of finish/color/process paths ---

# One case per branch in pbr.py's dispatch and per surface handler in _SURFACE.
_PBR_CASES = {
    # bare substrates (case-1 / case-2 color, transmissive, composite)
    "alu_bare": lambda: metals.aluminum(),
    "pla_color_fdm": lambda: plastics.pla(color="red", process=Process.FDM),
    "pmma_clear_pane": lambda: plastics.pmma(color="clear", thickness_mm=3),
    "pc_pane": lambda: plastics.pc(thickness_mm=4),
    "cfrp": lambda: plastics.cfrp(),
    "boro_pane": lambda: glass.borosilicate(color="green", thickness_mm=5),
    "oak": lambda: wood.hardwood(),
    "paper": lambda: paper.paper(),
    "cardboard": lambda: paper.cardboard(),
    "woven_color": lambda: textile.woven(color="blue"),
    # texture (mechanical) finishes
    "alu_brushed": lambda: metals.aluminum(finish=finishes.brushed()),
    "alu_bead_blast": lambda: metals.aluminum(finish=finishes.bead_blast()),
    "steel_slm_rough": lambda: metals.mild_steel(process=Process.SLM),
    # surface (color) finishes -- one per _SURFACE handler
    "alu_anodize": lambda: metals.aluminum(finish=finishes.anodize("blue")),
    "steel_black_oxide": lambda: metals.mild_steel(finish=finishes.black_oxide()),
    "alu_dye": lambda: metals.aluminum(finish=finishes.dye("red")),
    "nylon_dye": lambda: plastics.nylon(finish=finishes.dye("blue")),
    "ss_pvd_clear": lambda: metals.stainless(finish=finishes.pvd()),
    "ss_pvd_gold": lambda: metals.stainless(finish=finishes.pvd("gold")),
    "ss_chrome": lambda: metals.stainless(finish=finishes.chrome()),
    "brass_gold": lambda: metals.brass(finish=finishes.gold_plate()),
    "copper_silver": lambda: metals.copper(finish=finishes.silver_plate()),
    "copper_nickel": lambda: metals.copper(finish=finishes.nickel_plate()),
    "copper_tin": lambda: metals.copper(finish=finishes.tin_plate()),
    "steel_zinc": lambda: metals.mild_steel(finish=finishes.zinc_plate("yellow")),
    "ti_vacuum": lambda: metals.titanium(finish=finishes.vacuum_plating("black")),
    "steel_powder": lambda: metals.mild_steel(finish=finishes.powder_coat("red")),
    "alu_spray_matte": lambda: metals.aluminum(
        finish=finishes.spray_paint("green", Sheen.MATTE)
    ),
    "steel_ecoat": lambda: metals.mild_steel(finish=finishes.electrophoresis()),
    "steel_ecoat_white": lambda: metals.mild_steel(
        finish=finishes.electrophoresis("white")
    ),
    "alu_brushed_ecoat": lambda: metals.aluminum(
        finish=[finishes.brushed(), finishes.electrophoresis()]
    ),
    # anodize on a brushed substrate (recolor-keeping-relief branch)
    "alu_brushed_anodize": lambda: metals.aluminum(
        finish=[finishes.brushed(), finishes.anodize("black")]
    ),
}


@requires_threejs
@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_every_material_resolves_a_pbr_look(material):
    """Each catalog material resolves a three.js look through its category branch."""
    fm = FinishedMaterial(material, thickness_mm=3 if material.transparent else None)
    assert fm.pbr is not None


@requires_threejs
@pytest.mark.parametrize("build", _PBR_CASES.values(), ids=list(_PBR_CASES))
def test_finish_color_process_paths_resolve(build):
    """Every finish / color / process path in pbr.py resolves without error."""
    assert build().pbr is not None

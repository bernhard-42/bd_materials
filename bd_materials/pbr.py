"""Bridge from a finished material to a bundled three.js PBR material.

``get_pbr_properties(material, finish, process, color, thickness_mm, pbr)`` resolves
the right ``threejs_materials`` factory for how a part looks -- the function behind
the ``FinishedMaterial.pbr`` property (the user-facing entry, in ``finished``).

``finish`` is an ``AppliedFinish`` (from a finish function like
``spray_paint("blue")``) or a list of them; each carries its color. Finishes
split on two axes: **texture** (brushed / bead-blast -> metal relief variants)
and **surface/color** (anodize/PVD override; paint covers; plating replaces).
``process`` (a ``Process``) nudges the default surface: printed/as-built routes
render rough, everything else smooth. ``pbr`` (if given) is returned unchanged.

Requires ``threejs_materials`` (kept out of ``bd_materials``'s core imports; only
this module and ``FinishedMaterial.pbr`` pull it in).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from threejs_materials import coats, glass, metal, paper, plastic, textile, wood

from . import finishes as fin
from .core import FERROUS, RangeMaterial
from .finished import Color, FinishSpec, Process
from .finishes import AppliedFinish

if TYPE_CHECKING:  # real types for checkers; never imported at runtime (viz-free)
    from threejs_materials import PbrProperties

# as-printed / as-built routes default to a rough surface; the rest stay smooth
_ROUGH_PROCESSES = frozenset({Process.FDM, Process.SLS, Process.MJF, Process.SLM})

# --- color names -> sRGB hex (None = leave factory default / not colorable) --
_COLOR_HEX: dict[str, str | None] = {
    "natural": None,
    "clear": None,
    "black": "#111111",
    "white": "#f5f5f5",
    "gray": "#808080",
    "gunmetal": "#2a3439",
    "silver": "#c0c0c0",
    "nickel": "#b8b8b0",
    "chrome": "#c8ccce",
    "gold": "#d4af37",
    "rose gold": "#b76e79",
    "champagne": "#e6c99a",
    "brown": "#5c4033",
    "red": "#c0392b",
    "orange": "#e67e22",
    "yellow": "#f1c40f",
    "green": "#27ae60",
    "blue": "#2e86de",
    "purple": "#8e44ad",
}

# metal families with a dedicated bundled factory (else steel / stainless)
_BARE_METALS = frozenset(
    {"aluminum", "brass", "copper", "stainless", "titanium", "tin", "gold", "silver"}
)

# mechanical finishes -> metal surface-relief variant (None elsewhere = smooth)
_MECH = fin.MECHANICAL_FINISHES
_TEXTURE = {
    _MECH[fin.Mechanical.BRUSHED]: "brushed",
    _MECH[fin.Mechanical.BEAD_BLAST]: "matte",
    _MECH[fin.Mechanical.FINE_SANDING]: "matte",
}


def _color_value(color: Color | None) -> Color | None:
    """A standard color name -> hex; hex / CSS name / RGB tuple pass through."""
    if color is None:
        return None
    if isinstance(color, str):
        key = color.strip().lower()
        if key in _COLOR_HEX:
            return _COLOR_HEX[key]
        return color
    return color  # (r, g, b) tuple/list


def _metal_name(material: RangeMaterial) -> str:
    """The bundled metal-factory key for the material (a bare family, else steel/stainless)."""
    fam = material.family
    if fam in _BARE_METALS:
        return fam
    if fam in FERROUS:
        return "steel"
    return "stainless"  # last-resort fallback


def _is_carbon(material: RangeMaterial) -> bool:
    """Whether the material is the carbon-fiber (CFRP) family."""
    return material.family == "CFRP"


def _metal_tex_base(material: RangeMaterial, texture: str | None) -> PbrProperties:
    """Bare metal, optionally with a brushed/matte relief variant."""
    name = _metal_name(material)
    if texture is not None:
        return getattr(metal, f"{name}_{texture}")()
    return getattr(metal, name)()


def _plain_base(
    material: RangeMaterial,
    texture: str | None,
    rgb: Color | None,
    thickness: float | None,
) -> PbrProperties:
    """Look for a material with no covering color finish -- substrate + texture.

    Wood/paper/textile pick a bundled factory by ``family`` (the factory key),
    falling back to a generic factory for a family three.js doesn't bundle.

    Args:
        material: The material whose bare look to build.
        texture: A relief variant ("brushed" / "matte"), or ``None`` for smooth.
        rgb: The base color as hex / RGB, or ``None`` for the factory default.
        thickness: Pane thickness (mm) for transmissive materials (glass and anything
            flagged ``transparent``); ignored otherwise.

    Returns:
        The resolved ``PbrProperties``.
    """
    cat = material.category
    fam = material.family if material.family is not None else ""
    if cat == "metal":
        return _metal_tex_base(material, texture)
    if cat == "wood":
        factory = getattr(wood, fam, None)
        return (factory if factory is not None else wood.oak)(color=rgb)
    if cat == "glass":
        return glass.glass(color=rgb, thickness=thickness)
    if cat == "paper":
        factory = getattr(paper, fam, None)
        return (factory if factory is not None else paper.paper)(color=rgb)
    if cat == "textile":
        factory = getattr(textile, fam, None)
        return (factory if factory is not None else textile.fabric_weave)(color=rgb)
    # plastic / resin (composites stay in this branch)
    if material.transparent:
        # transmissive: refraction depends on pane thickness (three.js acrylic
        # approximates both PMMA and PC well enough)
        return plastic.acrylic(color=rgb, thickness=thickness)
    if _is_carbon(material):
        return plastic.carbon_fiber(color=rgb)
    if texture is not None:
        return plastic.plastic_rough(color=rgb)
    return plastic.plastic_clean(color=rgb)


# Dark conversion / e-coat finishes render as a very dark neutral grey, not an
# optical-void black, so surface geometry stays legible in the viewer: black oxide
# reads as matte "tool black" (gun-blue), e-coat black as a deep charcoal. Both are
# nominal look values, tune to taste.
_BLACK_OXIDE_GREY = "#2a2a2a"
_ECOAT_CHARCOAL = "#2e2e2e"


# --- surface (color) finishes: (material, rgb, texture, sheen) -> PbrProperties ---
# All handlers share this signature; sheen (gloss/matte) is only used by the
# paint/coat handler, ignored by the rest.
def _anodized(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Anodized look: recolor, keeping any brushed/blasted relief."""
    if m.family == "aluminum" and texture is None:
        return metal.aluminum_anodized(color=rgb)  # tuned preset for the common case
    base = _metal_tex_base(m, texture)  # keep relief; scalar recolor
    if rgb is not None:
        return base.override(color=rgb, roughness=0.3)
    return base


def _pvd(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """PVD look: "clear" shows the substrate metal; a color becomes a metallic coat."""
    if rgb is None:
        return _metal_tex_base(m, texture)  # clear PVD: bright substrate metal
    if texture is not None:  # keep the brushed/blasted relief
        return _metal_tex_base(m, texture).override(color=rgb, roughness=0.15)
    return coats.metallic_coat_gloss(color=rgb)


def _black_oxide(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Black-oxide look: matte very-dark-grey (tool black), keeping relief or as a coat."""
    if texture is not None:  # keep the blasted/brushed relief
        return _metal_tex_base(m, texture).override(
            color=_BLACK_OXIDE_GREY, roughness=0.5
        )
    return coats.metallic_coat_matte(color=_BLACK_OXIDE_GREY)


def _dyeing(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Dyed look: aluminum behaves like anodize; polymers tint the base."""
    if m.family == "aluminum":
        return _anodized(m, rgb, texture, sheen)
    return _plain_base(m, texture, rgb, None)  # dyed polymer: base tinted by color


def _chrome(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Chrome-plated look."""
    return coats.chrome()


def _gold(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Gold-plated look."""
    return metal.gold()


def _silver(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Silver-plated look."""
    return metal.silver()


def _nickel(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Nickel-plated look (tinted silver until metal.nickel is bundled)."""
    fn = getattr(metal, "nickel", None)  # adopt metal.nickel once bundled
    if fn is not None:
        return fn()
    return metal.silver().override(color="#b9b9b2")


def _tin(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Tin-plated look (matte / satin)."""
    # tin plating is matte/satin (matte tin is the solderability standard); prefer
    # the matte factory, else roughen the glossy plain-tin factory
    fn = getattr(metal, "tin_matte", None)
    if fn is not None:
        return fn()
    return metal.tin().override(roughness=0.4)


def _zinc(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Zinc-plated look (satin), optionally tinted."""
    # zinc plating is satin; prefer the matte zinc factory, else roughen the glossy
    # plain-zinc factory
    fn = getattr(metal, "zinc_matte", None)
    base = fn() if fn is not None else metal.zinc().override(roughness=0.4)
    if rgb is not None:
        return base.override(color=rgb)
    return base


def _coat(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Painted / coated look in ``rgb``; gloss or matte per ``sheen``."""
    fn = coats.coat_matte if sheen == fin.Sheen.MATTE else coats.coat_gloss
    return fn(color=rgb)


def _ecoat(
    m: RangeMaterial, rgb: Color | None, texture: str | None, sheen: fin.Sheen | None
) -> PbrProperties:
    """Electrophoretic e-coat look; the thin semi-transparent film reads as a deep
    charcoal even for "black", never optical-void black; other colors pass through."""
    if rgb is None or rgb == _COLOR_HEX["black"]:
        rgb = _ECOAT_CHARCOAL  # black (the default/common e-coat) -> deep charcoal
    return coats.coat_matte(color=rgb)


_CHEM = fin.CHEMICAL_FINISHES
_PLATE = fin.METAL_PLATING_FINISHES
_COAT = fin.COATING_FINISHES
_SURFACE = {
    _CHEM[fin.Chemical.ANODIZED]: _anodized,
    _CHEM[fin.Chemical.BLACK_OXIDE]: _black_oxide,
    _CHEM[fin.Chemical.DYEING]: _dyeing,
    _PLATE[fin.MetalPlating.PVD]: _pvd,
    _PLATE[fin.MetalPlating.CHROME_PLATING]: _chrome,
    _PLATE[fin.MetalPlating.GOLD_PLATING]: _gold,
    _PLATE[fin.MetalPlating.NICKEL_PLATING]: _nickel,
    _PLATE[fin.MetalPlating.SILVER_PLATING]: _silver,
    _PLATE[fin.MetalPlating.TIN_PLATING]: _tin,
    _PLATE[fin.MetalPlating.ZINC_PLATING]: _zinc,
    _PLATE[fin.MetalPlating.VACUUM_PLATING]: _coat,
    _COAT[fin.Coating.POWDER_COAT]: _coat,
    _COAT[fin.Coating.SPRAY_PAINT]: _coat,
    _COAT[fin.Coating.ELECTROPHORESIS]: _ecoat,
}
# everything else (smooth machining, electropolished, passivation, pickling,
# chem film, conductive oxidation, laser, etch, silkscreen) leaves the look as-is.


def _normalize(
    finish: FinishSpec,
) -> list[tuple[fin.Finish, str | None, fin.Sheen | None]]:
    """Normalize the ``finish`` argument to a list of (Finish, color, sheen).

    Args:
        finish: ``None``, a single ``AppliedFinish`` / ``Finish``, or a list of them.

    Returns:
        A list of ``(Finish, color, sheen)`` tuples; a raw ``Finish`` yields
        ``(finish, None, None)``.
    """
    if finish is None:
        return []
    seq = finish if isinstance(finish, (list, tuple)) else [finish]
    out = []
    for f in seq:
        if isinstance(f, AppliedFinish):
            out.append((f.finish, f.color, f.sheen))
        else:  # a raw Finish -> no color / sheen
            out.append((f, None, None))
    return out


def get_pbr_properties(
    material: RangeMaterial,
    finish: FinishSpec = None,
    process: Process | None = None,
    color: Color | None = None,
    thickness_mm: float | None = None,
    pbr: PbrProperties | None = None,
) -> PbrProperties:
    """Resolve a bundled three.js look for a finished material.

    Args:
        material: The material being rendered (dispatched on its ``category``).
        finish: An ``AppliedFinish`` (e.g. from ``spray_paint("blue")``) or a list of
            them -- each carries its own color.
        process: A ``Process`` that nudges the default surface (printed -> rough).
        color: The material's own base color, applied only when no surface finish
            covers it (e.g. a colored filament or tinted resin); ignored for bare
            metals, whose color is intrinsic.
        thickness_mm: Pane thickness (mm) for transmissive materials.
        pbr: A ready-made look, returned unchanged if given.

    Returns:
        The resolved ``PbrProperties``.
    """
    if pbr is not None:
        return pbr

    texture = None
    surface = None
    surface_color = None
    surface_sheen = None
    for f, col, sheen in _normalize(finish):
        if f in _TEXTURE:
            texture = _TEXTURE[f]
        elif f in _SURFACE:
            surface = f
            surface_color = col
            surface_sheen = sheen
    if texture is None and process in _ROUGH_PROCESSES:
        texture = "matte"  # as-printed / as-built relief

    if surface is None:
        # No covering/coloring finish -> the per-part color (case-2 selection);
        # bare metals pass color=None and render their intrinsic look.
        return _plain_base(material, texture, _color_value(color), thickness_mm)
    rgb = _color_value(surface_color)
    return _SURFACE[surface](material, rgb, texture, surface_sheen)


__all__ = ["get_pbr_properties"]

"""Bridge from a finished material to a bundled three.js PBR material.

``get_pbr_properties(material, finish, process, color, pbr)`` resolves the right
``threejs_materials`` factory for how a part looks -- the function behind
the ``FinishedMaterial.pbr`` property (the user-facing entry, in ``finished``).

``finish`` is an ``AppliedFinish`` (from a finish function like
``spray_paint("blue")``) or a list of them; each carries its colour. Finishes
split on two axes: **texture** (brushed / bead-blast -> metal relief variants)
and **surface/colour** (anodize/PVD override; paint covers; plating replaces).
``process`` (a ``Process``) nudges the default surface: printed/as-built routes
render rough, everything else smooth. ``pbr`` (if given) is returned unchanged.

Requires ``threejs_materials`` (kept out of ``bd_materials``'s core imports; only
this module and ``FinishedMaterial.pbr`` pull it in).
"""

from __future__ import annotations

from threejs_materials import coats, glass, metal, paper, plastic, textile, wood

from . import finishes as fin
from .core import FERROUS, RangeMaterial
from .finished import Process
from .finishes import AppliedFinish

# as-printed / as-built routes default to a rough surface; the rest stay smooth
_ROUGH_PROCESSES = frozenset({Process.FDM, Process.SLS, Process.MJF, Process.SLM})

# --- colour names -> sRGB hex (None = leave factory default / not colourable) --
_COLOR_HEX: dict[str, str | None] = {
    "natural": None,
    "clear": None,
    fin.CUSTOM: None,
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

_TEXTILE = {
    "Woven Fabric": "fabric_weave",
    "Knit Fabric": "fabric_knit",
    "Felt": "felt",
    "Leather": "leather",
}

# mechanical finishes -> metal surface-relief variant (None elsewhere = smooth)
_MECH = fin.MECHANICAL_FINISHES
_TEXTURE = {
    _MECH[fin.Mechanical.BRUSHED]: "brushed",
    _MECH[fin.Mechanical.BEAD_BLAST]: "matte",
    _MECH[fin.Mechanical.FINE_SANDING]: "matte",
}


def _color_value(color):
    """A standard colour name -> hex; hex / CSS name / RGB tuple pass through."""
    if color is None:
        return None
    if isinstance(color, str):
        key = color.strip().lower()
        if key in _COLOR_HEX:
            return _COLOR_HEX[key]
        return color
    return color  # (r, g, b) tuple/list


def _metal_name(material: RangeMaterial) -> str:
    fam = material.family
    if fam in _BARE_METALS:
        return fam
    if fam in FERROUS:
        return "steel"
    return "stainless"  # last-resort fallback


def _is_carbon(material: RangeMaterial) -> bool:
    return material.family == "CFRP"


def _metal_tex_base(material: RangeMaterial, texture):
    """Bare metal, optionally with a brushed/matte relief variant."""
    name = _metal_name(material)
    return getattr(metal, f"{name}_{texture}")() if texture else getattr(metal, name)()


def _plain_base(material: RangeMaterial, texture, rgb, thickness):
    """Look with no colour finish -- substrate + optional texture.

    Wood/paper/textile pick a bundled factory by ``family`` (the factory key),
    falling back to a generic factory for grades three.js doesn't bundle
    (e.g. pine, the wood generics). ``thickness`` (per part) feeds transmissive
    materials -- glass and any material flagged ``transparent``.
    """
    cat = material.category
    fam = material.family or ""
    if cat == "metal":
        return _metal_tex_base(material, texture)
    if cat == "wood":
        return (getattr(wood, fam, None) or wood.oak)(color=rgb)
    if cat == "glass":
        return glass.glass(color=rgb, thickness=thickness)
    if cat == "paper":
        return (getattr(paper, fam, None) or paper.paper)(color=rgb)
    if cat == "textile":
        return (getattr(textile, fam, None) or textile.fabric_weave)(color=rgb)
    # plastic / resin (composites stay in this branch)
    if material.transparent:
        # transmissive: refraction depends on pane thickness (three.js acrylic
        # approximates both PMMA and PC well enough)
        return plastic.acrylic(color=rgb, thickness=thickness)
    if _is_carbon(material):
        return plastic.carbon_fiber(color=rgb)
    if texture:
        return plastic.plastic_rough(color=rgb)
    return plastic.plastic_clean(color=rgb)


# --- surface (colour) finishes: (material, rgb, texture, sheen) -> PbrProperties ---
# All handlers share this signature; sheen (gloss/matte) is only used by the
# paint/coat handler, ignored by the rest.
def _anodized(m, rgb, texture, sheen):
    if m.family == "aluminum" and texture is None:
        return metal.aluminum_anodized(color=rgb)  # tuned preset for the common case
    base = _metal_tex_base(m, texture)  # keep relief; scalar recolour
    return base.override(color=rgb, roughness=0.3) if rgb else base


def _pvd(m, rgb, texture, sheen):
    if rgb is None:
        return _metal_tex_base(m, texture)  # clear PVD: bright substrate metal
    if texture:  # keep the brushed/blasted relief
        return _metal_tex_base(m, texture).override(color=rgb, roughness=0.15)
    return coats.metallic_coat_gloss(color=rgb)


def _black_oxide(m, rgb, texture, sheen):
    if texture:  # keep the blasted/brushed relief
        return _metal_tex_base(m, texture).override(color="#141414", roughness=0.5)
    return coats.metallic_coat_matte(color="#141414")


def _dyeing(m, rgb, texture, sheen):
    if m.family == "aluminum":
        return _anodized(m, rgb, texture, sheen)
    return _plain_base(m, texture, rgb, None)  # dyed polymer: base tinted by colour


def _chrome(m, rgb, texture, sheen):
    return coats.chrome()


def _gold(m, rgb, texture, sheen):
    return metal.gold()


def _silver(m, rgb, texture, sheen):
    return metal.silver()


def _nickel(m, rgb, texture, sheen):
    fn = getattr(metal, "nickel", None)  # adopt metal.nickel once bundled
    return fn() if fn else metal.silver().override(color="#b9b9b2")


def _tin(m, rgb, texture, sheen):
    # tin plating is matte/satin (matte tin is the solderability standard); prefer
    # the matte factory, else roughen the glossy plain-tin factory
    fn = getattr(metal, "tin_matte", None)
    return fn() if fn else metal.tin().override(roughness=0.4)


def _zinc(m, rgb, texture, sheen):
    # zinc plating is satin; prefer the matte zinc factory, else roughen the glossy
    # plain-zinc factory
    fn = getattr(metal, "zinc_matte", None)
    base = fn() if fn else metal.zinc().override(roughness=0.4)
    return base.override(color=rgb) if rgb else base


def _coat(m, rgb, texture, sheen):
    fn = coats.coat_matte if sheen == fin.Sheen.MATTE else coats.coat_gloss
    return fn(color=rgb)


def _ecoat(m, rgb, texture, sheen):
    return coats.coat_matte(color=rgb or "#101010")


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


def _normalize(finish):
    """finish -> list of (Finish, colour, sheen); unwraps AppliedFinish, tolerates
    a raw Finish."""
    if finish is None:
        return []
    seq = finish if isinstance(finish, (list, tuple)) else [finish]
    out = []
    for f in seq:
        if isinstance(f, AppliedFinish):
            out.append((f.finish, f.color, f.sheen))
        else:  # a raw Finish -> no colour / sheen
            out.append((f, None, None))
    return out


def get_pbr_properties(
    material: RangeMaterial,
    finish=None,
    process=None,
    color=None,
    thickness_mm=None,
    pbr=None,
):
    """Resolve a bundled three.js ``PbrProperties`` for a finished material.

    ``finish`` is an ``AppliedFinish`` (from a finish function like
    ``spray_paint("blue")``) or a list of them -- each carries its own colour.
    ``process`` (a ``Process``) nudges the default surface (printed -> rough).
    ``color`` is the material's own base colour, applied only when no surface
    finish covers it (e.g. a coloured filament or tinted resin); it has no
    effect on bare metals, whose colour is intrinsic. ``pbr`` (if given) is
    returned unchanged.
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
        # No covering/colouring finish -> the per-part colour (case-2 selection);
        # bare metals pass color=None and render their intrinsic look.
        return _plain_base(material, texture, _color_value(color), thickness_mm)
    rgb = _color_value(surface_color)
    return _SURFACE[surface](material, rgb, texture, surface_sheen)


__all__ = ["get_pbr_properties"]

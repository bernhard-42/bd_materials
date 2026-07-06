"""Bridge from a finished material to a bundled three.js PBR material.

``get_pbr_properties(material, finish, process, pbr)`` resolves the right
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
from .base import Material
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
_TEXTURE = {
    fin.BRUSHED: "brushed",
    fin.BEAD_BLAST: "matte",
    fin.FINE_SANDING: "matte",
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


def _metal_name(material: Material) -> str:
    fam = material.family
    if fam in _BARE_METALS:
        return fam
    if fam in fin.FERROUS:
        return "steel"
    return "stainless"  # last-resort fallback


def _is_carbon(material: Material) -> bool:
    return "carbon" in (material.grade or "").lower() or material.family == "CFRP"


def _metal_tex_base(material: Material, texture):
    """Bare metal, optionally with a brushed/matte relief variant."""
    name = _metal_name(material)
    return getattr(metal, f"{name}_{texture}")() if texture else getattr(metal, name)()


def _plain_base(material: Material, texture, rgb):
    """Look with no colour finish -- substrate + optional texture."""
    cat = material.category
    if cat == "metal":
        return _metal_tex_base(material, texture)
    if cat == "wood":
        return getattr(wood, material.name.lower())(color=rgb)
    if cat == "glass":
        return glass.glass(color=rgb)
    if cat == "paper":
        return getattr(paper, material.name.lower().replace(" ", "_"))(color=rgb)
    if cat == "textile":
        return getattr(textile, _TEXTILE[material.name])(color=rgb)
    # plastic / composite / resin
    if material.family == "PMMA":
        return plastic.acrylic(color=rgb)
    if cat == "composite":
        fn = plastic.carbon_fiber if _is_carbon(material) else plastic.plastic_rough
        return fn(color=rgb)
    if texture:
        return plastic.plastic_rough(color=rgb)
    return plastic.plastic_clean(color=rgb)


# --- surface (colour) finishes: (material, rgb, texture) -> PbrProperties ---
def _anodized(m, rgb, texture):
    if m.family == "aluminum" and texture is None:
        return metal.aluminum_anodized(color=rgb)  # tuned preset for the common case
    base = _metal_tex_base(m, texture)  # keep relief; scalar recolour
    return base.override(color=rgb, roughness=0.3) if rgb else base


def _pvd(m, rgb, texture):
    if rgb is None:
        return metal.gold()  # PVD default: decorative gold
    if texture:  # keep the brushed/blasted relief
        return _metal_tex_base(m, texture).override(color=rgb, roughness=0.15)
    return coats.metallic_coat_gloss(color=rgb)


def _black_oxide(m, rgb, texture):
    if texture:  # keep the blasted/brushed relief
        return _metal_tex_base(m, texture).override(color="#141414", roughness=0.5)
    return coats.metallic_coat_matte(color="#141414")


def _dyeing(m, rgb, texture):
    if m.family == "aluminum":
        return _anodized(m, rgb, texture)
    return _plain_base(m, texture, rgb)  # dyed polymer: base tinted by colour


def _chrome(m, rgb, texture):
    return coats.chrome()


def _gold(m, rgb, texture):
    return metal.gold()


def _silver(m, rgb, texture):
    return metal.silver()


def _nickel(m, rgb, texture):
    fn = getattr(metal, "nickel", None)  # adopt metal.nickel once bundled
    return fn() if fn else metal.silver().override(color="#b9b9b2")


def _tin(m, rgb, texture):
    return metal.tin()


def _zinc(m, rgb, texture):
    fn = getattr(metal, "zinc", None)  # prefer a real zinc factory if present
    base = fn() if fn else metal.silver_matte()
    return base.override(color=rgb) if rgb else base


def _coat_gloss(m, rgb, texture):
    return coats.coat_gloss(color=rgb)


def _coat_matte(m, rgb, texture):
    return coats.coat_matte(color=rgb)


def _ecoat(m, rgb, texture):
    return coats.coat_matte(color=rgb or "#101010")


_SURFACE = {
    fin.ANODIZED: _anodized,
    fin.PVD: _pvd,
    fin.BLACK_OXIDE: _black_oxide,
    fin.DYEING: _dyeing,
    fin.CHROME_PLATING: _chrome,
    fin.GOLD_PLATING: _gold,
    fin.NICKEL_PLATING: _nickel,
    fin.SILVER_PLATING: _silver,
    fin.TIN_PLATING: _tin,
    fin.ZINC_PLATING: _zinc,
    fin.POWDER_COAT_GLOSS: _coat_gloss,
    fin.POWDER_COAT_MATT: _coat_matte,
    fin.ELECTROPHORESIS: _ecoat,
    fin.SPRAY_PAINT_GLOSS: _coat_gloss,
    fin.SPRAY_PAINT_MATT: _coat_matte,
    fin.VACUUM_PLATING_GLOSS: _coat_gloss,
    fin.VACUUM_PLATING_MATT: _coat_matte,
}
# everything else (smooth machining, electropolished, passivation, pickling,
# chem film, conductive oxidation, laser, etch, silkscreen) leaves the look as-is.


def _normalize(finish):
    """finish -> list of (Finish, colour); unwraps AppliedFinish, tolerates raw Finish."""
    if finish is None:
        return []
    seq = finish if isinstance(finish, (list, tuple)) else [finish]
    out = []
    for f in seq:
        if isinstance(f, AppliedFinish):
            out.append((f.finish, f.color))
        else:  # a raw Finish -> no colour
            out.append((f, None))
    return out


def get_pbr_properties(material: Material, finish=None, process=None, pbr=None):
    """Resolve a bundled three.js ``PbrProperties`` for a finished material.

    ``finish`` is an ``AppliedFinish`` (from a finish function like
    ``spray_paint("blue")``) or a list of them -- each carries its own colour.
    ``process`` (a ``Process``) nudges the default surface (printed -> rough).
    ``pbr`` (if given) is returned unchanged.
    """
    if pbr is not None:
        return pbr

    texture = None
    surface = None
    surface_color = None
    for f, col in _normalize(finish):
        if f in _TEXTURE:
            texture = _TEXTURE[f]
        elif f in _SURFACE:
            surface = f
            surface_color = col
    if texture is None and process in _ROUGH_PROCESSES:
        texture = "matte"  # as-printed / as-built relief

    rgb = _color_value(surface_color)
    if surface is None:
        return _plain_base(material, texture, rgb)
    return _SURFACE[surface](material, rgb, texture)


__all__ = ["get_pbr_properties"]

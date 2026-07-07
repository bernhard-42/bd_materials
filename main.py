"""Self-check / demo:  python main.py"""

from __future__ import annotations

from bd_materials import (
    Process,
    finishes,
    glass,
    metals,
    paper,
    plastics,
    resins,
    textile,
    wood,
)
from bd_materials.materials.metals import Alu

_categories = {
    "metal": metals.ALL_METALS,
    "plastic": plastics.ALL_PLASTICS,
    "resin": resins.ALL_RESINS,
    "glass": glass.ALL_GLASSES,
    "wood": wood.ALL_WOODS,
    "paper": paper.ALL_PAPERS,
    "textile": textile.ALL_TEXTILES,
}
_all = [m for items in _categories.values() for m in items]
print(f"materials: {len(_all)}")
for _cat, _items in _categories.items():
    print(f"  {_cat:8s}: {len(_items)}")

# mass of a 20mm cube (density is a single representative value; V = 8000 mm3)
print("\nmass of a 20mm cube:")
for _fm in (metals.aluminum(), metals.titanium(), plastics.pla(color="black")):
    _m = _fm.material
    print(f"  {_m.name:22s} {_m.mass(8000):6.1f} g")

# a typical-value range dump (print uses the material's __str__)
print("\ntypical values (Alu 7075-T6):")
print(metals.aluminum(Alu.G7075_T6).material)

# --- visualization: FinishedMaterial -> three.js PBR ---------------------------
# Building a FinishedMaterial needs no threejs; only .pbr imports threejs_materials.
_looks = [
    ("aluminium, anodized", metals.aluminum(finish=finishes.anodize("champagne"))),
    (
        "steel, powder-coat",
        metals.mild_steel(finish=finishes.powder_coat("green", matt=True)),
    ),
    ("PLA, red (FDM)", plastics.pla(color="red", process=Process.FDM)),
    ("PMMA, clear 3mm", plastics.pmma(color="clear", thickness_mm=3)),
    ("borosilicate, 5mm", glass.glass(glass.Glass.BOROSILICATE, thickness_mm=5)),
    ("oak", wood.hardwood(wood.Hardwood.OAK)),
]
try:
    print("\nPBR look resolution (FinishedMaterial.pbr):")
    for _label, _look in _looks:
        _v = _look.pbr.to_dict()["values"]
        print(f"  {_label:22s} metal={_v.get('metalness')} rough={_v.get('roughness')}")
except ImportError:
    print("\nPBR demo skipped (threejs_materials not installed)")

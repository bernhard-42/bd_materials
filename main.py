"""Self-check / demo:  python main.py"""

from __future__ import annotations

from bd_materials import (
    canonical_name,
    finishes,
    glass,
    material_names,
    metals,
    paper,
    plastics,
    processes,
    resins,
    resolve,
    textile,
    wood,
)
from bd_materials.materials.metals import Alu

# %%
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

# lookup by name -- the string entry point (part.material = "aluminum")
print(f"\nmaterials reachable by name: {len(material_names())}")
for _name in ("aluminum", "oak", "felt", "Alu_G7075_T6", "mild steel"):
    print(f"  {_name:15s} -> {canonical_name(resolve(_name))}")

# --- visualization: FinishedMaterial -> three.js PBR ---------------------------
# Building a FinishedMaterial needs no threejs; only .pbr imports threejs_materials.
_looks = [
    ("aluminum, anodized", metals.aluminum(finish=finishes.anodize("champagne"))),
    (
        "steel, powder-coat",
        metals.mild_steel(finish=finishes.powder_coat("green", finishes.Sheen.MATTE)),
    ),
    ("PLA, red (FDM)", plastics.pla(color="red", process=processes.fdm())),
    ("PMMA, clear 3mm", plastics.pmma(color="clear", thickness_mm=3)),
    ("borosilicate, 5mm", glass.borosilicate(thickness_mm=5)),
    ("oak", wood.hardwood(wood.Hardwood.OAK)),
]
try:
    print("\nPBR look resolution (FinishedMaterial.pbr):")
    for _label, _look in _looks:
        _v = _look.pbr.to_dict()["values"]
        print(f"  {_label:22s} metal={_v.get('metalness')} rough={_v.get('roughness')}")
except ImportError:
    print("\nPBR demo skipped (threejs_materials not installed)")

# %%
from build123d import *
from ocp_vscode import show

b = Box(20, 20, 10)

b.material = plastics.asa(color="red")  # clean  → plastic()
show(b)
# %%
b.material = plastics.asa(
    color="red", process=processes.fdm(rotation=90)
)  # layers → plastic_fdm(), turned to run parallel to the base plate
show(b)
# %%
b.material = plastics.asa(
    color="red", process=processes.fdm(layer_height_mm=0.1, rotation=90)
)  # finer layers (0.1 mm instead of the authored 0.2)
show(b)
# %%
b.material = plastics.asa(
    color="red", process=processes.sls()
)  # rough → plastic_rough()
show(b)
# %%
b.material = plastics.asa(
    color="red", finish=finishes.fine_sanding()
)  # sanded print → plastic_rough()
show(b)
# %%
from build123d import *
from ocp_vscode import show

b = Box(10, 10, 5)
f = b.faces().sort_by()
b_top = f[-1]
b_bot = f[0]
b_wal = f - [b_top, b_bot]

layers = plastics.asa(color="blue", process=processes.fdm(rotation=90))
b_top.material = plastics.asa(color="blue", process=processes.fdm_skin())
b_bot.material = plastics.asa(color="blue", process=processes.fdm_skin())
for w in b_wal:
    w.material = layers

c = Pos(30, 0, 0) * Cylinder(20, 20)
c_top_bot = c.faces().filter_by(GeomType.PLANE)
c_wal = (c.faces() - c_top_bot)[0]
layers2 = plastics.asa(color="blue", process=processes.fdm())
c_wal.material = layers2

# A sphere's v parameter is latitude in RADIANS, spanning pi whatever the radius, so one
# UV unit is the radius in mm -- without saying so the map reads a fixed ~16 layers on
# any sphere. The box wall and the cylinder lateral are already metric (mm_per_uv=1).
R = 10
s = Pos(0, 40, 0) * Sphere(R)
s_face = s.faces()[0]
s_face.material = plastics.asa(color="blue", process=processes.fdm(mm_per_uv=R))

show(b_bot, b_top, b_wal, c, s_face)

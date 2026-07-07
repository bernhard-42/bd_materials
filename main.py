"""Self-check / demo:  python main.py"""

from __future__ import annotations

from bd_materials import (
    FinishedMaterial,
    IsotropicSolidMaterial,
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

# Category counts -- each module enumerates itself via all(); composites are
# PlasticMaterial with category="composite", so split them out of "plastic".
_plastics = plastics.all()
_categories = {
    "metal": metals.all(),
    "plastic": tuple(m for m in _plastics if m.category == "plastic"),
    "composite": tuple(m for m in _plastics if m.category == "composite"),
    "resin": resins.all(),
    "wood": wood.all(),
    "glass": glass.all(),
    "paper": paper.all(),
    "textile": textile.all(),
}
_all_materials = [m for items in _categories.values() for m in items]

print(f"registered materials: {len(_all_materials)}")
for cat, items in _categories.items():
    print(f"  {cat:10s}: {len(items)}")

# quick demo: mass of a 20mm cube in a few materials
for m in (metals.aluminum(), metals.titanium(), plastics.pla(color="black")):
    print(f"  {m.name:28s} 20mm cube = {m.mass_g_from_volume_mm3(8000):6.1f} g")
_sheet = paper.paper()
print(
    f"  {_sheet.name:28s} A4 sheet  = {_sheet.mass_g_from_area_mm2(210 * 297):6.2f} g"
)

# completeness: density/thermal apply to all; elastic only to isotropic solids
_universal = ["density_kg_m3", "thermal_conductivity_w_mk", "specific_heat_j_kgk"]
_elastic = ["youngs_modulus_pa", "poissons_ratio"]
for f in _universal:
    missing = [m.name for m in _all_materials if getattr(m, f, None) is None]
    print(f"  missing {f:24s}: {len(missing)}" + (f" -> {missing}" if missing else ""))
for f in _elastic:
    missing = [
        m.name
        for m in _all_materials
        if isinstance(m, IsotropicSolidMaterial) and getattr(m, f) is None
    ]
    print(f"  missing {f:24s}: {len(missing)}" + (f" -> {missing}" if missing else ""))


# --- visualization: FinishedMaterial -> three.js PBR ------------------------
# Building a FinishedMaterial needs no threejs; only the .pbr property does.
_looks = [
    ("aluminium, bare", FinishedMaterial(metals.aluminum())),
    (
        "aluminium, anodized",
        FinishedMaterial(metals.aluminum(), finishes.anodize("champagne")),
    ),
    (
        "aluminium, brushed + anodized",
        FinishedMaterial(
            metals.aluminum(), [finishes.brushed(), finishes.anodize("blue")]
        ),
    ),
    (
        "steel, powder-coat matt",
        FinishedMaterial(metals.mild_steel(), finishes.powder_coat("green", matt=True)),
    ),
    (
        "steel, nickel plating",
        FinishedMaterial(metals.mild_steel(), finishes.nickel_plate()),
    ),
    ("PLA, red filament", FinishedMaterial(plastics.pla(color="red"))),
    (
        "PLA, FDM (rough)",
        FinishedMaterial(plastics.pla(color="gray"), process=Process.FDM),
    ),
    ("oak", FinishedMaterial(wood.oak())),
]
try:
    print("\nPBR look resolution (FinishedMaterial.pbr):")
    for label, fm in _looks:
        vals = fm.pbr.to_dict()["values"]
        print(
            f"  {label:32s} metal={vals.get('metalness')} rough={vals.get('roughness')}"
        )
except ImportError:
    print("\nPBR demo skipped (threejs_materials not installed)")

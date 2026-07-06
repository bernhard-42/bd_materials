"""Self-check / demo:  python main.py"""

from __future__ import annotations

from bd_materials import (
    REGISTRY,
    FinishedMaterial,
    Process,
    anodize,
    bead_blast,
    brushed,
    metals,
    nickel_plate,
    plastics,
    powder_coat,
)
from bd_materials.base import IsotropicSolidMaterial

print(f"registered materials: {len(REGISTRY)}")
for cat in (
    "metal",
    "plastic",
    "resin",
    "composite",
    "wood",
    "glass",
    "paper",
    "textile",
):
    print(f"  {cat:10s}: {len(REGISTRY.filter(category=cat))}")

# quick demo: mass of parts in a few materials
for key in ("aluminum-6061-t6", "titanium-ti-6al-4v-gr5-tc4", "pla"):
    m = REGISTRY.get(key)
    if m:
        print(f"  {m.name:24s} 20mm cube = {m.mass_g_from_volume_mm3(8000):6.1f} g")
paper = REGISTRY.get("paper")
if paper:
    print(
        f"  {paper.name:24s} A4 sheet  = {paper.mass_g_from_area_mm2(210 * 297):6.2f} g"
    )

# completeness: density/thermal apply to all; elastic only to isotropic solids
universal = ["density_kg_m3", "thermal_conductivity_w_mk", "specific_heat_j_kgk"]
elastic = ["youngs_modulus_pa", "poissons_ratio"]
for f in universal:
    missing = [m.name for m in REGISTRY.all() if getattr(m, f, None) is None]
    print(f"  missing {f:24s}: {len(missing)}" + (f" -> {missing}" if missing else ""))
for f in elastic:
    missing = [
        m.name
        for m in REGISTRY.all()
        if isinstance(m, IsotropicSolidMaterial) and getattr(m, f) is None
    ]
    print(f"  missing {f:24s}: {len(missing)}" + (f" -> {missing}" if missing else ""))


# --- visualization: FinishedMaterial -> three.js PBR ------------------------
# Building a FinishedMaterial needs no threejs; only .to_pbr_properties() does.
_looks = [
    ("aluminium, bare", FinishedMaterial(metals.ALU_6061_T6)),
    ("aluminium, anodized", FinishedMaterial(metals.ALU_6061_T6, anodize("champagne"))),
    (
        "aluminium, brushed + anodized",
        FinishedMaterial(metals.ALU_6061_T6, [brushed(), anodize("blue")]),
    ),
    (
        "aluminium, bead-blast + anodized",
        FinishedMaterial(metals.ALU_6061_T6, [bead_blast(), anodize("red")]),
    ),
    (
        "steel, powder-coat matt",
        FinishedMaterial(metals.STEEL_1018, powder_coat("green", matt=True)),
    ),
    ("steel, nickel plating", FinishedMaterial(metals.STEEL_1018, nickel_plate())),
    ("PLA, FDM (rough)", FinishedMaterial(plastics.PLA, process=Process.FDM)),
    ("oak", FinishedMaterial(REGISTRY.get("oak"))),
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

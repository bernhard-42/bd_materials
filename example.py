# %%

from build123d import *
from ocp_vscode import *
from ocp_vscode.utils import create_shader_ball
from bd_materials import (
    metals,
    plastics,
    wood,
    glass,
    resins,
    finishes,
    Process,
    typical_finishes,
    typical_materials,
)

sb = create_shader_ball("sb")
set_defaults(studio_env_intensity=0.75, studio_env_rotation=48)
# %%


# %%


## 1 — defaults only: the most common grade, bare surface

m = metals.aluminum()  # 6061-T6
show(sb, materials=[m.pbr])
# %%

m = plastics.pla()  # generic PLA
show(sb, materials=[m.pbr])
# %%

m = wood.hardwood()  # generic hardwood
show(sb, materials=[m.pbr])
# %%


## 2 — pick a grade (grade is first-positional)

m = metals.aluminum(metals.Alu.G7075_T6)
show(sb, materials=[m.pbr])
# %%

m = metals.stainless(metals.Stainless.G316L_AS_BUILT)  # SLM as-built
show(sb, materials=[m.pbr])
# %%

m = wood.hardwood(wood.Hardwood.ASH)
show(sb, materials=[m.pbr])
# %%

m = wood.softwood(wood.Softwood.PINE)
show(sb, materials=[m.pbr])
# %%

m = resins.tough()
show(sb, materials=[m.pbr])
# %%


## 3 — selectable color (plastics/resins/paper/textile) and transparent panes

m = plastics.pla(color="red")
show(sb, materials=[m.pbr])
# %%

m = plastics.pmma(color="clear", thickness_mm=3)  # transparent -> pane thickness
show(sb, materials=[m.pbr])
# %%

m = glass.borosilicate(color="green", thickness_mm=5)
show(sb, materials=[m.pbr])
# %%


## 4 — a finish (color and, for paints/coats, a sheen ride on the finish)

m = metals.aluminum(finish=finishes.anodize("champagne"))  # finish on default grade
show(sb, materials=[m.pbr])
# %%

m = metals.aluminum(metals.Alu.G7075_T6, finishes.anodize("blue"))  # grade + finish
show(sb, materials=[m.pbr])
# %%

m = metals.mild_steel(finish=finishes.powder_coat("green", finishes.Sheen.MATTE))
show(sb, materials=[m.pbr])
# %%

m = metals.brass()
show(sb, materials=[m.pbr])
# %%

m = metals.brass(finish=finishes.pvd("gold"))
show(sb, materials=[m.pbr])
# %%


## 5 — process nudges the *bare* as-made surface (a print reads rough)

m = plastics.pla(color="black", process=Process.FDM)
show(sb, materials=[m.pbr])

# %% compared to

m = plastics.pla(color="black")
show(sb, materials=[m.pbr])
# %%


## 6 — inspect the physics, compute mass, resolve the look

al = metals.aluminum(metals.Alu.G7075_T6)
print(al.material)  # aligned "property  min to max  unit" table

print(f"{al.material.mass(volume_mm3=8000)=}")  # grams  (density x volume)

assert al.material.tensile_strength is not None

print(f"{al.material.tensile_strength=}")  # Range(mi)n=540, max=600  MPa
print(f"{al.material.tensile_strength.value_at(0)=}")  # 540 Pa (min)
print(f"{al.material.tensile_strength.value_at(1)=}")  # 600 Pa (max)
print(f"{al.material.tensile_strength.value_at(0.2)=}")  # 552 Pa (max)

al.pbr  # three.js PbrProperties

# %%

# density is a single representative value -- override it per part (e.g. measured):
al2 = metals.aluminum(metals.Alu.G7075_T6, density=2805)
print(f"{al2.material.density=}  (catalog default {al.material.density})")
print(f"{al2.material.mass(volume_mm3=8000)=}")  # mass reflects the override

# %%

# 7 — advisory applicability queries (never a constraint)

print("Typical finishes for a aluminum:\n")
for tf in typical_finishes(metals.aluminum().material):
    print(f"- {tf.name}")

print("\nTypical materials for a anodizing:\n")
for m in typical_materials(finishes.Chemical.ANODIZED):
    print(f"- {m.name}")


# %%

m = metals.aluminum()
show(sb, materials=[m.pbr])

# %%

m = metals.aluminum(finish=finishes.brushed())
show(sb, materials=[m.pbr])

# %%

m = metals.aluminum(finish=finishes.fine_sanding())
show(sb, materials=[m.pbr])

# %%

m = metals.aluminum(finish=finishes.anodize("#e8723b"))
show(sb, materials=[m.pbr])

# %%

m = metals.aluminum(finish=[finishes.bead_blast(), finishes.anodize("#e8723b")])
show(sb, materials=[m.pbr])

# %%

m = metals.tool_steel(metals.ToolSteel.D2_HARDENED)
show(sb, materials=[m.pbr])

# %%

m = metals.tool_steel(metals.ToolSteel.D2_HARDENED, finish=finishes.brushed())
show(sb, materials=[m.pbr])

# %%

m = metals.tool_steel(
    metals.ToolSteel.D2_HARDENED, finish=[finishes.brushed(), finishes.pvd("red")]
)
show(sb, materials=[m.pbr])

# %%

m = metals.tool_steel(metals.ToolSteel.D2_HARDENED, finish=finishes.black_oxide())
show(sb, materials=[m.pbr])

# %%

m = metals.tool_steel(metals.ToolSteel.D2_HARDENED, finish=finishes.zinc_plate())
show(sb, materials=[m.pbr])

# %%

m = metals.tool_steel(metals.ToolSteel.D2_HARDENED, finish=finishes.anodize("green"))
show(sb, materials=[m.pbr])

# %%
m = metals.tool_steel(
    metals.ToolSteel.D2_HARDENED,
    finish=[finishes.bead_blast(), finishes.anodize("green")],
)
show(sb, materials=[m.pbr])

# %%

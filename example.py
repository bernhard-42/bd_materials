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

## 1 — defaults only: the most common grade, bare surface

sb.material = metals.aluminum()  # 6061-T6
show(sb)
# %%

sb.material = plastics.pla()  # generic PLA
show(sb)
# %%

sb.material = wood.hardwood()  # generic hardwood
show(sb)
# %%


## 2 — pick a grade (grade is first-positional)

sb.material = metals.aluminum(metals.Alu.G7075_T6)
show(sb)
# %%

sb.material = metals.stainless(metals.Stainless.G316L_AS_BUILT)  # SLM as-built
show(sb)
# %%

sb.material = wood.hardwood(wood.Hardwood.ASH, rotation=90)
show(sb)
# %%

sb.material = wood.softwood(wood.Softwood.PINE, scale=(2, 2))
show(sb)
# %%

sb.material = resins.tough()
show(sb)
# %%


## 3 — selectable color (plastics/resins/paper/textile) and transparent panes

sb.material = plastics.pla(color="red")
show(sb)
# %%

sb.material = plastics.pmma(
    color="clear", thickness_mm=3
)  # transparent -> pane thickness
show(sb)
# %%

sb.material = glass.borosilicate(color="green", thickness_mm=5)
show(sb)
# %%


## 4 — a finish (color and, for paints/coats, a sheen ride on the finish)

sb.material = metals.aluminum(
    finish=finishes.anodize("champagne")
)  # finish on default grade
show(sb)
# %%

sb.material = metals.aluminum(
    metals.Alu.G7075_T6, finishes.anodize("blue")
)  # grade + finish
show(sb)
# %%

sb.material = metals.mild_steel(
    finish=finishes.powder_coat("green", finishes.Sheen.MATTE)
)
show(sb)
# %%

sb.material = metals.brass()
show(sb)
# %%

sb.material = metals.brass(finish=finishes.pvd("gold"))
show(sb)
# %%


## 5 — process nudges the *bare* as-made surface (a print reads rough)

sb.material = plastics.pla(color="black", process=Process.FDM)
show(sb)

# %% compared to

sb.material = plastics.pla(color="black")
show(sb)
# %%


## 6 — inspect the physics, compute mass, resolve the look

al = metals.aluminum(metals.Alu.G7075_T6)
print(al.material)  # aligned "property  min to max  unit" table

print(f"{al.material.mass(volume_mm3=8000)=}")  # grams  (density x volume)

assert al.material.tensile_strength is not None

print(f"{al.material.tensile_strength=}")  # Range min=540, max=600  MPa
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

sb.material = metals.aluminum()
show(sb)

# %%

sb.material = metals.aluminum(finish=finishes.brushed())
show(sb)

# %%

sb.material = metals.aluminum(finish=finishes.fine_sanding())
show(sb)

# %%

sb.material = metals.aluminum(finish=finishes.anodize("#e8723b"))
show(sb)

# %%

sb.material = metals.aluminum(
    finish=[finishes.bead_blast(), finishes.anodize("#e8723b")]
)
show(sb)

# %%

sb.material = metals.tool_steel(metals.ToolSteel.D2_HARDENED)
show(sb)

# %%

sb.material = metals.tool_steel(metals.ToolSteel.D2_HARDENED, finish=finishes.brushed())
show(sb)

# %%

sb.material = metals.tool_steel(
    metals.ToolSteel.D2_HARDENED, finish=[finishes.brushed(), finishes.pvd("red")]
)
show(sb)

# %%

sb.material = metals.tool_steel(
    metals.ToolSteel.D2_HARDENED, finish=finishes.black_oxide()
)
show(sb)

# %%

sb.material = metals.tool_steel(
    metals.ToolSteel.D2_HARDENED, finish=finishes.zinc_plate()
)
show(sb)

# %%

sb.material = metals.tool_steel(
    metals.ToolSteel.D2_HARDENED, finish=finishes.anodize("green")
)
show(sb)

# %%
sb.material = metals.tool_steel(
    metals.ToolSteel.D2_HARDENED,
    finish=[finishes.bead_blast(), finishes.anodize("green")],
)
show(sb)

# %%
sb.material = metals.aluminum(
    finish=[finishes.brushed(), finishes.electrophoresis()],
)
show(sb)

# %%
sb.material = metals.tool_steel(
    finish=[finishes.brushed(), finishes.electrophoresis()],
)
show(sb)

# %%

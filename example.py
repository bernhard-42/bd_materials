# %%
from build123d import *
from ocp_vscode import *
from ocp_vscode.utils import create_shader_ball
from bd_ext import *
from bd_materials import metals, plastics, finishes, Process

sb = create_shader_ball("sb")
# %%

m = metals.aluminum(finish=finishes.anodize("orange"))
show(sb, materials=[m.pbr])
# %%

m = metals.mild_steel()
show(sb, materials=[m.pbr])
# %%

m = plastics.pla(color="gray", process=Process.FDM)
show(sb, materials=[m.pbr])

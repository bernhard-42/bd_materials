# %%
from build123d import *
from ocp_vscode import *
from ocp_vscode.utils import create_shader_ball
from bd_ext import *
from bd_materials import metals, plastics, finishes, FinishedMaterial, Process

sb = create_shader_ball("sb")
# %%

m = FinishedMaterial(metals.ALU_6061_T6, finishes.anodize("orange"))
show(sb, materials=[m.pbr])
# %%

m = FinishedMaterial(
    metals.STEEL_1018,
)
show(sb, materials=[m.pbr])
# %%

m = FinishedMaterial(plastics.PLA, process=Process.FDM)
show(sb, materials=[m.pbr])

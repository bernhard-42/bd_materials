# bd_materials

A **typical-values** engineering-materials library for **build123d**: quickly
*provide or compute* physical characteristics of a designed part (mass, stiffness,
stress safety factors, thermal response), name a common material, and resolve how
it *looks* (finish + colour → three.js PBR). GitHub:
`https://github.com/bernhard-42/bd_materials`.

It is **not** a generic/encyclopedic materials database. Every field earns its
place by feeding a calculation or identifying the material. Values are
representative (room-temperature nominal unless noted), seeded from a PCBWay
scrape and backfilled with typical MatWeb-class reference values.

## Working style (important)

- **Simplicity, calc-first.** Lean, purpose-driven fields; no datasheet trivia
  "for completeness." When in doubt, fewer fields.
- The user wants **root causes**, not band-aids; discuss design trade-offs before
  large refactors.
- The user **reviews the data values** himself — flag anything nominal/uncertain.
- Format with **ruff** (line length 88, `target-version = py310`).

## Layout

```
pyproject.toml          setuptools>=81; package = bd_materials; deps: none
                        (viz extra = threejs-materials)
main.py                 self-check / demo:  python main.py
bd_materials/
  base.py               Material, IsotropicSolidMaterial, ArealMaterial;
                        MaterialRegistry + REGISTRY; Category (Literal)
  metals.py             MetalMaterial + 29 metals
  plastics.py           PlasticMaterial + thermoplastics AND composites
  resins.py             7 vendor-neutral resin families
  wood.py               WoodMaterial (orthotropic) + 9 woods
  paper.py / textile.py PaperMaterial / TextileMaterial (both extend ArealMaterial)
  glass.py              one glass (a plain IsotropicSolidMaterial)
  finishes.py           Finish spec + finish FUNCTIONS + AppliedFinish
  finished.py           FinishedMaterial (user touch point) + Process enum
  pbr.py                get_pbr_properties() -- the three.js bridge (needs viz)
inputs/                 OLD PCBWay scrapes; NOT committed, do not depend on them
```

## Type hierarchy (one file per material *class*)

- `Material` — universal: identity + density + thermal + **derived metrics**
  (`thermal_diffusivity_m2_s`, `volumetric_heat_capacity_j_m3k`) + mass helpers.
- `IsotropicSolidMaterial(Material)` — isotropic linear-elastic (E, ν, G, yield,
  UTS) + shear/safety-factor/Hooke methods + specific stiffness/strength. Parents
  `MetalMaterial`, `PlasticMaterial`, and the single glass instance.
- `ArealMaterial(Material)` — grammage goods; `mass_g_from_area_mm2`. Parents
  `PaperMaterial`, `TextileMaterial`.
- `WoodMaterial(Material)` — orthotropic; grain-direction fields; **not** isotropic
  (deliberately never inherits `effective_shear_modulus_pa`, which would be wrong).

`category` is a cross-cutting attribute (composites are `PlasticMaterial` with
`category="composite"`, kept beside their base polymer — not a separate file).

## Key design decisions (the "why")

- **Naming:** grade + temper (`ALU_6061_T6`, `TOOL_STEEL_D2`), never process.
- **`condition`** is a *readable temper/heat-treat tag only* (`"T6"`, `"annealed"`,
  `"quenched & tempered"`, `"hardened"`, `"as-built"`). No numbers in it.
- **`hardness`** is its own metal field (`"58-62 HRC"`, `"197 HB"`) — it used to be
  smuggled into `condition`. Plastics keep `shore_hardness`. Each entry is one
  self-described representative; a different temper is a `.with_overrides(...)` clone.
- **NO `form`/`process` field on materials.** A material can be moulded *or* printed;
  encoding one route is a material→process mapping we rejected (same reason finishes
  don't map material→finish). **Process is a use-time choice.**
- **`continuous_service_temp_c`** (renamed from `max_service_temp_c`); melting dropped
  (no calc used it); `category` is a validated `Literal`.

## Finishes (hidden behind functions)

Finishes are advisory hints, never gates. The **public API is functions**, not the
raw constants:
- colour + gloss/matt: `spray_paint(color, matt=False)`, `powder_coat(...)`,
  `vacuum_plating(...)`.
- colour: `anodize(color=None)`, `dye(color)`, `pvd(color=None)`, `zinc_plate(...)`,
  `silkscreen(...)`, `electrophoresis(...)`.
- no colour: `chrome()`, `gold_plate()`, `nickel_plate()`, `bead_blast()`,
  `brushed()`, `passivate()`, `black_oxide()`, `laser_engrave()`, ...

Each returns an **`AppliedFinish`** = finish + its colour (colour lives in the
finish, not a loose argument). Raw constants (`SPRAY_PAINT_MATT`, …) are
module-internal.

## FinishedMaterial (the user touch point)

```python
from bd_materials import metals, FinishedMaterial, Process
from bd_materials import anodize, brushed, spray_paint

FinishedMaterial(metals.ALU_6061_T6)                          # bare
FinishedMaterial(metals.ALU_6061_T6, anodize("champagne"))
FinishedMaterial(metals.ALU_6061_T6, [brushed(), anodize("blue")])
FinishedMaterial(metals.PLA, process=Process.FDM)             # as-printed → rough
FinishedMaterial(mat, _pbr=my_pbr)                            # explicit override
```

- Fields: `.material` (physics/calc), `.finish` (AppliedFinish or list),
  `.process` (a `Process`), `._pbr` (private override).
- `.pbr` is a **property** returning the resolved three.js `PbrProperties`
  (`_pbr` if given, else derived). `_pbr` and `process` are mutually exclusive.
- **Lazy viz**: `import bd_materials` is threejs-free; only `.pbr` /
  `bd_materials.pbr` import `threejs_materials`.
- `Process` (`FDM, SLS, MJF, SLM, VAT, MOLDED, MACHINED, CAST, WROUGHT`) only nudges
  the default surface: `{FDM,SLS,MJF,SLM}` → rough, else smooth.

## Environment & the threejs-materials dependency

- Run/lint with a **Python 3.10+** env that has `ruff` and (for viz)
  `threejs-materials`. On the original machine that's the `ocp79` uv venv at
  `~/.uv-global/ocp79/.venv/` (`bin/python`, `bin/ruff`). On a new machine, create
  an equivalent env; plain `python main.py` still works and skips the PBR block if
  threejs is absent.
- **`threejs-materials` is a SEPARATE package** (its own repo, edited by its own
  agent — do not modify it from here). `pbr.py` uses `getattr(metal, name, ...)`
  fallbacks so it adopts new bundled factories (steel/titanium/tin/nickel/zinc/
  carbon_fiber all landed that way) with no code change here.

## Status / pending

- Working, ruff-clean, `main.py` runs. Committed on `main`.
- **Pending user review:** the draft metal **hardness values** — a few are nominal
  (e.g. 304/316 HRB, A36) and copper is left blank.
- When split into its own GitHub repo, `bd_materials/` + `pyproject.toml` become the
  root (they currently sit inside a larger `3D-Projects` git repo).

# bd_materials

A **range-based typical-values** engineering-materials library for **build123d**:
quickly *provide or compute* a designed part's characteristics (mass, mechanical
& thermal properties), name a common material, and resolve how it *looks*
(finish + colour -> three.js PBR). GitHub:
`https://github.com/bernhard-42/bd_materials`.

Every property is a **min-max `Range`**, not a single point. Two reasons:

- **No vendor/licensing trap.** A published band ("6061-T6 tensile ~290-320 MPa")
  is textbook common knowledge; a single precise figure copied from a datasheet
  is the thing that carries provenance/licensing risk.
- **Honesty about variation.** Real values scatter with temper, heat-treatment,
  product form, and (for AM) process. A range states that spread.

(This replaced an earlier single-point-value design; the point-value modules are
preserved in the `checkpoint:` commit `7a7852b` in history.)

## Working style (important)

- **Simplicity, honest data.** Lean, purpose-driven fields. When in doubt, fewer.
- The user wants **root causes**, not band-aids; discuss trade-offs before large
  refactors.
- The user **reviews the data values** himself -- flag anything nominal/derived.
- Format/lint with **ruff** (line length 88, `target-version = py310`); type-check
  with **ty** (Astral), not mypy/pyright. On the original machine the toolchain
  lives in the `ocp79` uv venv at `~/.uv-global/ocp79/.venv/`.

## Layout

Repo root is `~/Development/CAD/bd_materials/` (its own `.git`).

```
pyproject.toml   setuptools; package = bd_materials; deps: none (viz extra = threejs-materials)
main.py          self-check / demo:  python main.py
bd_materials/
  core.py        SHARED core: Range, NOT_SUITABLE, PROPERTY_UNITS, Category/
                 ALLOWED_CATEGORIES, FERROUS + substrate groupings, RangeMaterial
                 mixin + Solid/Polymer/Areal bases
  finishes.py    Finish catalog (5 process-group enums + <GROUP>_FINISHES dicts) +
                 flat verb functions + AppliedFinish + Sheen
  applicability.py  material<->finish TYPICAL_SUBSTRATES table + typical_finishes /
                 typical_materials queries (advisory)
  finished.py    FinishedMaterial (user touch point) + Process enum
  pbr.py         get_pbr_properties() -- the three.js bridge (needs viz)
  materials/     the category catalogs (re-exported at the package top level)
    metals.py    MetalMaterial   + 31 metals   (Alu/Stainless/MildSteel/... enums)
    plastics.py  PlasticMaterial + 24 plastics (PLA/ABS/Nylon/Peek/TPU/PC/.../CFRP)
    resins.py    ResinMaterial   + 7 resins    (Resin enum; uses shore_hardness)
    glass.py     GlassMaterial   + 2 glasses   (Glass: soda-lime, borosilicate)
    wood.py      WoodMaterial    + 12 woods    (Hardwood/Softwood/EngineeredWood)
    paper.py     PaperMaterial   + 3           (Paper/Cardboard/Foamboard; areal)
    textile.py   TextileMaterial + 3           (Textile: woven, felt, leather)
```

`materials/` is a subpackage re-exported at the top level, so both
`from bd_materials import metals` and `from bd_materials.materials import metals`
(and `from bd_materials.materials.metals import Alu`) work.

## Material model

Each category has its own frozen dataclass `<Cat>Material(RangeMaterial)` holding
the **physics ranges + intrinsic identity**. `RangeMaterial` (in `core.py`) provides
`mass(volume_mm3)`, a `__str__` range-table dump, and the type contract for the
identity fields:

- `name` (identifier) and `density` (the one universal single-value property).
- `category` -- a `ClassVar[str]` fixed per class ("metal", "plastic", ...),
  **validated** against `ALLOWED_CATEGORIES` in `RangeMaterial.__init_subclass__`
  (a typo'd category raises at import).
- `family` -- the PBR/identity key (e.g. "aluminum", "PLA", "oak", "fabric_weave").
- `transparent: bool` -- intrinsic see-through (glass, PMMA, PC, clear resin).

The base hierarchy in `core.py` factors the shared property fields:
`RangeMaterial` -> `SolidMaterial` (metals, glass, polymers) -> `PolymerMaterial`
(plastics, resins); `RangeMaterial` -> `ArealMaterial` (paper, textile); `WoodMaterial`
stands alone. Property fields differ per category (metals have `melting_temperature`
+ `hardness`+`hardness_scale`; plastics swap in `glass_transition_temperature`,
`heat_deflection_temperature`, `elongation_at_break`; resins use a fixed-scale
`shore_hardness`; wood is orthotropic-collapsed-to-along-grain with
`modulus_of_rupture`/`compressive_strength_parallel`/`janka_hardness`; paper/textile
are areal with `areal_density`+`thickness`). **One** `PROPERTY_UNITS` dict in
`core.py` maps every property name across all categories to its unit **and** fixes
the display order; `__str__` iterates it, rendering property fields and skipping
identity.

A `Range` field may also be **`None`** (value *missing*) or **`NOT_SUITABLE`**
(`Range(nan, nan)` -- property *does not apply*, e.g. an elastomer's yield, PTFE's
Tg, a laminate's isotropic yield). `__str__` prints `missing` / `n/a`.

## Catalog structure (how materials are declared)

Uniform per family: a grade **enum** `<Xxx>`, a public inline **dict**
`<XXX>_MATERIALS` keyed by that enum, and a **family function** `<xxx>(grade=...)`.
Single-variant families still get a one-member enum (future-proof). Material `name`
follows `Enum_MEMBER` (e.g. `Nylon_PA6`, `Hardwood_OAK`) so the many `GENERIC`
members stay distinguishable. `ALL_<CATEGORY>` derives from the dicts' `.values()`.

```python
class Alu(Enum):
    G6061_T6 = auto(); G7075_T6 = auto(); ...

ALU_MATERIALS: dict[Alu, MetalMaterial] = {
    Alu.G6061_T6: MetalMaterial(name="Alu_G6061_T6", density=2700, ...),
    ...
}

def aluminum(grade=Alu.G6061_T6, finish=None, process=None) -> FinishedMaterial:
    return FinishedMaterial(ALU_MATERIALS[grade], finish, process=process)
```

To add a grade: one enum member + one dict entry. To add a type: a new `<Xxx>`
enum + `<XXX>_MATERIALS` dict + one `<xxx>()` function.

## Access API (enum + family functions -> FinishedMaterial)

```python
from bd_materials import metals, plastics, glass, wood, finishes, Process
from bd_materials.materials.metals import Alu
from bd_materials.materials.wood import Hardwood

metals.aluminum()                                  # 6061 default -> FinishedMaterial
metals.aluminum(Alu.G7075_T6, finishes.anodize("champagne"))
plastics.pla(color="red")                          # selectable colour (case 2)
plastics.pmma(color="clear", thickness_mm=3)       # transparent -> pane thickness
glass.glass(glass.Glass.BOROSILICATE, color="green", thickness_mm=5)
wood.hardwood(Hardwood.OAK)                         # family fn + grade (was oak())

print(metals.aluminum().material)                  # typical-value range dump (__str__)
metals.aluminum().pbr                              # resolved three.js look
```

Family functions take `(grade=<default>, [color], [thickness_mm], finish=None,
process=None)` and return a **`FinishedMaterial`**. Grade is first-positional, so a
finish on the default grade needs the `finish=` keyword. `color`/`thickness_mm` are
present only where meaningful (selectable-colour / transparent families). Each module
also exposes `<Cat>Material`, its grade enum(s), the `<XXX>_MATERIALS` dict(s), and
`ALL_<CATEGORY>`.

Function names per category: metals `aluminum/stainless/mild_steel/alloy_steel/
spring_steel/tool_steel/titanium/brass/copper/magnesium`; plastics `pla/abs_/nylon/
peek/tpu/pc/pp/pom/ptfe/pmma/pe/phenolic/rubber/petg/pps/fr4/cfrp`; resins `resin`;
glass `glass`; wood `hardwood/softwood/engineered_wood`; paper `paper/cardboard/
foamboard`; textile `textile`.

## Colour / appearance model (the "why")

Three colour cases, split by **where the colour lives**:

1. **Fixed intrinsic** (metals, wood, corrugated cardboard) -- no `color` param;
   the look is derived from `family` in PBR.
2. **Selectable intrinsic** (plastics, resins, textile, paper, foamboard, optional
   glass) -- a `color=` param that lands on the `FinishedMaterial`.
3. **Finish colour** (paint/powder/anodize/dye/...) -- carried by the `AppliedFinish`.
   Precedence: finish colour > selected colour > intrinsic.

**Intrinsic-vs-per-part rule:** intrinsic facts (`family`, `category`,
`transparent`) live on the `Material`; per-part choices (`color`, `thickness_mm`,
`finish`, `process`) live on the `FinishedMaterial`. So the range tables stay pure
typical-values.

## FinishedMaterial

`FinishedMaterial(material, finish=None, *, color=None, thickness_mm=None,
process=None, pbr=None)`. `.material` = physics; `.pbr` = look (lazy-imports
`threejs_materials`, so `import bd_materials` stays viz-free).

- **`finish` and `process` are mutually exclusive** (`ValueError`): a finish
  defines the surface, so a process (the raw as-made surface, e.g. FDM rough) is
  ignored. (A spray-painted print is sanded first, so it's smooth -- realistic.)
- `pbr=` is a full override, mutually exclusive with the rest.
- `process` only nudges the *bare* surface: `{FDM, SLS, MJF, SLM}` -> rough.

## Finishes & applicability

A `Finish` is **intrinsic spec only** (`name`, `colors` palette, `notes`). Finishes
are grouped by process into enums -- `Mechanical`, `Chemical`, `MetalPlating`,
`Coating`, `Marking` -- each backed by a `<GROUP>_FINISHES` dict (the maintenance
backbone). The **public API is the flat verb functions** (`anodize("blue")`,
`powder_coat(...)`), which bind per-part appearance to a finish and return an
`AppliedFinish`.

Two per-part appearance choices ride on the `AppliedFinish` (not the `Finish`):

- `color` -- from `STANDARD_COLORS` (or `CUSTOM`). `"natural"`/`"clear"` map to *no
  tint* in PBR (the factory/substrate look), not a grey.
- `sheen` -- `Sheen.GLOSS` (default) / `Sheen.MATTE`, meaningful for paints/coats
  (`powder_coat`, `spray_paint`, `vacuum_plating`); drives PBR roughness.

Colour is honest per finish: **mandatory** where the finish is defined by it (`dye`,
`powder_coat`, `spray_paint`, `vacuum_plating`, `anodize`); a **sensible default**
where a natural look exists (`pvd="clear"`, `zinc_plate="clear"`, `silkscreen="black"`);
**absent** where fixed (`electrophoresis` is always black; plating colours are inherent).

**Applicability is a separate concern**, in `applicability.py`: one central
`TYPICAL_SUBSTRATES` table (finish enum -> the `category`/`family` substrate keys it is
typically used on) read by two advisory queries -- `typical_finishes(material)` and
`typical_materials(finish)` (no candidate arg; it sees the whole catalog via
`materials.ALL_MATERIALS`). Advisory only: any finish may be applied to any material.

## PBR bridge (pbr.py)

`get_pbr_properties(material, finish, process, color, thickness_mm)` dispatches on
`material.category`, keys metal/wood/paper/textile factories off `material.family`
(falling back for grades three.js doesn't bundle, e.g. pine -> spruce), uses
`material.transparent` + `thickness_mm` for transmissive looks, and treats
`family == "CFRP"` as the carbon-fibre look (CF-filled filaments render as plastic).

- **`threejs-materials` is a SEPARATE package** (its own repo/agent -- do not edit
  from here). `pbr.py` uses `getattr(...)` fallbacks to adopt new bundled factories.
- Plain `python main.py` skips the PBR block if `threejs-materials` is absent.

## Status / pending

- Working, ruff-clean, `ty`-clean, `main.py` runs. 82 materials across 7 categories;
  26 finishes across 5 process groups.
- On **`main`** (the range-based library is canonical; the point-value library lives
  on in checkpoint commit `7a7852b`).
- **Pending review (user reviews values):** the wood/paper/textile bands are the
  roughest; several derived values across families (shear strengths, tool-steel
  yields, resin/glass thermal bands) are estimates. Also spot-check the intrinsic
  colour defaults (paper/foamboard "white", cardboard fixed kraft).
- **Not yet tracked:** `inputs/` (PCBWay source-taxonomy YAML) and `new-concept/`
  (a superseded exploration) are untracked; decide per-file whether to commit.
```

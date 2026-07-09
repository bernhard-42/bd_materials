# bd_materials

---

**!!! ALPHA - DO NOT USE YET !!!**

---

Typical-value engineering materials — give a part a named material, get its **mass and mechanical/thermal properties**, and resolve how it **looks** (finish + colour → three.js PBR).

```python
from bd_materials import metals, finishes

part = metals.aluminum(metals.Alu.G7075_T6, finishes.anodize("champagne"))
part.material.mass(volume_mm3=8000)   # grams
part.material                         # print -> typical-value range table
part.pbr                              # three.js material for OCP VSCode
```

---

## 1. Purpose

bd_materials is **not a materials database**. It is an _opinionated, curated_ list of the common materials you actually reach for in mechanical/CAD design, with **typical-value ranges** for the properties and a single representative **density**.

> ### ⚠️ Disclaimer — read this
>
> - **Typical values only.** Every mechanical/thermal property is a **min–max `Range`**, not a guaranteed spec. Even `density` is a _single representative value_, not exact.
> - **Real products can fall outside the range.** Temper, heat treatment, product form, process (esp. additive), fillers and supplier variation all shift the numbers. The bands are _common-knowledge_ typical figures — cross-checked, but approximate.
> - **For the early design phase.** Use it for sizing, material selection, mass estimates and visualisation. **In detailed design, use the actual product's data sheet.**
> - A property may be **`None`** (value not filled in) or **`NOT_SUITABLE`** (`Range(nan, nan)` — the property does not apply, e.g. an elastomer's yield strength).
> - The `family` tag drives the _look_ (PBR), not the physics. Where three.js lacks a dedicated factory it falls back to the nearest look (e.g. pine → spruce).

---

## 2. Materials & finishes — organised by manufacturing process

The taxonomy follows how parts are actually **made** and **finished**, not an abstract chemistry tree.

### Materials — 7 categories, grouped into families (grade enums)

| Category   | Families (grade enums)                                                                                                                   | Grades |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| `metals`   | `Alu`, `Stainless`, `MildSteel`, `AlloySteel`, `ToolSteel`, `SpringSteel`, `Titanium`, `Brass`, `Copper`, `Magnesium`                    | 33     |
| `plastics` | `PLA`, `ABS`, `Nylon`, `Peek`, `TPU`, `PC`, `PP`, `POM`, `PTFE`, `PMMA`, `PE`, `Phenolic`, `Rubber`, `PETG`, `PPS`, `FR4`, `CFRP`, `Asa` | 26     |
| `resins`   | `Resin` (standard / tough / high-temp / ceramic / castable / esd / transparent / flexible)                                               | 8      |
| `glass`    | `Glass` (soda-lime, borosilicate)                                                                                                        | 2      |
| `wood`     | `Hardwood`, `Softwood`, `EngineeredWood`                                                                                                 | 12     |
| `paper`    | `Paper`, `Cardboard`, `Foamboard`                                                                                                        | 3      |
| `textile`  | `Textile` (woven, felt, leather)                                                                                                         | 3      |

Grades encode the **condition** that governs properties — e.g. `Alu.G7075_T6` (temper), `Stainless.G316L_AS_BUILT` (SLM as-built) vs `G316L_ANNEALED` (wrought), `Nylon.PA12_SINTERED` (SLS/MJF powder). Same alloy, different process → different grade.

### Finishes — grouped by process family

| Group (`finishes.…`) | Finishes                                                                      |
| -------------------- | ----------------------------------------------------------------------------- |
| Mechanical           | bead blast, brushed, fine sanding, smooth machining, electropolish            |
| Chemical             | anodize, chem film, conductive oxidation, black oxide, passivate, pickle, dye |
| Metal plating        | chrome, gold/nickel/silver/tin plate, PVD, zinc plate, vacuum plating         |
| Coating              | powder coat, spray paint, electrophoresis                                     |
| Marking              | laser engrave, etch, silkscreen                                               |

Finishes are **advisory hints, not gates** — any finish may be applied to any material.
The `applicability` module answers "which finish typically suits which material" without restricting.

---

## 3. Public API — from defaults to sophisticated

Every family function returns a **`FinishedMaterial`**: `.material` is the physics, `.pbr` is the look.

```python
from bd_materials import metals, plastics, glass, wood, finishes, Process
```

```python
# 1 — defaults only: the most common grade, bare surface
metals.aluminum()                       # 6061-T6
plastics.pla()                          # generic PLA
wood.hardwood()                         # generic hardwood

# 2 — pick a grade (grade is first-positional)
metals.aluminum(metals.Alu.G7075_T6)
metals.stainless(metals.Stainless.G316L_AS_BUILT)   # SLM as-built
wood.hardwood(wood.Hardwood.OAK)
resins.resin(resins.Resin.TOUGH)

# 3 — selectable colour (plastics/resins/paper/textile) and transparent panes
plastics.pla(color="red")
plastics.pmma(color="clear", thickness_mm=3)        # transparent -> pane thickness
glass.glass(glass.Glass.BOROSILICATE, color="green", thickness_mm=5)

# 4 — a finish (colour and, for paints/coats, a sheen ride on the finish)
metals.aluminum(finish=finishes.anodize("champagne"))          # finish on default grade
metals.aluminum(metals.Alu.G7075_T6, finishes.anodize("blue")) # grade + finish
metals.mild_steel(finish=finishes.powder_coat("green", finishes.Sheen.MATTE))
metals.brass(finish=finishes.pvd("gold"))

# 5 — process nudges the *bare* as-made surface (a print reads rough)
plastics.pla(color="black", process=Process.FDM)
#   note: finish and process are mutually exclusive (a finished part is smooth)

# 6 — inspect the physics, compute mass, resolve the look
al = metals.aluminum(metals.Alu.G7075_T6)
print(al.material)                      # aligned "property  min to max  unit" table
al.material.mass(volume_mm3=8000)       # grams  (density x volume)
al.material.tensile_strength            # Range(min=540, max=600)  MPa
al.pbr                                  # three.js PbrProperties

# 7 — advisory applicability queries (never a constraint)
from bd_materials import typical_finishes, typical_materials
typical_finishes(metals.aluminum().material)         # [Anodized, Bead Blast, ...]
typical_materials(finishes.Chemical.ANODIZED)        # [Alu_G6061_T6, ..., Titanium_...]
```

Grade enums live on their module (`metals.Alu`, `glass.Glass`, …) or import directly: `from bd_materials.materials.metals import Alu`.

---

## 4. Material classes

Shared primitives live in **`bd_materials.core`**:

- **`Range(min, max)`** — a closed typical-value band; `Range.value_at(r)` samples it (`0` → min, `1` → max). **`NOT_SUITABLE`** = `Range(nan, nan)` (property N/A).
- **`PROPERTY_UNITS`** — the single unit + display-order table spanning all categories.
- **`Category`** / **`ALLOWED_CATEGORIES`** — the material taxonomy, validated per class.
- **`RangeMaterial`** — mixin giving `mass(volume_mm3)`, a pretty `__str__`, and the identity fields `name`, `density`, `category`, `family`, `transparent`.

Each category is a frozen dataclass with the physics-range fields relevant to it:

| Class                               | Category-specific fields (beyond the shared solid ranges)                                                                                    |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `MetalMaterial`                     | `yield_strength`, `shear_strength`, `hardness`(+`hardness_scale`), `melting_temperature`                                                     |
| `PlasticMaterial`                   | `yield_strength`, `shear_strength`, `elongation_at_break`, `glass_transition_temperature`, `heat_deflection_temperature`, `hardness`(+scale) |
| `ResinMaterial`                     | same as plastic (`hardness_scale` = Shore D rigid / Shore A flexible)                                                                        |
| `GlassMaterial`                     | `hardness`(+scale, HV), `glass_transition_temperature`, `melting_temperature` (no yield — brittle)                                           |
| `WoodMaterial`                      | along-grain `modulus_of_elasticity`, `modulus_of_rupture`, `compressive_strength_parallel`, `janka_hardness`                                 |
| `PaperMaterial` / `TextileMaterial` | areal goods: `areal_density` (grammage), `thickness`, in-plane `tensile_strength`                                                            |

Intrinsic facts (`family`, `category`, `transparent`) live on the **`Material`**; per-part choices (`color`, `thickness_mm`, `finish`, `process`) live on the **`FinishedMaterial`**:

```
FinishedMaterial(material, finish=None, *, color=None, thickness_mm=None,
                 process=None, pbr=None)
    .material   # the physics (a shared, immutable range table)
    .pbr        # the resolved three.js look (for the OCP VSCode viewer)
```

Each category module also exposes its `<Cat>Material` class, its grade enum(s), a public `<FAMILY>_MATERIALS` dict per family, and an `ALL_<CATEGORY>` tuple.

---

## 5. Finish classes

In **`bd_materials.finishes`**:

- **`Finish`** — a finish's intrinsic spec: `name`, `colors` (its standard palette), `notes`.
- **`Sheen`** — `GLOSS` (default) / `MATTE`, a per-application choice for paints/coatings.
- **`AppliedFinish`** — a `Finish` plus the per-part `color` and `sheen`. This is what the verb functions return and what `FinishedMaterial(finish=…)` accepts.
- Group enums (`Mechanical`, `Chemical`, `MetalPlating`, `Coating`, `Marking`) + their `<GROUP>_FINISHES` dicts are the maintenance backbone; the **verb functions are the API**.

Colour is handled per finish:

- **Mandatory** where the finish is defined by colour — `anodize(color)`, `dye(color)`, `powder_coat(color, sheen=…)`, `spray_paint(...)`, `vacuum_plating(...)`.
- **Sensible default** where a natural look exists — `pvd("clear")`, `zinc_plate("clear")`, `silkscreen("black")`. `"clear"`/`"natural"` render the bare substrate (no tint).
- **None** where fixed/inherent — `chrome()`, `gold_plate()`, `electrophoresis()` (black), and the mechanical finishes (`bead_blast()`, `brushed()`, …).

`finish` and `process` are **mutually exclusive** on a `FinishedMaterial`: a finish defines the surface, so the raw as-made process texture is moot (a spray-painted print is sanded first, hence smooth).

The material↔finish _applicability_ relation lives in **`bd_materials.applicability`** as one central table with two advisory queries — `typical_finishes(material)` and `typical_materials(finish)`.

---

## Install & environment

_Not on pypi yet_

```bash
pip install -e .
```

The one runtime dependency is **`threejs-materials`** — a pure-Python library that renders the predefined materials without MaterialX. `FinishedMaterial.pbr` yields a three.js material for the OCP VSCode viewer. Python 3.10+; format/lint with **ruff** (line length 88), type-check with **ty** (Astral).

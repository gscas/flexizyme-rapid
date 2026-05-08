---
name: flexizyme-rapid
description: |
  Flexizyme/RaPID system for macrocyclic peptide discovery using mRNA display with non-canonical amino acids.
  Covers Hiroaki Suga's artificial ribozyme (flexizyme) catalyzed tRNA aminoacylation and the RaPID
  (Random non-standard Peptide Integrated Discovery) selection platform.
  Use when: (1) Designing flexizyme reactions for non-canonical amino acid charging,
  (2) Setting up RaPID selection campaigns for macrocyclic peptide hit discovery,
  (3) Choosing cyclization strategies for macrocyclic peptides (thioether, head-to-tail, etc.),
  (4) Selecting NCAAs (non-canonical amino acids) for RaPID libraries,
  (5) Planning counter-selection and enrichment strategies,
  (6) Optimizing hit peptides from RaPID screens,
  (7) Converting RaPID hits to drug candidates (stability, membrane permeability, in vivo),
  (8) Comparing RaPID with other display technologies (phage, DNA-encoded, OBOC).
---

# Flexizyme/RaPID — Macrocyclic Peptide Discovery by mRNA Display

## System Overview

**RaPID (Random non-standard Peptide Integrated Discovery)** combines:
1. **Flexizyme** — artificial ribozyme charging tRNA with NCAAs
2. **mRNA display** — genotype-phenotype linkage via puromycin
3. **In vitro translation** — cell-free (PURE/Wheat germ/E. coli S30) with reprogrammed genetic code
4. **Macrocyclization** — in-translation cyclization via reactive NCAA
5. **Selection** — binding/enzymatic assays with counter-selection

**Key advantage over phage/DNA-encoded libraries:** Incorporates NCAAs enabling thioether macrocyclization, N-methylation, and other stabilizing modifications directly during selection — not just post-screening.

## Workflow 1: Flexizyme Selection & Reaction Setup

### Four Flexizyme Variants

| Flexizyme | Aminoacyl substrate scope | Key recognition motif | Typical conc. |
|---|---|---|---|
| **dFx** (dinitro-Fx) | Aromatic esters (CME, CBT) | Aromatic ring + electron-withdrawing leaving group | 1–5 mM acyl-donor |
| **eFx** (enhanced-Fx) | Aromatic esters + acyl-CoA thioesters | Aromatic ring (broader than dFx) | 1–5 mM |
| **aFx** (amino-Fx) | Aminoacyl-adenylates (2,3-DNB-ester) | Free α-amine tolerated | 1–5 mM |
| **tFx** (tRNA-Fx) | Pre-charged acyl-tRNA mimic | Minimal — highest substrate generality | 0.5–2 mM |

### Reaction Protocol

```
1. Prepare flexizyme (25 µM) + tRNA (25 µM) in 50 mM HEPES-KOH pH 7.5
2. Denature at 95°C 1 min → slow cool to RT (anneal)
3. Add acyl-donor substrate (1–5 mM final) in DMSO (≤20% v/v)
4. Incubate on ice: dFx/eFx 2–6h, aFx 30 min–2h, tFx varies
5. Quench: add 0.1 vol 1.5 M NaOAc pH 5.2
6. Acidic PAGE or RP-HPLC to confirm charging
7. Ethanol precipitate, dissolve in translation buffer
```

### Substrate Compatibility Table

Read [references/flexizyme_substrate_table.md](references/flexizyme_substrate_table.md) for the complete list of validated acyl-donor substrates organized by flexizyme type, including:
- Aromatic amino acids (Phe/Tyr/Trp analogs)
- Aliphatic amino acids (via aFx/tFx)
- N-methyl amino acids (N-Me-AA-CME for dFx)
- α,α-disubstituted amino acids
- D-amino acids
- Special warheads (chloroacetyl for thioether, alkyne for click, etc.)

### Decision Tree

```
Is the acyl-donor an activated ester with aromatic ring?
├── Yes → dFx (CME/CBT ester) or eFx (thioester)
│   └── Contains free α-amine? → aFx instead
├── No (aliphatic, β-AA, D-AA, complex warhead)
│   ├── Can make 2,3-DNB-ester? → aFx
│   └── Can make acyl-tRNA mimic? → tFx
└── N-methyl amino acid?
    └── N-Me-AA-CME → dFx (well-validated)
```

## Workflow 2: RaPID Library Construction

### mRNA Library Design

| Parameter | Typical range | Considerations |
|---|---|---|
| Random region | 4–15 codons | Longer → more chemical space, lower per-sequence coverage |
| Codon scheme | NNB or NNS | NNB reduces stop codons (1/48 vs 3/64) |
| Fixed flanking | Start codon + linker | AUG-(NNB)n-UAG (UAG reassigned to NCAA) |
| Library size | 10¹²–10¹⁴ unique | Limited by ligation efficiency, not diversity |

### Genetic Code Reprogramming

Assign UAG (amber) stop codon to NCAA-charged tRNA<sub>CUA</sub>:

```
Standard codon → Standard AA    (tRNA supplied by PURE/wheat germ)
UAG            → NCAA           (via flexizyme-charged tRNA_CUA)
UGG            → N-methyl-Trp   (optional: reassign Trp codon for N-Me)
```

For multiple NCAAs, use 4-base codon (AGGA, CCCU, etc.) or quadruplet codons:
- **Dual reprogramming**: UAG → NCAA1, AGGA → NCAA2
- **Triple**: Add CCCU → NCAA3 (lower efficiency)

### Puromycin Linker

```
mRNA — (PEG)n — Puromycin
            ↕
     Cell-free translation
            ↓
   Peptide-puromycin-mRNA fusion (cDNA after RT)
```

- PEG spacer: typically (PEG)₃ or (PEG)₅
- Ligation: T4 RNA ligase or splint ligation
- RT step: SuperScript III/IV after translation, before selection

## Workflow 3: Macrocyclization Strategies

### In-Translation Cyclization (Preferred)

| Type | NCAA warhead | Cys position | Ring size | Notes |
|---|---|---|---|---|
| **Thioether** | ClAc-AA (chloroacetyl) | Cys | 4–20 aa | Most common; Suga lab standard |
| **Thioether** | BrAc-AA | Cys | 4–20 aa | Faster kinetics than ClAc |
| **Lactam** | Glu/Asp side chain | Lys/Orn | Variable | No Cys required; may need protecting group |
| **Head-to-tail** | N-terminal ClAc | C-terminal Cys | Variable | Spontaneous after translation |
| **Trifluoromethylthio** | CF₃S-AA | Cys | — | Novel; limited validation |
| **Disulfide** | None (2× Cys) | — | Variable | Redox-sensitive; rarely used in RaPID |

**Standard thioether cyclization:**
1. Incorporate ClAc-AA at N-terminus (via flexizyme-tRNA initiating at AUG or reassigned codon)
2. Place Cys at desired cyclization position
3. Cyclization occurs spontaneously during/after translation
4. Side reaction: ClAc can react with Lys/His — control with pH 7.0–7.5

### Post-Translation Cyclization

For lactam, click chemistry, or other strategies where in-translation cyclization isn't feasible.

## Workflow 4: Selection & Enrichment

### Standard RaPID Selection Cycle

```
Round 1: Library (~10¹²) → Target immobilized → Wash → Elute → RT-PCR → Next round
Round 2–4: Enrich, add stringency (shorter wash, competitor)
Round 5–8: Deep sequencing analysis, clone individual hits
```

### Counter-Selection Strategies

| Strategy | When to use | Implementation |
|---|---|---|
| **Negative selection** | Remove non-specific binders | Pre-incubate library with immobilized negative target (tag-only, irrelevant protein) |
| **Competitive elution** | Select for specific binding site | Elute with soluble target or known ligand |
| **Off-rate selection** | Enrich slow off-rate binders | Extended wash steps (1–24h) |
| **Affinity thresholding** | Target Kd range | Titrate immobilized target concentration |

### Immobilization Methods

| Method | Pros | Cons |
|---|---|---|
| **Biotin-streptavidin** | Strong, reversible (biotin) | Streptavidin non-specific binding |
| **His-tag/Ni-NTA** | Convenient, common | Ni²⁺ leaching, histidine-rich hits |
| **FLAG-tag/anti-FLAG** | Specific | Antibody cost |
| **Direct adsorption** | Simple | Denaturation risk |
| **Click chemistry** | Site-specific | Requires azide/alkyne modification |

### Enrichment Monitoring

- qPCR of eluted cDNA after each round
- Expect 10–100× enrichment per round for good targets
- Deep sequence after round 3–5 to identify convergence
- Plateau by round 6–8 typically

## Workflow 5: Hit Validation & Optimization

### Primary Validation

1. **Resynthesis** — SPPS or recombinant expression of top 10–50 sequences
2. **Binding affinity** — SPR/ITC/MST for Kd determination
3. **Specificity** — Panel of related/unrelated proteins
4. **Sequence alignment** — Identify consensus motifs

### Optimization Strategies

| Direction | Method | Typical improvement |
|---|---|---|
| **Affinity** | Alanine scan, truncated library, focused library | 10–100× |
| **Stability** | N-methylation, D-amino acid substitution, PEGylation | Serum t₁/₂: min → hours |
| **Permeability** | N-methylation pattern, reduce HBD, macrocycle rigidity | PAMPA: 0 → measurable |
| **Solubility** | Add charged residues, reduce hydrophobicity, PEG |μg/mL range |
| **Selectivity** | Counter-selection in subsequent RaPID rounds | Off-target reduced 10–100× |

### From Hit to Lead

Read [references/hit_to_lead.md](references/hit_to_lead.md) for the detailed conversion roadmap including:
- SPPS resynthesis protocols for macrocyclic peptides
- Serum stability assay (human/mouse/rat)
- Cell permeability assays (PAMPA, Caco-2, cellular target engagement)
- In vivo PK/PD considerations for macrocyclic peptides
- Patent landscape (Suga IP, Takeda license, PeptiDream)

## Workflow 6: Comparison with Alternative Display Technologies

| Feature | RaPID | Phage Display | DNA-Encoded Library (DEL) | OBOC |
|---|---|---|---|---|
| Library size | 10¹² | 10⁹ | 10⁶–10⁸ | 10⁶–10⁷ |
| NCAA incorporation | ✅ Extensive | ❌ Limited (auxotroph) | ✅ Some (split-pool) | ✅ Full |
| Macrocyclization | ✅ In-selection | ❌ Post-screen | ✅ Some | ✅ Full |
| N-methylation | ✅ | ❌ | Limited | ✅ |
| Membrane targets | ✅ (detergent-compatible) | Limited | ❌ | ✅ |
| Throughput | 1–4 weeks/screen | 1–2 weeks | 1–2 weeks | 2–4 weeks |
| IP landscape | Suga/Takeda/PeptiDream | Broad | Broad | Moderate |

## Workflow 7: Target-Specific Considerations

### PPI Targets (Protein-Protein Interaction)

- Prefer longer libraries (8–15 mer) with thioether cyclization
- N-methyl scan post-hit to improve permeability
- Consider dual-macrocycle strategy for large interfaces

### Enzyme Active Sites

- Shorter libraries (4–8 mer) can suffice
- Include electrophilic warheads (Michael acceptor, boronic acid) via NCAA
- Activity-based selection possible (covalent capture)

### GPCRs & Membrane Proteins

- Use detergent-solubilized or nanodisc-reconstituted target
- Extend wash stringency carefully (detergent may disrupt weak binders)
- Counter-select against detergent micelles alone

### Intracellular Targets

- Prioritize permeability: N-methyl-rich libraries
- Consider lactam cyclization (no Cys → less polar)
- Cell-penetrating peptide (CPP) conjugation post-screen

## Scripts

### `scripts/rapid_designer.py`

Design a RaPID selection campaign from target properties:

```bash
python3 scripts/rapid_designer.py \
  --target PPI \
  --library_length 12 \
  --ncaa_type ClAc-D-Phe \
  --cyclization thioether \
  --rounds 6
```

Outputs: library oligo design, flexizyme choice, cyclization plan, selection protocol.

### `scripts/flexizyme_selector.py`

Recommend flexizyme variant and acyl-donor ester for a given NCAA:

```bash
python3 scripts/flexizyme_selector.py --ncaa "N-Me-Phe"
python3 scripts/flexizyme_selector.py --ncaa "ClAc-Lys"
```

Outputs: recommended flexizyme, acyl-donor ester type, reaction conditions, expected charging yield.

## References

- Suga H, et al. "Flexizymes for genetic code reprogramming." Nat Protoc (2023)
- Katoh T, Suga H. "RaPID selection of macrocyclic peptides." Methods Mol Biol (2022)
- Yamagishi Y, et al. "Natural product-like macrocyclic N-methyl-peptide inhibitors against a ubiquitin ligase." ChemBioChem (2011)
- Ito K, et al. "Thioether macrocyclic peptide inhibitors of SARS-CoV-2."  Sci Adv (2023)
- PeptiDream platform: PDPS (PeptiDream Discovery Platform System)

# From RaPID Hit to Drug Candidate

## Stage 1: Hit Confirmation (Week 1–2)

### SPPS Resynthesis of Macrocyclic Peptides

**Standard Fmoc-SPPS for thioether macrocycles:**

1. Load Cys(Trt)-OH on Rink amide resin (0.1 mmol scale)
2. Fmoc deprotection: 20% piperidine/DMF, 2×3 min
3. Coupling: Fmoc-AA-OH (4 eq), HATU (3.8 eq), DIEA (8 eq), DMF, 30 min
4. Repeat for each residue (C→N direction)
5. N-terminal ClAc-D-Phe coupling: ClAc-D-Phe-OH (3 eq), HATU, DIEA, 1h
6. Global deprotection: TFA/H₂O/TIPS (95:2.5:2.5), 2h
7. Cleavage from resin → crude linear peptide
8. **Macrocyclization**: Dilute to 0.5 mM in 50 mM NH₄HCO₃ pH 8.0, RT, 2–12h
9. Monitor by LC-MS, purify by RP-HPLC

**Yield expectations**: 5–20% overall (linear + cyclization + purification)

### Binding Affinity Measurement

| Method | Sample amount | Time | Information |
|---|---|---|---|
| SPR (Biacore) | 50–200 µg | 1 day | Kd, kon, koff |
| ITC | 200–500 µg | 1 day | Kd, ΔH, ΔS, stoichiometry |
| MST | 5–20 µg | 2h | Kd only |
| BLI (Octet) | 20–50 µg | 4h | Kd, kon, koff |
| FP | 1–5 µg | 1h | Kd (fluorescent label needed) |

### Specificity Panel

Test against:
- Closest homologs (≥30% sequence identity)
- Off-target panel (10–20 unrelated proteins)
- Serum albumin (HSA) — rule out non-specific binding
- Streptavidin (if using biotin selection)

## Stage 2: Structure-Activity Relationship (Week 3–6)

### Alanine Scan

1. Synthesize each residue → Ala mutant (except Cys for cyclization)
2. Measure Kd for each mutant
3. Classify residues: Core contact (ΔΔG > 1.5 kcal/mol), Peripheral (0.5–1.5), Tolerant (< 0.5)

### Truncation Scan

1. N-terminal truncation: remove 1 residue at a time
2. C-terminal truncation: remove 1 residue at a time
3. Identify minimum binding epitope

### Focused Library (Secondary RaPID)

Based on SAR data, design focused library:
- Fix conserved contact residues
- Randomize tolerant positions (2–4 positions)
- Include N-Me/D-AA at solvent-exposed positions
- Re-screen with higher stringency

## Stage 3: Stability & Permeability Optimization (Week 4–10)

### Serum Stability

```bash
# Protocol
1. Incubate 10 µM peptide in 50% human serum at 37°C
2. Time points: 0, 0.5, 1, 2, 4, 8, 24 h
3. Quench with 2 vol 70% ACN + 0.1% formic acid
4. Analyze by LC-MS (intact peptide peak)
5. Calculate t₁/₂ from exponential decay fit

# Benchmarks
Linear peptide: t₁/₂ < 30 min
Thioether macrocycle: t₁/₂ = 2–24 h
N-methylated macrocycle: t₁/₂ = 24–200 h
D-AA-containing macrocycle: t₁/₂ = 50–500 h
```

### N-Methylation Strategy for Permeability

**Rules of thumb** (based on Borchardt, Kessler, Lokey studies):

1. N-methylate amide bonds pointing toward solvent (based on NMR/model)
2. Avoid N-methylation at H-bond donors that contact target
3. Maintain ≤3 consecutive N-methylated residues
4. N-Me scan: synthesize all single N-Me variants, test permeability + binding
5. Combine favorable N-Me positions in multi-N-Me analogs

**Permeability assays:**

| Assay | Metric | Good | Acceptable | Poor |
|---|---|---|---|---|
| PAMPA | Pₑ (10⁻⁶ cm/s) | >10 | 1–10 | <1 |
| Caco-2 | A→B (10⁻⁶ cm/s) | >10 | 1–10 | <1 |
| RRCK | Papp (10⁻⁶ cm/s) | >5 | 0.5–5 | <0.5 |

### D-Amino Acid Substitution

1. Substitute one L-AA at a time with D-AA at non-contact positions
2. Measure serum stability and binding affinity
3. Favorable substitutions: extended half-life without affinity loss
4. Can combine with N-methylation

## Stage 4: In Vivo PK/PD (Week 8–16)

### PK Study Design

| Species | Dose | Route | Time points | n |
|---|---|---|---|---|
| Mouse | 1 mg/kg | IV | 0.05, 0.25, 0.5, 1, 2, 4, 8, 24h | 3/timepoint |
| Mouse | 5 mg/kg | SC | 0.25, 0.5, 1, 2, 4, 8, 24h | 3/timepoint |
| Rat | 1 mg/kg | IV | same as mouse | 3/timepoint |

**Bioanalysis**: LC-MS/MS (MRM), LLOQ typically 1–10 ng/mL

**Typical macrocyclic peptide PK parameters:**

| Parameter | Thioether macrocycle | + N-Me | + D-AA |
|---|---|---|---|
| CL (mL/min/kg) | 30–80 | 15–40 | 10–30 |
| Vd (L/kg) | 0.3–1.0 | 0.5–2.0 | 0.5–3.0 |
| t₁/₂ (h) | 0.3–2 | 1–6 | 2–12 |
| F (%) | <5 | 5–20 | 10–40 |

### PD Considerations

- Target engagement biomarker (if available)
- PD duration often exceeds PK t₁/₂ for tight binders (Kd < 10 nM)
- Dose at 3–10× Kd for proof-of-concept

## Stage 5: Patent & Regulatory

### Key Patent Landscape

| Entity | Patent family | Coverage |
|---|---|---|
| **Univ. Tokyo (Suga)** | Flexizyme + RaPID system | Method claims: flexizyme-mediated charging, RaPID selection |
| **Takeda** | Exclusive license for therapeutics | Co-development with Suga lab |
| **PeptiDream** | PDPS platform | Macrocyclic peptide discovery; separate from RaPID but related chemistry |
| **Bicycle Therapeutics** | Phage display + thioether | Bicycle® peptides; different display but same cyclization |

### Freedom-to-Operate Considerations

- **Academic research**: Generally permitted under research exemption
- **Commercial therapeutic**: License from Takeda/Univ. Tokyo required for RaPID-derived hits
- **Alternative**: Use phage display + post-screening thioether cyclization (Bicycle approach) to avoid RaPID method claims
- **New IP**: Novel sequences, novel target applications, optimization modifications are patentable

### IND-Enabling Studies for Macrocyclic Peptides

| Study | Duration | Notes |
|---|---|---|
| GLP tox (rat + dog) | 3–6 months | Single + repeat dose |
| Safety pharmacology | 1–3 months | Cardiovascular (hERG), CNS, respiratory |
| Genotoxicity | 1–2 months | Ames, micronucleus |
| CMC | Ongoing | GMP synthesis, formulation, stability |
| Species selection | 1–2 months | Target binding cross-species, PK/PD bridging |

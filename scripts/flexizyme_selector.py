#!/usr/bin/env python3
"""
Flexizyme Selector — Recommend flexizyme variant and acyl-donor for a given NCAA.
"""

import argparse
import json

# Comprehensive NCAA → flexizyme mapping
NCAA_DATABASE = {
    # Aromatic amino acids (dFx)
    "L-Phe": {"fx": "dFx", "ester": "Phe-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "80-90"},
    "D-Phe": {"fx": "dFx", "ester": "Phe-CME", "conc_mM": 5, "time_h": 6, "yield_pct": "30-50"},
    "4-F-Phe": {"fx": "dFx", "ester": "4-F-Phe-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "75-85"},
    "4-Cl-Phe": {"fx": "dFx", "ester": "4-Cl-Phe-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "70-80"},
    "L-Tyr": {"fx": "dFx", "ester": "Tyr-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "75-85"},
    "L-Trp": {"fx": "dFx", "ester": "Trp-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "70-80"},
    "1-Nal": {"fx": "dFx", "ester": "1-Nal-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "70-80"},
    "2-Nal": {"fx": "dFx", "ester": "2-Nal-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "70-80"},
    "Bpa": {"fx": "dFx", "ester": "Bpa-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "65-75"},
    "β-Phe": {"fx": "dFx", "ester": "β-Phe-CME", "conc_mM": 5, "time_h": 4, "yield_pct": "50-65"},
    
    # N-methyl amino acids (dFx)
    "N-Me-Phe": {"fx": "dFx", "ester": "N-Me-Phe-CME", "conc_mM": 5, "time_h": "2-4", "yield_pct": "60-75"},
    "N-Me-Ala": {"fx": "dFx", "ester": "N-Me-Ala-CME", "conc_mM": 5, "time_h": 4, "yield_pct": "40-55"},
    "N-Me-Leu": {"fx": "dFx", "ester": "N-Me-Leu-CME", "conc_mM": 5, "time_h": "2-4", "yield_pct": "55-70"},
    "N-Me-Val": {"fx": "dFx", "ester": "N-Me-Val-CME", "conc_mM": 5, "time_h": "4", "yield_pct": "45-60"},
    "N-Me-Ser": {"fx": "dFx", "ester": "N-Me-Ser-CME", "conc_mM": 5, "time_h": "4", "yield_pct": "40-55"},
    "N-Me-Ile": {"fx": "dFx", "ester": "N-Me-Ile-CME", "conc_mM": 5, "time_h": "4", "yield_pct": "45-60"},
    "N-Me-Thr": {"fx": "dFx", "ester": "N-Me-Thr-CME", "conc_mM": 5, "time_h": "4", "yield_pct": "40-55"},
    
    # Cyclization warheads (dFx)
    "ClAc-D-Phe": {"fx": "dFx", "ester": "ClAc-D-Phe-CME", "conc_mM": 5, "time_h": "2-4", "yield_pct": "60-70"},
    "ClAc-D-Ala": {"fx": "dFx", "ester": "ClAc-D-Ala-CME", "conc_mM": 5, "time_h": "2-4", "yield_pct": "55-65"},
    "ClAc-Gly": {"fx": "dFx", "ester": "ClAc-Gly-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "60-70"},
    "BrAc-D-Phe": {"fx": "dFx", "ester": "BrAc-D-Phe-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "65-75"},
    "Acr-D-Phe": {"fx": "dFx", "ester": "Acr-D-Phe-CME", "conc_mM": 5, "time_h": "2-4", "yield_pct": "50-65"},
    
    # Aliphatic amino acids (aFx)
    "L-Ala": {"fx": "aFx", "ester": "Ala-2,3-DNB", "conc_mM": 5, "time_h": 0.5, "yield_pct": "65-75"},
    "Gly": {"fx": "aFx", "ester": "Gly-2,3-DNB", "conc_mM": 5, "time_h": 0.5, "yield_pct": "70-80"},
    "L-Ser": {"fx": "aFx", "ester": "Ser-2,3-DNB", "conc_mM": 5, "time_h": 0.5, "yield_pct": "60-70"},
    "L-Thr": {"fx": "aFx", "ester": "Thr-2,3-DNB", "conc_mM": 5, "time_h": 0.5, "yield_pct": "55-65"},
    "L-Val": {"fx": "aFx", "ester": "Val-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "55-65"},
    "L-Leu": {"fx": "aFx", "ester": "Leu-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "55-65"},
    "L-Ile": {"fx": "aFx", "ester": "Ile-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "50-60"},
    "L-Asp": {"fx": "aFx", "ester": "Asp-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "50-60"},
    "L-Glu": {"fx": "aFx", "ester": "Glu-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "50-60"},
    "L-Lys": {"fx": "aFx", "ester": "Lys-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "45-55"},
    "L-Arg": {"fx": "aFx", "ester": "Arg-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "40-50"},
    "L-Pro": {"fx": "aFx", "ester": "Pro-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "40-55"},
    
    # β/γ-amino acids (aFx)
    "β-Ala": {"fx": "aFx", "ester": "β-Ala-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "45-55"},
    "GABA": {"fx": "aFx", "ester": "GABA-2,3-DNB", "conc_mM": 5, "time_h": 1, "yield_pct": "45-55"},
    
    # Click chemistry handles (dFx)
    "Pra": {"fx": "dFx", "ester": "Pra-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "60-70"},
    
    # Heteroaromatic (eFx)
    "2-ThiAla": {"fx": "eFx", "ester": "2-ThiAla-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "65-75"},
    "3-ThiAla": {"fx": "eFx", "ester": "3-ThiAla-CME", "conc_mM": 5, "time_h": 2, "yield_pct": "65-75"},
    "His": {"fx": "eFx", "ester": "His-CME", "conc_mM": 5, "time_h": 4, "yield_pct": "50-65"},
}

# Aliases
ALIASES = {
    "N-Me-Phenylalanine": "N-Me-Phe",
    "N-Me-Alanine": "N-Me-Ala",
    "N-Me-Leucine": "N-Me-Leu",
    "N-Me-Valine": "N-Me-Val",
    "N-Me-Serine": "N-Me-Ser",
    "N-Me-Isoleucine": "N-Me-Ile",
    "N-Me-Threonine": "N-Me-Thr",
    "chloroacetyl-D-Phe": "ClAc-D-Phe",
    "chloroacetyl-D-Ala": "ClAc-D-Ala",
    "bromoacetyl-D-Phe": "BrAc-D-Phe",
    "acryloyl-D-Phe": "Acr-D-Phe",
    "propargylglycine": "Pra",
    "p-benzoylphenylalanine": "Bpa",
    "Phenylalanine": "L-Phe",
    "Tyrosine": "L-Tyr",
    "Tryptophan": "L-Trp",
    "Alanine": "L-Ala",
    "Glycine": "Gly",
    "Serine": "L-Ser",
    "Threonine": "L-Thr",
    "Valine": "L-Val",
    "Leucine": "L-Leu",
    "Isoleucine": "L-Ile",
    "Aspartate": "L-Asp",
    "Glutamate": "L-Glu",
    "Lysine": "L-Lys",
    "Arginine": "L-Arg",
    "Proline": "L-Pro",
}

def lookup_ncaa(name):
    """Look up NCAA in database, trying aliases."""
    # Direct lookup
    if name in NCAA_DATABASE:
        return name, NCAA_DATABASE[name]
    
    # Try alias
    if name in ALIASES:
        canonical = ALIASES[name]
        if canonical in NCAA_DATABASE:
            return canonical, NCAA_DATABASE[canonical]
    
    # Case-insensitive search
    name_lower = name.lower()
    for key in NCAA_DATABASE:
        if key.lower() == name_lower:
            return key, NCAA_DATABASE[key]
    
    for alias, canonical in ALIASES.items():
        if alias.lower() == name_lower and canonical in NCAA_DATABASE:
            return canonical, NCAA_DATABASE[canonical]
    
    # Partial match
    for key in NCAA_DATABASE:
        if name_lower in key.lower() or key.lower() in name_lower:
            return key, NCAA_DATABASE[key]
    
    return None, None

def infer_from_name(name):
    """Infer flexizyme recommendation when NCAA is not in database."""
    name_lower = name.lower()
    
    if any(kw in name_lower for kw in ["n-me", "nmethyl", "n-methyl"]):
        return {
            "fx": "dFx",
            "ester": "N-Me-AA-CME (custom synthesis)",
            "conc_mM": 5,
            "time_h": "2-6",
            "yield_pct": "40-75 (estimate)",
            "notes": "N-methyl AAs typically charged with dFx via CME ester"
        }
    
    if any(kw in name_lower for kw in ["clac", "chloroacetyl", "brac", "bromoacetyl"]):
        return {
            "fx": "dFx",
            "ester": "ClAc/BrAc-AA-CME",
            "conc_mM": 5,
            "time_h": "2-4",
            "yield_pct": "55-75 (estimate)",
            "notes": "Cyclization warheads work with dFx; use CME ester"
        }
    
    if any(kw in name_lower for kw in ["d-", "d-"]):
        return {
            "fx": "dFx (if aromatic) or aFx (if aliphatic)",
            "ester": "CME ester (dFx) or 2,3-DNB ester (aFx)",
            "conc_mM": 5,
            "time_h": "4-6",
            "yield_pct": "30-50 (estimate)",
            "notes": "D-AAs give lower yields; longer incubation recommended"
        }
    
    if any(kw in name_lower for kw in ["phe", "tyr", "trp", "nal", "bpa", "aromatic"]):
        return {
            "fx": "dFx or eFx",
            "ester": "AA-CME ester",
            "conc_mM": 5,
            "time_h": "2-6",
            "yield_pct": "65-90 (estimate)",
            "notes": "Aromatic AAs are standard dFx substrates"
        }
    
    if any(kw in name_lower for kw in ["ala", "gly", "ser", "thr", "val", "leu", "ile", "asp", "glu", "lys", "arg", "pro", "aliphatic"]):
        return {
            "fx": "aFx",
            "ester": "AA-2,3-DNB ester",
            "conc_mM": 5,
            "time_h": "0.5-1",
            "yield_pct": "40-80 (estimate)",
            "notes": "Aliphatic AAs require aFx with 2,3-DNB ester"
        }
    
    return {
        "fx": "tFx (tRNA-flexizyme)",
        "ester": "Acyl-tRNA mimic (custom 3'-ACC substrate)",
        "conc_mM": "0.5-2",
        "time_h": "2-6",
        "yield_pct": "20-60 (estimate)",
        "notes": "Unusual substrate — use tFx with custom acyl-tRNA mimic; consider aFx with 2,3-DNB as alternative"
    }

def main():
    parser = argparse.ArgumentParser(description="Select flexizyme variant for a given NCAA")
    parser.add_argument("--ncaa", required=True, help="Non-canonical amino acid name")
    parser.add_argument("--all", action="store_true", help="Show all matching results")
    args = parser.parse_args()
    
    canonical, data = lookup_ncaa(args.ncaa)
    
    if data:
        result = {
            "query": args.ncaa,
            "canonical_name": canonical,
            "recommended_flexizyme": data["fx"],
            "acyl_donor_ester": data["ester"],
            "concentration_mM": data["conc_mM"],
            "incubation_time_h": data["time_h"],
            "expected_charging_yield": data["yield_pct"],
            "reaction_protocol": {
                "step1": f"Prepare {data['fx']} (25 µM) + tRNA_CUA (25 µM) in 50 mM HEPES-KOH pH 7.5",
                "step2": "Denature 95°C 1 min → slow cool to RT",
                "step3": f"Add {data['ester']} ({data['conc_mM']} mM final) in DMSO (≤20% v/v)",
                "step4": f"Incubate on ice {data['time_h']}h",
                "step5": "Quench with 0.1 vol 1.5 M NaOAc pH 5.2",
                "step6": "Confirm charging by acidic PAGE or RP-HPLC",
                "step7": "Ethanol precipitate, dissolve in translation buffer"
            }
        }
    else:
        inferred = infer_from_name(args.ncaa)
        result = {
            "query": args.ncaa,
            "canonical_name": "NOT IN DATABASE (inferred recommendation)",
            "recommended_flexizyme": inferred["fx"],
            "acyl_donor_ester": inferred["ester"],
            "concentration_mM": inferred.get("conc_mM", "N/A"),
            "incubation_time_h": inferred.get("time_h", "N/A"),
            "expected_charging_yield": inferred.get("yield_pct", "N/A"),
            "notes": inferred.get("notes", ""),
            "reaction_protocol": {
                "step1": f"Prepare {inferred['fx']} (25 µM) + tRNA_CUA (25 µM) in 50 mM HEPES-KOH pH 7.5",
                "step2": "Denature 95°C 1 min → slow cool to RT",
                "step3": f"Add {inferred['ester']} ({inferred.get('conc_mM', '?')} mM final) in DMSO (≤20% v/v)",
                "step4": f"Incubate on ice {inferred.get('time_h', '?')}h",
                "step5": "Quench with 0.1 vol 1.5 M NaOAc pH 5.2",
                "step6": "Confirm charging by acidic PAGE or RP-HPLC",
                "step7": "Ethanol precipitate, dissolve in translation buffer"
            }
        }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

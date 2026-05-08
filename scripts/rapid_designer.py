#!/usr/bin/env python3
"""
RaPID Selection Campaign Designer
Designs a complete RaPID selection campaign from target properties.
"""

import argparse
import json
import math

# Target type → library design recommendations
TARGET_PROFILES = {
    "PPI": {
        "library_length": (8, 15),
        "preferred_length": 12,
        "cyclization": "thioether",
        "ncaa_warhead": "ClAc-D-Phe",
        "rounds": (5, 8),
        "notes": "PPI targets benefit from larger macrocycles to cover the flat interface"
    },
    "enzyme": {
        "library_length": (4, 10),
        "preferred_length": 8,
        "cyclization": "thioether",
        "ncaa_warhead": "ClAc-D-Phe",
        "rounds": (4, 7),
        "notes": "Shorter libraries can access enzyme active sites; consider electrophilic warhead"
    },
    "GPCR": {
        "library_length": (6, 12),
        "preferred_length": 10,
        "cyclization": "thioether",
        "ncaa_warhead": "ClAc-D-Phe",
        "rounds": (6, 10),
        "notes": "Nanodisc or detergent-solubilized target required; more rounds for membrane targets"
    },
    "ion_channel": {
        "library_length": (6, 12),
        "preferred_length": 10,
        "cyclization": "thioether",
        "ncaa_warhead": "ClAc-D-Phe",
        "rounds": (6, 10),
        "notes": "Similar to GPCR; consider pore-blocking peptides"
    },
    "transcription factor": {
        "library_length": (8, 15),
        "preferred_length": 12,
        "cyclization": "thioether",
        "ncaa_warhead": "ClAc-D-Phe",
        "rounds": (5, 8),
        "notes": "DNA-binding surface is typically flat; large macrocycles preferred"
    },
    "intracellular": {
        "library_length": (6, 12),
        "preferred_length": 10,
        "cyclization": "lactam",
        "ncaa_warhead": "ClAc-D-Phe + N-Me-AAs",
        "rounds": (6, 10),
        "notes": "Prioritize N-methylated library for cell permeability; lactam cyclization reduces polarity"
    },
}

CODON_SCHEMES = {
    "NNB": {"total": 48, "stop_fraction": 1/48, "description": "Reduced stop codons, good coverage"},
    "NNS": {"total": 64, "stop_fraction": 3/64, "description": "Standard, more stop codons than NNB"},
    "NNK": {"total": 64, "stop_fraction": 1/32, "description": "Equal AA representation, moderate stops"},
}

def calculate_library_stats(length, codon_scheme="NNB"):
    scheme = CODON_SCHEMES[codon_scheme]
    total_sequences = scheme["total"] ** length
    productive_fraction = 1 - scheme["stop_fraction"]
    # Probability that ALL positions are NOT stop
    productive_sequences = int(total_sequences * (productive_fraction ** length))
    return {
        "theoretical_diversity": total_sequences,
        "productive_sequences": productive_sequences,
        "productive_fraction": round(productive_fraction ** length, 4),
        "codon_scheme": codon_scheme,
    }

def design_oligo(length, codon_scheme="NNB", ncaa_codon="TAG"):
    """Design the DNA oligo for the library."""
    if codon_scheme == "NNB":
        random_codon = "NNB"
    elif codon_scheme == "NNS":
        random_codon = "NNS"
    else:
        random_codon = "NNK"

    # Typical RaPID library: 5'-T7promoter-ribosome_binding-AUG-(random)n-UAG-3'
    # NCAA at UAG position (C-terminal or internal)
    random_region = "-".join([random_codon] * length)
    
    oligo_template = {
        "T7_promoter": "TAATACGACTCACTATA",
        "ribosome_binding": "GGGAGGACGAUG",  # Includes start context
        "start_codon": "ATG",
        "random_region": random_region,
        "ncaa_codon": ncaa_codon,
        "puromycin_linker": "Linker-(PEG)3-CC-puromycin"
    }
    
    return oligo_template

def design_selection_rounds(num_rounds, target_type):
    """Design selection protocol for each round."""
    rounds = []
    for i in range(1, num_rounds + 1):
        round_plan = {
            "round": i,
            "target_concentration": max(10, 500 // (2 ** (i-1))),  # nM, decreasing
            "wash_steps": min(3 + i, 10),
            "wash_volume": "1 mL",
            "incubation_time": "30 min" if i <= 2 else "1h",
            "counter_selection": i >= 2,
            "counter_target": "Tag-only or irrelevant protein" if i >= 2 else "None",
            "stringency_note": ""
        }
        
        if i <= 2:
            round_plan["stringency_note"] = "Low stringency — capture diverse binders"
        elif i <= 4:
            round_plan["stringency_note"] = "Moderate stringency — add counter-selection"
            round_plan["wash_steps"] = 5 + i
        elif i <= 6:
            round_plan["stringency_note"] = "High stringency — extended washes, competitor"
            round_plan["wash_steps"] = 8 + i
        else:
            round_plan["stringency_note"] = "Very high stringency — off-rate selection if needed"
            round_plan["incubation_time"] = "2h + overnight wash"
        
        rounds.append(round_plan)
    return rounds

def main():
    parser = argparse.ArgumentParser(description="Design a RaPID selection campaign")
    parser.add_argument("--target", required=True, 
                        choices=list(TARGET_PROFILES.keys()),
                        help="Target type")
    parser.add_argument("--library_length", type=int, default=None,
                        help="Random region length (amino acids)")
    parser.add_argument("--ncaa_type", default=None,
                        help="NCAA warhead (e.g. ClAc-D-Phe)")
    parser.add_argument("--cyclization", default=None,
                        choices=["thioether", "lactam", "head-to-tail", "disulfide"],
                        help="Cyclization strategy")
    parser.add_argument("--rounds", type=int, default=None,
                        help="Number of selection rounds")
    parser.add_argument("--codon_scheme", default="NNB",
                        choices=["NNB", "NNS", "NNK"],
                        help="Codon randomization scheme")
    parser.add_argument("--ncaa_codon", default="TAG",
                        help="Codon reassigned to NCAA (default: TAG/amber)")
    
    args = parser.parse_args()
    
    profile = TARGET_PROFILES[args.target]
    
    length = args.library_length or profile["preferred_length"]
    cyclization = args.cyclization or profile["cyclization"]
    ncaa = args.ncaa_type or profile["ncaa_warhead"]
    num_rounds = args.rounds or profile["rounds"][1]
    
    # Calculate library stats
    lib_stats = calculate_library_stats(length, args.codon_scheme)
    
    # Design oligo
    oligo = design_oligo(length, args.codon_scheme, args.ncaa_codon)
    
    # Design selection rounds
    selection = design_selection_rounds(num_rounds, args.target)
    
    # Recommend flexizyme
    flexizyme_rec = recommend_flexizyme(ncaa)
    
    result = {
        "target_type": args.target,
        "target_notes": profile["notes"],
        "library": {
            "length": length,
            "codon_scheme": args.codon_scheme,
            "ncaa_codon": args.ncaa_codon,
            "ncaa_type": ncaa,
            "cyclization": cyclization,
            "stats": lib_stats,
            "oligo_design": oligo,
        },
        "flexizyme": flexizyme_rec,
        "selection": selection,
        "estimated_timeline": f"{num_rounds * 3}-{num_rounds * 5} days for selection + 1-2 weeks for sequencing and hit confirmation",
    }
    
    print(json.dumps(result, indent=2))

def recommend_flexizyme(ncaa_type):
    """Recommend flexizyme variant based on NCAA type."""
    ncaa_lower = ncaa_type.lower()
    
    if "clac" in ncaa_lower or "brac" in ncaa_lower:
        return {
            "recommended": "dFx (dinitro-flexizyme)",
            "acyl_donor": "CME ester",
            "concentration": "5 mM",
            "incubation": "2-4h on ice",
            "expected_yield": "60-75%",
            "notes": "Chloroacetyl/bromoacetyl warheads work well with dFx via CME ester"
        }
    elif "n-me" in ncaa_lower or "nmethyl" in ncaa_lower:
        return {
            "recommended": "dFx (dinitro-flexizyme)",
            "acyl_donor": "N-Me-AA-CME ester",
            "concentration": "5 mM",
            "incubation": "2-4h on ice",
            "expected_yield": "40-75%",
            "notes": "N-methyl amino acids charge well with dFx; yield varies with AA size"
        }
    elif any(x in ncaa_lower for x in ["phe", "tyr", "trp", "nal", "bpa"]):
        return {
            "recommended": "dFx or eFx",
            "acyl_donor": "CME ester (dFx) or thioester (eFx)",
            "concentration": "5 mM",
            "incubation": "2-6h on ice",
            "expected_yield": "70-90%",
            "notes": "Aromatic AAs are the original dFx substrates; highest yields"
        }
    elif any(x in ncaa_lower for x in ["gly", "ala", "ser", "thr", "val", "leu", "ile", "asp", "glu", "lys", "arg", "pro"]):
        return {
            "recommended": "aFx (amino-flexizyme)",
            "acyl_donor": "2,3-DNB ester",
            "concentration": "5 mM",
            "incubation": "0.5-1h on ice",
            "expected_yield": "40-80%",
            "notes": "Aliphatic AAs require aFx; fastest reaction among flexizymes"
        }
    elif "d-" in ncaa_lower:
        return {
            "recommended": "dFx (aromatic D-AA) or aFx (aliphatic D-AA)",
            "acyl_donor": "CME ester (dFx) or 2,3-DNB ester (aFx)",
            "concentration": "5 mM",
            "incubation": "4-6h on ice",
            "expected_yield": "30-50%",
            "notes": "D-amino acids generally give lower yields; longer incubation helps"
        }
    else:
        return {
            "recommended": "tFx (tRNA-flexizyme)",
            "acyl_donor": "Acyl-tRNA mimic (3'-ACC linked)",
            "concentration": "0.5-2 mM",
            "incubation": "2-6h on ice",
            "expected_yield": "20-60%",
            "notes": "For unusual substrates not compatible with dFx/eFx/aFx; requires custom synthesis"
        }

if __name__ == "__main__":
    main()

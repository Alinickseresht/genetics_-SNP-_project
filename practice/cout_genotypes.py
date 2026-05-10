
#!/usr/bin/env python3
"""
count_genotypes.py - Count homozygous/heterozygous for a given SNP from a hypothetical CSV file
"""

import pandas as pd
import sys

def count_genotypes_from_csv(csv_path, sample_col='genotype'):
    """
    csv_path: CSV file containing a column with genotypes like 'A/A', 'A/G', 'G/G'
    Returns: counts of reference homozygous, heterozygous, alternative homozygous
    """
    df = pd.read_csv(csv_path)
    if sample_col not in df.columns:
        print(f"Column '{sample_col}' not found. Available columns: {list(df.columns)}")
        return None
    
    genotypes = df[sample_col].dropna()
    hom_ref = (genotypes == 'A/A').sum()
    het = (genotypes == 'A/G').sum()
    hom_alt = (genotypes == 'G/G').sum()
    return hom_ref, het, hom_alt

def simulate_genotype_csv(output_path, n_samples=100, freq_alt=0.3):
    """
    Generate a simulated CSV file of genotypes (for practice)
    """
    import numpy as np
    # According to Hardy-Weinberg equilibrium
    p = 1 - freq_alt
    q = freq_alt
    prob_hom_ref = p**2
    prob_het = 2*p*q
    prob_hom_alt = q**2
    genotypes = np.random.choice(['A/A', 'A/G', 'G/G'], size=n_samples, p=[prob_hom_ref, prob_het, prob_hom_alt])
    df = pd.DataFrame({'sample_id': range(1, n_samples+1), 'genotype': genotypes})
    df.to_csv(output_path, index=False)
    print(f"Simulated file saved: {output_path}")
    return output_path

if name == 'main':
    # If no input file provided, simulate one and analyze
    if len(sys.argv) < 2:
        sim_file = "practice/simulated_genotypes.csv"
        simulate_genotype_csv(sim_file)
        csv_path = sim_file
    else:
        csv_path = sys.argv[1]
    
    res = count_genotypes_from_csv(csv_path)
    if res:
        hom_ref, het, hom_alt = res
        total = hom_ref + het + hom_alt
        print(f"Reference homozygous (A/A): {hom_ref} ({hom_ref/total:.1%})")
        print(f"Heterozygous (A/G): {het} ({het/total:.1%})")
        print(f"Alternative homozygous (G/G): {hom_alt} ({hom_alt/total:.1%})")



# Introduction to SNP (Single Nucleotide Polymorphism)

## Definition
An SNP is a single base pair change (A, T, C, G) in the DNA sequence that occurs in at least 1% of the population. Example: at position 1000, most individuals have 'A' but some have 'G'.

## Key Components
- REF (Reference Allele): The allele present in the reference genome.
- ALT (Alternative Allele): The allele that differs from the reference.
- Genotype: The combination of alleles in an individual at a specific position. Three states:
  - Reference Homozygous (REF/REF) : e.g., A|A
  - Heterozygous (REF/ALT) : e.g., A|G
  - Alternative Homozygous (ALT/ALT) : e.g., G|G

## Allele Frequency
The proportion of a particular allele in a population. If a population of 100 individuals (200 chromosomes) has 40 copies of allele G, then frequency of G is 0.2 (20%).

## VCF Format (Variant Call Format)
Standard file format for storing SNPs and indels. Main columns:
- #CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT, followed by sample names.
- The FORMAT and sample columns, e.g., GT:AD:DP and values like 0/1:12,5:17.

## Applications
- Ancestry inference
- Disease prediction
- Pharmacogenomics



---

## scripts/compare_populations.py
`python
#!/usr/bin/env python3
"""
compare_populations.py - Chi-square test for comparing genotype frequencies between two populations
"""

import pandas as pd
from scipy.stats import chi2_contingency
import sys

def chi2_test_for_snp(df, snp_col, pop1_col, pop2_col):
    """
    df: DataFrame with columns (pop1_col, pop2_col) containing genotype strings like '0/0', '0/1', '1/1'
    snp_col is unused but kept for consistency
    Returns chi2 statistic and p-value
    """
    # Count 2x3 contingency table
    pop1_counts = df[pop1_col].value_counts()
    pop2_counts = df[pop2_col].value_counts()
    # Ensure all three categories (0/0, 0/1, 1/1) are present
    all_cats = ['0/0', '0/1', '1/1']
    pop1_arr = [pop1_counts.get(cat, 0) for cat in all_cats]
    pop2_arr = [pop2_counts.get(cat, 0) for cat in all_cats]
    contingency = [pop1_arr, pop2_arr]
    chi2, p, dof, expected = chi2_contingency(contingency)
    return chi2, p

def create_sample_population_csv(output_path='datasets/processed/population_data.csv'):
    import numpy as np
    np.random.seed(123)
    n_samples = 200
    # Population A: ALT allele frequency = 0.2
    # Population B: ALT allele frequency = 0.6
    def sample_genotype(freq_alt):
        p = 1-freq_alt
        q = freq_alt
        r = np.random.random()
        if r < p**2:
            return '0/0'
        elif r < p**2 + 2*p*q:
            return '0/1'
        else:
            return '1/1'
    
    popA = [sample_genotype(0.2) for _ in range(n_samples)]
    popB = [sample_genotype(0.6) for _ in range(n_samples)]
    df = pd.DataFrame({'pop_A': popA, 'pop_B': popB})
    df.to_csv(output_path, index=False)
    print(f"Sample data for two populations created: {output_path}")
    return df

if name == 'main':
    # If file doesn't exist, create a sample
    try:
        df = pd.read_csv('datasets/processed/population_data.csv')
    except:
        df = create_sample_population_csv()
    
    chi2, p = chi2_test_for_snp(df, None, 'pop_A', 'pop_B')
    print(f"Chi-square test: chi2 = {chi2:.3f}, p-value = {p:.4f}")
    if p < 0.05:
        print("Significant difference between the two populations.")
    else:
        print("No significant difference.")


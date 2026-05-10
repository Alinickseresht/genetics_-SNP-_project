
#!/usr/bin/env python3
"""
compare_populations.py - Chi-square test for comparing genotype frequencies between two populations
"""

import pandas as pd
import sys
import os

def chi2_test_for_snp(df, pop1_col, pop2_col):
    """
    Perform chi-square test of independence for genotype counts between two populations.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with columns pop1_col and pop2_col containing genotype strings
        like '0/0', '0/1', '1/1' (or 'A/A', 'A/G', 'G/G').
    pop1_col : str
        Column name for population 1.
    pop2_col : str
        Column name for population 2.
    
    Returns
    -------
    chi2 : float
        Chi-square statistic.
    p : float
        P-value.
    expected : ndarray
        Expected frequencies under null hypothesis.
    """
    from scipy.stats import chi2_contingency
    
    # Count genotype occurrences for each population
    pop1_counts = df[pop1_col].value_counts()
    pop2_counts = df[pop2_col].value_counts()
    
    # Ensure all three categories exist (add missing with 0)
    all_cats = ['0/0', '0/1', '1/1']  # standard VCF encoding
    # Also handle potential 'A/A', 'A/G', 'G/G' format from simulated data
    if set(pop1_counts.index) | set(pop2_counts.index) - set(all_cats):
        # if categories differ, try the A/A style
        all_cats = ['A/A', 'A/G', 'G/G']
    
    pop1_arr = [pop1_counts.get(cat, 0) for cat in all_cats]
    pop2_arr = [pop2_counts.get(cat, 0) for cat in all_cats]
    
    contingency = [pop1_arr, pop2_arr]
    chi2, p, dof, expected = chi2_contingency(contingency)
    return chi2, p, expected

def create_sample_population_csv(output_path='datasets/processed/population_data.csv'):
    """
    Create a synthetic dataset of two populations with different ALT allele frequencies.
    Population A: ALT frequency 0.2, Population B: ALT frequency 0.6.
    """
    import numpy as np
    np.random.seed(123)
    n_samples = 200
    
    def sample_genotype(freq_alt):
        p = 1 - freq_alt
        q = freq_alt
        probs = [p2, 2*p*q, q2]   # [0/0, 0/1, 1/1]
        choices = np.random.choice(['0/0', '0/1', '1/1'], p=probs)
        return choices
    
    popA = [sample_genotype(0.2) for _ in range(n_samples)]
    popB = [sample_genotype(0.6) for _ in range(n_samples)]
    df = pd.DataFrame({'pop_A': popA, 'pop_B': popB})
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Sample population data created: {output_path}")
    return df

def main():
    data_path = 'datasets/processed/population_data.csv'
    
    # If data file doesn't exist, create it
    if not os.path.exists(data_path):
        df = create_sample_population_csv(data_path)
    else:
        df = pd.read_csv(data_path)
    
    # Run chi-square test
    try:
        chi2, p, expected = chi2_test_for_snp(df, 'pop_A', 'pop_B')
        print(f"Chi-square statistic: {chi2:.4f}")
        print(f"P-value: {p:.6e}" if p < 0.001 else f"P-value: {p:.4f}")
        if p < 0.05:
            print("Result: Significant difference between the two populations.")
        else:
            print("Result: No significant difference between the two populations.")
        print("\nExpected contingency table (under null hypothesis):")
        print(expected)
    except ImportError:
        print("Error: scipy not installed. Please run: pip install scipy")
        sys.exit(1)

if name == 'main':
    main()


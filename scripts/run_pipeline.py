#!/usr/bin/env python3
"""
compute_allele_freq.py - Calculate allele frequencies from a VCF file and save as CSV
"""

import sys
import pandas as pd
import numpy as np

def compute_allele_frequency(vcf_path, output_csv='datasets/processed/allele_freq.csv', max_snps=None):
    """
    Parse VCF and compute ALT allele frequency for each SNP.
    Assumes diploid genotypes in GT field (0/0, 0/1, 1/1).
    """
    # Read VCF without comment lines (except the header)
    # First find the column names line
    with open(vcf_path, 'r') as f:
        header_line = None
        for line in f:
            if line.startswith('#CHROM'):
                header_line = line.strip()
                break
    if not header_line:
        print("Error: No #CHROM line found.")
        return None
    
    col_names = header_line.lstrip('#').split('\t')
    # Read data skipping comment lines
    df = pd.read_csv(vcf_path, comment='#', sep='\t', names=col_names, dtype=str, nrows=max_snps)
    
    # Identify sample columns (those after FORMAT)
    format_idx = col_names.index('FORMAT')
    sample_cols = col_names[format_idx+1:]
    
    results = []
    for idx, row in df.iterrows():
        chrom = row['#CHROM']
        pos = row['POS']
        ref = row['REF']
        alt = row['ALT']
        # Gather genotypes from each sample
        alt_count = 0
        total_alleles = 0
        for sample in sample_cols:
            gt_field = str(row[sample]).split(':')[0]  # GT is first
            if gt_field in ['./.', '.|.', '']:
                continue  # missing genotype
            # Replace '|' with '/'
            gt = gt_field.replace('|', '/')
            alleles = gt.split('/')
            if len(alleles) != 2:
                continue
            total_alleles += 2
            # Count ALT alleles (assuming 1 = ALT, 0 = REF)
            for a in alleles:
                if a == '1':
                    alt_count += 1
                elif a == '0':
                    pass
                else:
                    # If allele is something else (like .), skip
                    pass
        if total_alleles == 0:
            freq = np.nan
        else:
            freq = alt_count / total_alleles
        results.append({
            'CHROM': chrom,
            'POS': pos,
            'REF': ref,
            'ALT': alt,
            'ALT_allele_freq': freq,
            'num_samples_used': total_alleles // 2
        })
    
    freq_df = pd.DataFrame(results)
    freq_df.to_csv(output_csv, index=False)
    print(f"Allele frequencies saved to {output_csv}")
    return freq_df

if name == 'main':
    if len(sys.argv) < 2:
        print("Usage: python compute_allele_freq.py <vcf_file> [--max_snps N]")
        sys.exit(1)
    vcf_file = sys.argv[1]
    max_snps = None
    if '--max_snps' in sys.argv:
        idx = sys.argv.index('--max_snps')
        if idx+1 < len(sys.argv):
            max_snps = int(sys.argv[idx+1])
    compute_allele_frequency(vcf_file, max_snps=max_snps)



#!/usr/bin/env python3
"""
parse_vcf.py - Basic parsing of VCF files and information extraction
"""

import sys
import pandas as pd

def parse_vcf_metadata(vcf_path, max_rows=10):
    """
    Read the beginning of a VCF file and convert to DataFrame
    """
    # Use pandas with tab separator, skip lines starting with ##
    try:
        # Read the header line starting with #CHROM
        with open(vcf_path, 'r') as f:
            header_line = None
            for line in f:
                if line.startswith('#CHROM'):
                    header_line = line.strip()
                    break
        if not header_line:
            print("#CHROM header not found!")
            return None
        
        column_names = header_line.lstrip('#').split('\t')
        # Read data with pandas
        data = pd.read_csv(vcf_path, comment='#', sep='\t', names=column_names,
                           dtype={'#CHROM': str, 'POS': int, 'REF': str, 'ALT': str},
                           nrows=max_rows)
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def extract_info(sample_row, format_col='FORMAT'):
    """
    Extract genotypes from sample columns (simple version: first field GT)
    """
    # Determine sample columns (those after FORMAT)
    sample_columns = [col for col in sample_row.index if col not in ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']]
    genotypes = {}
    for sample in sample_columns:
        genotype_field = sample_row[sample]
        if pd.notna(genotype_field):
            # Usually GT is first, e.g., "0/1" or "0|1"
            gt = genotype_field.split(':')[0]
            genotypes[sample] = gt
        else:
            genotypes[sample] = './.'
    return genotypes

if name == 'main':
    if len(sys.argv) < 2:
        print("Usage: python parse_vcf.py <path_to_vcf> [--max_rows N]")
        sys.exit(1)
    
    vcf_file = sys.argv[1]
    max_rows = 20
    if '--max_rows' in sys.argv:
        idx = sys.argv.index('--max_rows')
        if idx+1 < len(sys.argv):
            max_rows = int(sys.argv[idx+1])
    
    df = parse_vcf_metadata(vcf_file, max_rows)
    if df is not None:
        print("Sample extracted data:")
        print(df.head())
        
        # Example: extract genotypes of first row
        if len(df) > 0:
            first_row = df.iloc[0]
            genotypes = extract_info(first_row)
            print("\nGenotypes for the first row:")
            print(genotypes)


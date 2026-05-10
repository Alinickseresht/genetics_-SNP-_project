
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

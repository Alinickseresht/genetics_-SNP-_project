#!/bin/bash
# download_real_data.sh - Download a small real VCF from 1000 Genomes (chromosome 22, low-coverage)
# Requires: wget, tabix (samtools)

set -e

echo "Downloading a small real VCF from 1000 Genomes..."
VCF_URL="https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
OUT_DIR="datasets/raw/real_data"
mkdir -p $OUT_DIR

cd $OUT_DIR
wget -c $VCF_URL
wget -c ${VCF_URL}.tbi

# Extract first 1000 SNPs (optional)
echo "Extracting first 1000 SNPs to a smaller file..."
gunzip -c ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz | head -n 10000 > sample_1000snps.vcf

echo "Done. File saved as $OUT_DIR/sample_1000snps.vcf"

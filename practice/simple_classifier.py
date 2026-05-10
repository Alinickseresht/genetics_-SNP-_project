
#!/usr/bin/env python3
"""
simple_classifier.py - Train a logistic regression classifier to predict population from SNP genotypes
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def generate_synthetic_snp_data(n_samples=500, n_snps=20, seed=42):
    """
    Generate synthetic SNP data for two populations.
    Population 0: low ALT allele frequency (0.2)
    Population 1: high ALT allele frequency (0.6)
    """
    np.random.seed(seed)
    # Assign population labels (0 or 1)
    labels = np.random.choice([0, 1], size=n_samples)
    # Genotype matrix: rows = samples, cols = SNPs
    genotypes = np.zeros((n_samples, n_snps), dtype=str)
    # Convert to one-hot or numeric encoding: 0=0/0, 1=0/1, 2=1/1
    numeric_geno = np.zeros((n_samples, n_snps), dtype=int)
    
    for i in range(n_samples):
        if labels[i] == 0:
            freq_alt = 0.2
        else:
            freq_alt = 0.6
        p = 1 - freq_alt
        q = freq_alt
        probs = [p2, 2*p*q, q2]  # [0/0, 0/1, 1/1]
        for snp in range(n_snps):
            gt_code = np.random.choice([0, 1, 2], p=probs)
            numeric_geno[i, snp] = gt_code
            if gt_code == 0:
                genotypes[i, snp] = "0/0"
            elif gt_code == 1:
                genotypes[i, snp] = "0/1"
            else:
                genotypes[i, snp] = "1/1"
    
    return numeric_geno, labels, genotypes

def main():
    print("Generating synthetic SNP data for two populations...")
    X, y, genotypes = generate_synthetic_snp_data(n_samples=800, n_snps=30)
    
    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train logistic regression
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    
    # Predict
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {acc:.3f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=["Pop_A (low ALT freq)", "Pop_B (high ALT freq)"]))
    
    # Optional: show coefficients for top SNPs
    coef_abs = np.abs(clf.coef_[0])
    top_snp_indices = np.argsort(coef_abs)[-5:][::-1]
    print("\nTop 5 most discriminative SNPs (by coefficient magnitude):")
    for idx in top_snp_indices:
        print(f"  SNP {idx}: coefficient = {clf.coef_[0][idx]:.3f}")

if name == 'main':
    main()



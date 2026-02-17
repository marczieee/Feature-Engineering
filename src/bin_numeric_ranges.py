"""
Feature Engineering Module 3: Bin Numeric Ranges
Group 6 - Groups continuous numerical variables into discrete bins
"""

import pandas as pd
import numpy as np


def bin_numeric_ranges(df):
    df_new = df.copy()

    if 'age' in df_new.columns:
        bins = [0, 25, 35, 50, 65, 100]
        labels = ['18-25', '26-35', '36-50', '51-65', '65+']
        df_new['age_group'] = pd.cut(df_new['age'], bins=bins, labels=labels, include_lowest=True)
        print(f"  Created: age_group  {labels}")

    if 'income' in df_new.columns:
        bins = [0, 30000, 50000, 75000, 100000, np.inf]
        labels = ['Low', 'Lower-Middle', 'Middle', 'Upper-Middle', 'High']
        df_new['income_bracket'] = pd.cut(df_new['income'], bins=bins, labels=labels)
        print(f"  Created: income_bracket  {labels}")

    if 'purchase_amount' in df_new.columns:
        bins = [0, 100, 500, 1000, 2000, np.inf]
        labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
        df_new['purchase_category'] = pd.cut(df_new['purchase_amount'], bins=bins, labels=labels)
        print(f"  Created: purchase_category  {labels}")

    if 'rating' in df_new.columns:
        bins = [0, 2, 3, 4, 5]
        labels = ['Poor', 'Fair', 'Good', 'Excellent']
        df_new['rating_category'] = pd.cut(df_new['rating'], bins=bins, labels=labels, include_lowest=True)
        print(f"  Created: rating_category  {labels}")

    if 'discount_percent' in df_new.columns:
        bins = [0, 10, 25, 40, 100]
        labels = ['No Discount', 'Low Discount', 'Medium Discount', 'High Discount']
        df_new['discount_tier'] = pd.cut(df_new['discount_percent'], bins=bins, labels=labels, include_lowest=True)
        print(f"  Created: discount_tier  {labels}")

    if 'final_price' in df_new.columns:
        df_new['price_quartile'] = pd.qcut(df_new['final_price'], q=4,
                                            labels=['Q1', 'Q2', 'Q3', 'Q4'],
                                            duplicates='drop')
        print("  Created: price_quartile (quantile-based Q1-Q4)")

    if 'income_purchase_ratio' in df_new.columns:
        df_new['spending_ratio_bin'] = pd.cut(df_new['income_purchase_ratio'], bins=5)
        print("  Created: spending_ratio_bin (5 equal-width bins)")

    return df_new


def process_csv(input_file, output_file=None):
    print("\n" + "="*55)
    print("MODULE 3: BIN NUMERIC RANGES")
    print("="*55)

    if isinstance(input_file, str):
        df = pd.read_csv(input_file)
        print(f"Loaded: {input_file}")
    else:
        df = input_file.copy()
        print("Loaded DataFrame from previous step")

    print(f"Original shape: {df.shape}")
    df_processed = bin_numeric_ranges(df)
    print(f"New shape: {df_processed.shape}")
    print(f"Added {df_processed.shape[1] - df.shape[1]} new columns")

    if output_file:
        df_processed.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")

    return df_processed


if __name__ == "__main__":
    df = process_csv('data/processed/step2_encoded_features.csv',
                     'data/processed/step3_binned_features.csv')
    print("\nSample output:")
    cols = ['age', 'age_group', 'income', 'income_bracket', 'purchase_amount', 'purchase_category']
    available = [c for c in cols if c in df.columns]
    print(df[available].head(8))

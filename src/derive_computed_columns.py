"""
Feature Engineering Module 1: Derive Computed Columns
Group 6 - Creates new columns from mathematical operations on existing columns
"""

import pandas as pd
import numpy as np


def derive_computed_columns(df):
    df_new = df.copy()

    if 'purchase_amount' in df_new.columns and 'shipping_cost' in df_new.columns:
        df_new['total_cost'] = (df_new['purchase_amount'] + df_new['shipping_cost']).round(2)
        print("  Created: total_cost")

    if 'purchase_amount' in df_new.columns and 'discount_percent' in df_new.columns:
        df_new['discount_amount'] = (df_new['purchase_amount'] * df_new['discount_percent'] / 100).round(2)
        print("  Created: discount_amount")

    if 'total_cost' in df_new.columns and 'discount_amount' in df_new.columns:
        df_new['final_price'] = (df_new['total_cost'] - df_new['discount_amount']).round(2)
        print("  Created: final_price")

    if 'final_price' in df_new.columns and 'rating' in df_new.columns:
        df_new['price_per_rating'] = (df_new['final_price'] / df_new['rating']).round(2)
        print("  Created: price_per_rating")

    if 'income' in df_new.columns and 'purchase_amount' in df_new.columns:
        df_new['income_purchase_ratio'] = (df_new['purchase_amount'] / df_new['income'] * 100).round(2)
        print("  Created: income_purchase_ratio")

    if 'age' in df_new.columns:
        df_new['age_squared'] = df_new['age'] ** 2
        print("  Created: age_squared")

    if 'income' in df_new.columns and 'age' in df_new.columns:
        df_new['spending_power_index'] = ((df_new['income'] / 1000) / df_new['age']).round(2)
        print("  Created: spending_power_index")

    return df_new


def process_csv(input_file, output_file=None):
    print("\n" + "="*55)
    print("MODULE 1: DERIVE COMPUTED COLUMNS")
    print("="*55)

    if isinstance(input_file, str):
        df = pd.read_csv(input_file)
        print(f"Loaded: {input_file}")
    else:
        df = input_file.copy()
        print("Loaded DataFrame from previous step")

    print(f"Original shape: {df.shape}")
    df_processed = derive_computed_columns(df)
    print(f"New shape: {df_processed.shape}")
    print(f"Added {df_processed.shape[1] - df.shape[1]} new columns")

    if output_file:
        df_processed.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")

    return df_processed


if __name__ == "__main__":
    df = process_csv('data/raw/sample_data.csv',
                     'data/processed/step1_computed_columns.csv')
    print("\nSample output:")
    print(df[['purchase_amount', 'shipping_cost', 'total_cost', 'discount_amount', 'final_price']].head())

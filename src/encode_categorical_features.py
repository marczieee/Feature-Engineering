"""
Feature Engineering Module 2: Encode Categorical Features
Group 6 - Converts categorical variables into numerical representations
"""

import pandas as pd
import numpy as np


def encode_categorical_features(df):
    df_new = df.copy()

    categorical_cols = df_new.select_dtypes(include=['object']).columns.tolist()

    # Remove datetime-like columns
    datetime_cols = []
    for col in categorical_cols:
        try:
            pd.to_datetime(df_new[col])
            datetime_cols.append(col)
        except:
            pass
    categorical_cols = [c for c in categorical_cols if c not in datetime_cols]

    print(f"\n  Found {len(categorical_cols)} categorical columns: {categorical_cols}")

    # Label Encoding for ordinal features
    if 'education' in df_new.columns:
        order = ['High School', 'Bachelor', 'Master', 'PhD']
        df_new['education_encoded'] = df_new['education'].map({v: i for i, v in enumerate(order)})
        print("  Label encoded: education -> education_encoded (0=High School, 3=PhD)")

    # One-Hot Encoding for nominal features
    for col in ['gender', 'product_category']:
        if col in df_new.columns:
            dummies = pd.get_dummies(df_new[col], prefix=col, drop_first=False)
            # Convert boolean to int
            dummies = dummies.astype(int)
            df_new = pd.concat([df_new, dummies], axis=1)
            print(f"  One-hot encoded: {col} -> {list(dummies.columns)}")

    # Frequency Encoding for remaining categorical
    already_encoded = ['education', 'gender', 'product_category']
    for col in categorical_cols:
        if col not in already_encoded and col in df_new.columns:
            freq = df_new[col].value_counts(normalize=True)
            df_new[f'{col}_freq'] = df_new[col].map(freq).round(4)
            print(f"  Frequency encoded: {col} -> {col}_freq")

    return df_new


def process_csv(input_file, output_file=None):
    print("\n" + "="*55)
    print("MODULE 2: ENCODE CATEGORICAL FEATURES")
    print("="*55)

    if isinstance(input_file, str):
        df = pd.read_csv(input_file)
        print(f"Loaded: {input_file}")
    else:
        df = input_file.copy()
        print("Loaded DataFrame from previous step")

    print(f"Original shape: {df.shape}")
    df_processed = encode_categorical_features(df)
    print(f"New shape: {df_processed.shape}")
    print(f"Added {df_processed.shape[1] - df.shape[1]} new columns")

    if output_file:
        df_processed.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")

    return df_processed


if __name__ == "__main__":
    df = process_csv('data/processed/step1_computed_columns.csv',
                     'data/processed/step2_encoded_features.csv')
    print("\nSample output:")
    enc_cols = [c for c in df.columns if '_encoded' in c or 'gender_' in c]
    print(df[enc_cols[:4]].head())

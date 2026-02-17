"""
Feature Engineering Module 4: Time-Based Feature Extraction
Group 6 - Extracts temporal features from datetime columns
"""

import pandas as pd
import numpy as np


def time_based_feature_extraction(df):
    df_new = df.copy()

    # Detect datetime columns
    datetime_cols = []
    for col in df_new.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                df_new[col] = pd.to_datetime(df_new[col])
                datetime_cols.append(col)
            except:
                pass

    print(f"\n  Found {len(datetime_cols)} datetime column(s): {datetime_cols}")

    for col in datetime_cols:
        print(f"\n  Extracting from: {col}")

        df_new[f'{col}_year']         = df_new[col].dt.year
        df_new[f'{col}_month']        = df_new[col].dt.month
        df_new[f'{col}_month_name']   = df_new[col].dt.month_name()
        df_new[f'{col}_day']          = df_new[col].dt.day
        df_new[f'{col}_day_of_week']  = df_new[col].dt.dayofweek
        df_new[f'{col}_day_name']     = df_new[col].dt.day_name()
        df_new[f'{col}_quarter']      = df_new[col].dt.quarter
        df_new[f'{col}_week_of_year'] = df_new[col].dt.isocalendar().week.astype(int)
        df_new[f'{col}_is_weekend']   = df_new[col].dt.dayofweek.isin([5, 6]).astype(int)
        df_new[f'{col}_is_month_start'] = df_new[col].dt.is_month_start.astype(int)
        df_new[f'{col}_is_month_end']   = df_new[col].dt.is_month_end.astype(int)

        epoch = pd.Timestamp('1970-01-01')
        df_new[f'{col}_days_since_epoch'] = (df_new[col] - epoch).dt.days

        month = df_new[col].dt.month
        df_new[f'{col}_season'] = month.apply(lambda x:
            'Winter' if x in [12, 1, 2] else
            'Spring' if x in [3, 4, 5] else
            'Summer' if x in [6, 7, 8] else
            'Fall'
        )

        today = pd.Timestamp.now()
        df_new[f'{col}_days_from_today'] = (today - df_new[col]).dt.days
        df_new[f'{col}_is_recent']       = (df_new[f'{col}_days_from_today'] <= 30).astype(int)

        new_cols = [c for c in df_new.columns if c.startswith(f'{col}_')]
        for nc in new_cols:
            print(f"    Created: {nc}")

    return df_new


def process_csv(input_file, output_file=None):
    print("\n" + "="*55)
    print("MODULE 4: TIME-BASED FEATURE EXTRACTION")
    print("="*55)

    if isinstance(input_file, str):
        df = pd.read_csv(input_file)
        print(f"Loaded: {input_file}")
    else:
        df = input_file.copy()
        print("Loaded DataFrame from previous step")

    print(f"Original shape: {df.shape}")
    df_processed = time_based_feature_extraction(df)
    print(f"New shape: {df_processed.shape}")
    print(f"Added {df_processed.shape[1] - df.shape[1]} new columns")

    if output_file:
        df_processed.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")

    return df_processed


if __name__ == "__main__":
    df = process_csv('data/processed/step3_binned_features.csv',
                     'data/processed/step4_time_features.csv')
    print("\nSample time columns:")
    time_cols = [c for c in df.columns if 'purchase_date' in c][:6]
    if time_cols:
        print(df[time_cols].head())

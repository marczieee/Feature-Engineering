"""
Feature Engineering Module 5: Flag Anomalies Column
Group 6 - Detects and flags outliers using statistical methods
"""

import pandas as pd
import numpy as np
from scipy import stats


def flag_zscore(df, column, threshold=3):
    z_scores = np.abs(stats.zscore(df[column].dropna()))
    flags = pd.Series(0, index=df.index)
    flags.loc[df[column].notna()] = (z_scores > threshold).astype(int)
    return flags


def flag_iqr(df, column, multiplier=1.5):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return ((df[column] < lower) | (df[column] > upper)).astype(int)


def flag_anomalies_column(df):
    df_new = df.copy()

    numeric_cols = df_new.select_dtypes(include=[np.number]).columns.tolist()

    # Only flag the key meaningful columns
    priority = ['income', 'purchase_amount', 'final_price', 'age',
                'shipping_cost', 'discount_percent', 'rating']
    cols_to_check = [c for c in priority if c in numeric_cols]

    print(f"\n  Flagging anomalies in: {cols_to_check}\n")

    for col in cols_to_check:
        z_flag   = flag_zscore(df_new, col, threshold=3)
        iqr_flag = flag_iqr(df_new, col, multiplier=1.5)

        df_new[f'{col}_anomaly_zscore'] = z_flag
        df_new[f'{col}_anomaly_iqr']    = iqr_flag
        df_new[f'{col}_is_anomaly']     = ((z_flag == 1) | (iqr_flag == 1)).astype(int)

        z_n   = z_flag.sum()
        iqr_n = iqr_flag.sum()
        both  = df_new[f'{col}_is_anomaly'].sum()
        print(f"  {col}: Z-score={z_n}  IQR={iqr_n}  Combined={both}")

    # Overall anomaly score per row
    anomaly_cols = [c for c in df_new.columns if c.endswith('_is_anomaly')]
    df_new['anomaly_score']    = df_new[anomaly_cols].sum(axis=1)
    df_new['has_any_anomaly']  = (df_new['anomaly_score'] > 0).astype(int)

    total = df_new['has_any_anomaly'].sum()
    print(f"\n  Rows with at least one anomaly: {total} ({total/len(df_new)*100:.1f}%)")
    print("  Created: anomaly_score, has_any_anomaly")

    return df_new


def process_csv(input_file, output_file=None):
    print("\n" + "="*55)
    print("MODULE 5: FLAG ANOMALIES COLUMN")
    print("="*55)

    if isinstance(input_file, str):
        df = pd.read_csv(input_file)
        print(f"Loaded: {input_file}")
    else:
        df = input_file.copy()
        print("Loaded DataFrame from previous step")

    print(f"Original shape: {df.shape}")
    df_processed = flag_anomalies_column(df)
    print(f"New shape: {df_processed.shape}")
    print(f"Added {df_processed.shape[1] - df.shape[1]} new columns")

    if output_file:
        df_processed.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")

    return df_processed


if __name__ == "__main__":
    df = process_csv('data/processed/step4_time_features.csv',
                     'data/processed/step5_anomaly_flags.csv')
    print("\nSample anomaly output:")
    cols = ['income', 'income_is_anomaly', 'purchase_amount',
            'purchase_amount_is_anomaly', 'anomaly_score', 'has_any_anomaly']
    available = [c for c in cols if c in df.columns]
    print(df[available].head(10))

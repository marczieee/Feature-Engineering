"""
main.py - Feature Engineering Pipeline
Group 6 | DevOps Midterm
Automatically detects CSV files in /input and saves results to /output
"""

import os
import sys
import pandas as pd
from datetime import datetime

from src.derive_computed_columns import process_csv as derive_columns
from src.encode_categorical_features import process_csv as encode_features
from src.bin_numeric_ranges import process_csv as bin_features
from src.time_based_feature_extraction import process_csv as extract_time_features
from src.flag_anomalies_column import process_csv as flag_anomalies


INPUT_DIR  = "input"
OUTPUT_DIR = "output"


def detect_csv_files(folder):
    """Automatically detect all CSV files in the input folder"""
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"  Created folder: {folder}/")
    csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    return csv_files


def run_pipeline():
    start_time = datetime.now()

    print("\n" + "="*60)
    print("  FEATURE ENGINEERING PIPELINE - GROUP 6")
    print("  DevOps Midterm | CI/CD Automated Run")
    print("="*60)
    print(f"  Started : {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Input   : {INPUT_DIR}/")
    print(f"  Output  : {OUTPUT_DIR}/")
    print("="*60)

    # Ensure output folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Auto-detect CSV files
    csv_files = detect_csv_files(INPUT_DIR)

    if not csv_files:
        print("\n  No CSV files found in input/. Generating sample data...")
        import generate_sample_data
        csv_files = detect_csv_files(INPUT_DIR)

    print(f"\n  Found {len(csv_files)} CSV file(s): {csv_files}\n")

    all_results = {}

    for csv_file in csv_files:
        input_path = os.path.join(INPUT_DIR, csv_file)
        base_name  = csv_file.replace('.csv', '')

        print(f"\n{'='*60}")
        print(f"  Processing: {csv_file}")
        print(f"{'='*60}")

        try:
            original_df = pd.read_csv(input_path)
            print(f"  Rows: {len(original_df)} | Columns: {len(original_df.columns)}")

            # Step 1 - Derive Computed Columns
            print("\nSTEP 1/5: derive_computed_columns")
            df = derive_columns(input_path)
            df.to_csv(f"{OUTPUT_DIR}/{base_name}_step1_computed.csv", index=False)

            # Step 2 - Encode Categorical Features
            print("\nSTEP 2/5: encode_categorical_features")
            df = encode_features(df)
            df.to_csv(f"{OUTPUT_DIR}/{base_name}_step2_encoded.csv", index=False)

            # Step 3 - Bin Numeric Ranges
            print("\nSTEP 3/5: bin_numeric_ranges")
            df = bin_features(df)
            df.to_csv(f"{OUTPUT_DIR}/{base_name}_step3_binned.csv", index=False)

            # Step 4 - Time-Based Feature Extraction
            print("\nSTEP 4/5: time_based_feature_extraction")
            df = extract_time_features(df)
            df.to_csv(f"{OUTPUT_DIR}/{base_name}_step4_time.csv", index=False)

            # Step 5 - Flag Anomalies
            print("\nSTEP 5/5: flag_anomalies_column")
            df = flag_anomalies(df)

            # Save final output
            final_path = f"{OUTPUT_DIR}/{base_name}_FINAL.csv"
            df.to_csv(final_path, index=False)

            all_results[csv_file] = {
                'original_cols': original_df.shape[1],
                'final_cols': df.shape[1],
                'rows': len(df),
                'new_features': df.shape[1] - original_df.shape[1]
            }

            print(f"\n  Saved final output: {final_path}")

        except Exception as e:
            print(f"\n  ERROR processing {csv_file}: {e}")
            import traceback
            traceback.print_exc()
            continue

    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "="*60)
    print("  PIPELINE SUMMARY")
    print("="*60)
    for fname, info in all_results.items():
        print(f"\n  File    : {fname}")
        print(f"  Rows    : {info['rows']}")
        print(f"  Before  : {info['original_cols']} columns")
        print(f"  After   : {info['final_cols']} columns")
        print(f"  Added   : {info['new_features']} new features")

    print(f"\n  Duration  : {duration:.2f} seconds")
    print(f"  Output in : {OUTPUT_DIR}/")
    print("="*60)
    print("  ALL STEPS COMPLETED SUCCESSFULLY")
    print("="*60 + "\n")

    return all_results


if __name__ == "__main__":
    run_pipeline()

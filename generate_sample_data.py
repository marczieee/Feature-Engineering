"""
generate_sample_data.py
Generates a sample CSV file and places it in the input/ folder
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

np.random.seed(42)
n = 1000

income          = np.random.randint(20000, 150000, n)
purchase_amount = np.random.uniform(10, 5000, n).round(2)

# Inject anomalies
idx = np.random.choice(n, 50, replace=False)
income[idx]          = np.random.randint(200000, 500000, 50)
purchase_amount[idx] = np.random.uniform(8000, 15000, 50).round(2)

data = {
    'customer_id':      range(1, n + 1),
    'age':              np.random.randint(18, 80, n),
    'gender':           np.random.choice(['Male', 'Female', 'Other'], n),
    'education':        np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n),
    'income':           income,
    'purchase_amount':  purchase_amount,
    'purchase_date':    [(datetime.now() - timedelta(days=int(np.random.randint(0, 365)))).strftime('%Y-%m-%d')
                         for _ in range(n)],
    'product_category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], n),
    'rating':           np.random.uniform(1, 5, n).round(1),
    'discount_percent': np.random.uniform(0, 50, n).round(2),
    'shipping_cost':    np.random.uniform(0, 50, n).round(2),
}

df = pd.DataFrame(data)
output_path = "input/sample_data.csv"
df.to_csv(output_path, index=False)

print(f"Sample CSV generated: {output_path}")
print(f"Shape: {df.shape}")
print(df.head(3))

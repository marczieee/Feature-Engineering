# Feature Engineering Pipeline - Group 6
### DevOps Midterm | Automated CSV Data Processing using CI Pipeline

![Python](https://img.shields.io/badge/python-3.11-blue)
![pytest](https://img.shields.io/badge/tested%20with-pytest-yellow)

---

## 👥 Group Members
| Name |
|------|
| [Gelera, Marc Eldrian] 
| [Pacheco, Haroliyen] | 
| [Bolina, Renz Andrae] 
| [Aganan, Akira Yuki] 

---

## 📋 Project Overview

This project implements an **automated CSV data processing pipeline** with a **GitHub Actions CI/CD pipeline**. Every time code is pushed or a pull request is made, GitHub automatically:

1. Detects CSV files in the `input/` folder
2. Runs all 5 feature engineering functions
3. Saves processed results to the `output/` folder
4. Runs all PyTest tests to validate correctness
5. Commits output files back to the repository

---

## 📁 Project Structure

```
Feature-Engineering-Group-6/
│
├── .github/
│   └── workflows/
│       └── ci.yml                        ← GitHub Actions CI Pipeline
│
├── src/                                  ← 5 Python processing functions
│   ├── __init__.py
│   ├── derive_computed_columns.py        ← Function 1
│   ├── encode_categorical_features.py    ← Function 2
│   ├── bin_numeric_ranges.py             ← Function 3
│   ├── time_based_feature_extraction.py  ← Function 4
│   └── flag_anomalies_column.py          ← Function 5
│
├── tests/
│   └── test_features.py                  ← PyTest test cases (30+ tests)
│
├── input/                                ← Place CSV files here
│   └── sample_data.csv
│
├── output/                               ← Processed results saved here
│   ├── sample_data_step1_computed.csv
│   ├── sample_data_step2_encoded.csv
│   ├── sample_data_step3_binned.csv
│   ├── sample_data_step4_time.csv
│   └── sample_data_FINAL.csv
│
├── main.py                               ← Pipeline orchestrator
├── generate_sample_data.py               ← Sample CSV generator
├── requirements.txt                      ← Python dependencies
└── README.md                             ← This file
```

---

## ⚙️ Five CSV Processing Functions

### Function 1 — `derive_computed_columns.py`
Creates new columns using mathematical operations on existing columns.

| New Column | Formula |
|---|---|
| `total_cost` | purchase_amount + shipping_cost |
| `discount_amount` | purchase_amount × discount_percent / 100 |
| `final_price` | total_cost − discount_amount |
| `price_per_rating` | final_price / rating |
| `income_purchase_ratio` | purchase_amount / income × 100 |
| `spending_power_index` | (income / 1000) / age |

### Function 2 — `encode_categorical_features.py`
Converts text/category columns into numbers for machine learning.

| Technique | Applied To | Output |
|---|---|---|
| Label Encoding | education | 0=High School → 3=PhD |
| One-Hot Encoding | gender | gender_Male, gender_Female, gender_Other |
| One-Hot Encoding | product_category | product_category_Electronics, etc. |

### Function 3 — `bin_numeric_ranges.py`
Groups continuous numbers into meaningful categories/bins.

| New Column | Bins |
|---|---|
| `age_group` | 18-25, 26-35, 36-50, 51-65, 65+ |
| `income_bracket` | Low, Lower-Middle, Middle, Upper-Middle, High |
| `purchase_category` | Very Low, Low, Medium, High, Very High |
| `rating_category` | Poor, Fair, Good, Excellent |
| `discount_tier` | No Discount, Low, Medium, High |

### Function 4 — `time_based_feature_extraction.py`
Extracts temporal features from date columns.

| New Column | Description |
|---|---|
| `purchase_date_year` | Year of purchase |
| `purchase_date_month` | Month number (1-12) |
| `purchase_date_day_of_week` | 0=Monday, 6=Sunday |
| `purchase_date_is_weekend` | 1 if Saturday/Sunday |
| `purchase_date_quarter` | Q1, Q2, Q3, Q4 |
| `purchase_date_season` | Winter, Spring, Summer, Fall |
| `purchase_date_days_from_today` | Days since purchase |

### Function 5 — `flag_anomalies_column.py`
Detects statistical outliers using two methods.

| Method | How it works |
|---|---|
| Z-score | Flags values more than 3 standard deviations from mean |
| IQR | Flags values outside 1.5× interquartile range |
| `has_any_anomaly` | 1 if anomaly detected by either method |
| `anomaly_score` | Count of anomalous columns per row |

---

## 🔄 CI/CD Workflow

```
Developer pushes code
        │
        ▼
GitHub Actions triggers automatically
        │
        ├── Install Python 3.11
        ├── Install requirements.txt
        ├── Generate sample CSV (if input/ empty)
        ├── Run main.py pipeline
        │       ├── Step 1: derive_computed_columns
        │       ├── Step 2: encode_categorical_features
        │       ├── Step 3: bin_numeric_ranges
        │       ├── Step 4: time_based_feature_extraction
        │       └── Step 5: flag_anomalies_column
        ├── Run PyTest (30+ tests)
        └── Commit output/ files back to repo
```

The CI pipeline runs on:
- Every **push** to `main` or `master`
- Every **pull request** to `main` or `master`

---

## 🚀 How to Run Locally

### 1. Clone the repository
```
git clone https://github.com/marczieee/Feature-Engineering-Group-6.git
cd Feature-Engineering-Group-6
```

### 2. Install dependencies
```
py -m pip install -r requirements.txt
```

### 3. Add your CSV to the input folder
```
copy your_file.csv input\
```

### 4. Run the pipeline
```
py main.py
```

### 5. Run tests
```
py -m pytest tests/ -v
```

### 6. Check output folder
```
ls output\
```

---

## 🧪 Testing Strategy

All 5 functions are tested using **PyTest** with 30+ test cases organized into classes:

| Test Class | Tests |
|---|---|
| `TestDeriveComputedColumns` | 8 tests |
| `TestEncodeCategoricalFeatures` | 6 tests |
| `TestBinNumericRanges` | 7 tests |
| `TestTimeBasedFeatureExtraction` | 10 tests |
| `TestFlagAnomaliesColumn` | 7 tests |
| `TestFullPipeline` | 4 integration tests |

---

## 📦 Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.11.0
```

---

**Group 6 | DevOps Midterm**

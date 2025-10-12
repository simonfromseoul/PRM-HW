# --- imports ---
import pandas as pd

# --- import data ---
df = pd.read_excel("multi_asset_etf_data.xlsx", sheet_name='excess returns')

# --- display the data ---
print("Shape:", df.shape)
print("\nColumn dtypes:\n", df.dtypes)

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))

# --- descriptive stats ---

# Numeric columns
num = df.select_dtypes(include="number")
if not num.empty:
    print("\nNumeric summary (describe):")
    print(num.describe().transpose().to_string())

    print("\nCorrelation matrix (numeric):")
    print(num.corr(numeric_only=True).to_string())

# Categorical / object columns
cat = df.select_dtypes(exclude="number")
if not cat.empty:
    print("\nCategorical summary:")
    # For objects, describe shows count, unique, top, freq
    print(cat.describe().transpose().to_string())

# Missing values overview
na_counts = df.isna().sum().sort_values(ascending=False)
na_counts = na_counts[na_counts > 0]
print("\nMissing values per column:")
print(na_counts.to_string())


# Draw the time series of the asset classes (excluding QAI)
import matplotlib.pyplot as plt

date_col = df.columns[0]
df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=[date_col]).sort_values(date_col).set_index(date_col)

# numeric class columns
cols = df.select_dtypes(include="number").columns.tolist()
if "QAI" in cols:
    cols.remove("QAI")

ax = df[cols].plot(figsize=(10, 5))
ax.set_title("Time Series by Asset Class (excluding QAI)")
ax.set_xlabel("Date")
ax.set_ylabel("Excess Return")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()



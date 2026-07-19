import os
import pandas as pd


# Find the main project folder
project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

raw_file = os.path.join(
    project_root,
    "data",
    "atm_cash_data_raw.csv"
)

cleaned_file = os.path.join(
    project_root,
    "data",
    "atm_cash_data_cleaned.csv"
)


# Load dataset
df = pd.read_csv(raw_file)

print("Dataset loaded successfully.")
print("Original shape:", df.shape)


# Convert date column
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)


# Fill missing numerical values using median
df["temperature"] = df["temperature"].fillna(
    df["temperature"].median()
)

df["average_withdrawal"] = df[
    "average_withdrawal"
].fillna(
    df["average_withdrawal"].median()
)

df["deposit_amount"] = df[
    "deposit_amount"
].fillna(
    df["deposit_amount"].median()
)


# Remove duplicate rows
duplicates = df.duplicated().sum()

print("Duplicate rows found:", duplicates)

df = df.drop_duplicates()


# Remove invalid negative values
numeric_columns = [
    "transaction_count",
    "average_withdrawal",
    "withdrawal_amount",
    "deposit_amount",
    "opening_cash",
    "cash_remaining",
    "next_day_cash_requirement"
]

for column in numeric_columns:
    df = df[df[column] >= 0]


# Create useful date features
df["year"] = df["date"].dt.year
df["day"] = df["date"].dt.day
df["day_of_year"] = df["date"].dt.dayofyear


# Validate binary columns
binary_columns = [
    "is_weekend",
    "is_holiday",
    "cash_out",
    "replenishment_required"
]

for column in binary_columns:
    df[column] = df[column].astype(int)


# Sort dataset
df = df.sort_values(
    by=["date", "atm_id"]
).reset_index(drop=True)


# Save cleaned dataset
df.to_csv(
    cleaned_file,
    index=False
)


print("\nData cleaning completed.")
print("Cleaned shape:", df.shape)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)

print("\nCleaned dataset saved at:")
print(cleaned_file)
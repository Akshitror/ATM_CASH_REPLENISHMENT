import os
import sqlite3

import pandas as pd


# ------------------------------------------------
# Project paths
# ------------------------------------------------

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

csv_path = os.path.join(
    project_root,
    "data",
    "atm_cash_data_cleaned.csv"
)

database_folder = os.path.join(
    project_root,
    "database"
)

os.makedirs(database_folder, exist_ok=True)

database_path = os.path.join(
    database_folder,
    "atm_replenishment.db"
)


# ------------------------------------------------
# Load cleaned dataset
# ------------------------------------------------

df = pd.read_csv(csv_path)

print("Dataset loaded successfully.")
print("Records found:", len(df))


# ------------------------------------------------
# Fix missing values
# ------------------------------------------------

text_columns = [
    "atm_id",
    "date",
    "city",
    "location_type",
    "day_of_week",
    "festival"
]

for column in text_columns:
    if column in df.columns:
        df[column] = df[column].fillna("None")


numeric_columns = [
    "month",
    "is_weekend",
    "is_holiday",
    "temperature",
    "transaction_count",
    "average_withdrawal",
    "withdrawal_amount",
    "deposit_amount",
    "opening_cash",
    "cash_remaining",
    "cash_out",
    "replenishment_required",
    "next_day_cash_requirement",
    "year",
    "day",
    "day_of_year"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if df[column].isnull().sum() > 0:
            df[column] = df[column].fillna(
                df[column].median()
            )


# Convert binary and integer columns
integer_columns = [
    "record_id",
    "month",
    "is_weekend",
    "is_holiday",
    "transaction_count",
    "cash_out",
    "replenishment_required",
    "year",
    "day",
    "day_of_year"
]

for column in integer_columns:
    if column in df.columns:
        df[column] = df[column].astype(int)


print("\nMissing values before database insertion:")
print(df.isnull().sum())


# ------------------------------------------------
# Remove old database if it exists
# ------------------------------------------------

if os.path.exists(database_path):
    os.remove(database_path)
    print("\nOld database removed.")


# ------------------------------------------------
# Connect to SQLite
# ------------------------------------------------

connection = sqlite3.connect(database_path)
cursor = connection.cursor()


# ------------------------------------------------
# Create ATM records table
# ------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS atm_records (
    record_id INTEGER PRIMARY KEY,
    atm_id TEXT NOT NULL,
    date TEXT NOT NULL,
    city TEXT NOT NULL,
    location_type TEXT NOT NULL,
    day_of_week TEXT NOT NULL,
    month INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL,
    is_holiday INTEGER NOT NULL,
    festival TEXT NOT NULL,
    temperature REAL NOT NULL,
    transaction_count INTEGER NOT NULL,
    average_withdrawal REAL NOT NULL,
    withdrawal_amount REAL NOT NULL,
    deposit_amount REAL NOT NULL,
    opening_cash REAL NOT NULL,
    cash_remaining REAL NOT NULL,
    cash_out INTEGER NOT NULL,
    replenishment_required INTEGER NOT NULL,
    next_day_cash_requirement REAL NOT NULL,
    year INTEGER,
    day INTEGER,
    day_of_year INTEGER
)
""")


# ------------------------------------------------
# Create prediction history table
# ------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_date TEXT NOT NULL,
    atm_id TEXT NOT NULL,
    city TEXT NOT NULL,
    location_type TEXT NOT NULL,
    opening_cash REAL NOT NULL,
    withdrawal_amount REAL NOT NULL,
    deposit_amount REAL NOT NULL,
    transaction_count INTEGER NOT NULL,
    average_withdrawal REAL NOT NULL,
    temperature REAL NOT NULL,
    day_of_week TEXT NOT NULL,
    month INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL,
    is_holiday INTEGER NOT NULL,
    festival TEXT NOT NULL,
    predicted_cash_requirement REAL NOT NULL,
    risk_level TEXT NOT NULL,
    recommendation TEXT NOT NULL
)
""")


# ------------------------------------------------
# Create indexes
# ------------------------------------------------

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_atm_id
ON atm_records(atm_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_city
ON atm_records(city)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_record_date
ON atm_records(date)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_prediction_atm
ON prediction_history(atm_id)
""")


# ------------------------------------------------
# Insert dataset into database
# ------------------------------------------------

df.to_sql(
    "atm_records",
    connection,
    if_exists="append",
    index=False
)


# ------------------------------------------------
# Save changes
# ------------------------------------------------

connection.commit()


# ------------------------------------------------
# Verify database
# ------------------------------------------------

cursor.execute("""
SELECT COUNT(*)
FROM atm_records
""")

record_count = cursor.fetchone()[0]


cursor.execute("""
SELECT COUNT(DISTINCT atm_id)
FROM atm_records
""")

atm_count = cursor.fetchone()[0]


cursor.execute("""
SELECT COUNT(DISTINCT city)
FROM atm_records
""")

city_count = cursor.fetchone()[0]


cursor.execute("""
SELECT COUNT(*)
FROM prediction_history
""")

prediction_count = cursor.fetchone()[0]


print("\n====================================")
print("DATABASE CREATED SUCCESSFULLY")
print("====================================")

print("Database location:", database_path)
print("ATM records inserted:", record_count)
print("Unique ATMs:", atm_count)
print("Cities:", city_count)
print("Prediction records:", prediction_count)


connection.close()

print("\nDatabase connection closed.")
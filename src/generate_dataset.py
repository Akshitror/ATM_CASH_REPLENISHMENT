import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)

NUMBER_OF_RECORDS = 12000
NUMBER_OF_ATMS = 40

cities = [
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Pune",
    "Jaipur"
]

locations = [
    "Market",
    "Mall",
    "Hospital",
    "Railway Station",
    "Bus Stand",
    "College",
    "Residential",
    "Business Area"
]

festivals = [
    "None",
    "Diwali",
    "Holi",
    "Eid",
    "Christmas",
    "Dussehra"
]

records = []

start_date = datetime(2024, 1, 1)

for record_id in range(1, NUMBER_OF_RECORDS + 1):

    atm_number = random.randint(1, NUMBER_OF_ATMS)
    atm_id = f"ATM{atm_number:03d}"

    date = start_date + timedelta(days=random.randint(0, 729))

    city = random.choice(cities)
    location_type = random.choice(locations)

    day_of_week = date.strftime("%A")
    month = date.month

    is_weekend = 1 if day_of_week in ["Saturday", "Sunday"] else 0
    is_holiday = np.random.choice([0, 1], p=[0.92, 0.08])

    festival = np.random.choice(
        festivals,
        p=[0.85, 0.04, 0.03, 0.03, 0.025, 0.025]
    )

    temperature = round(random.uniform(15, 42), 2)

    base_transactions = random.randint(80, 250)

    if location_type in ["Railway Station", "Mall", "Market", "Business Area"]:
        base_transactions += random.randint(50, 160)

    if is_weekend:
        base_transactions += random.randint(20, 80)

    if is_holiday:
        base_transactions += random.randint(30, 100)

    if festival != "None":
        base_transactions += random.randint(70, 180)

    transaction_count = max(base_transactions, 20)

    average_withdrawal = random.randint(1500, 6500)

    withdrawal_amount = transaction_count * average_withdrawal

    if month in [10, 11, 12]:
        withdrawal_amount *= random.uniform(1.1, 1.35)

    withdrawal_amount = round(withdrawal_amount, 2)

    deposit_amount = round(
        withdrawal_amount * random.uniform(0.03, 0.18),
        2
    )

    opening_cash = random.choice([
        1000000,
        1500000,
        2000000,
        2500000,
        3000000
    ])

    cash_remaining = opening_cash - withdrawal_amount + deposit_amount

    cash_remaining = max(round(cash_remaining, 2), 0)

    cash_out = 1 if cash_remaining <= 50000 else 0

    replenishment_required = 1 if cash_remaining < 500000 else 0

    next_day_cash_requirement = (
        withdrawal_amount
        * random.uniform(0.85, 1.20)
    )

    if is_weekend:
        next_day_cash_requirement *= 1.08

    if is_holiday:
        next_day_cash_requirement *= 1.12

    if festival != "None":
        next_day_cash_requirement *= 1.18

    next_day_cash_requirement = round(
        next_day_cash_requirement,
        2
    )

    records.append({
        "record_id": record_id,
        "atm_id": atm_id,
        "date": date.strftime("%Y-%m-%d"),
        "city": city,
        "location_type": location_type,
        "day_of_week": day_of_week,
        "month": month,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "festival": festival,
        "temperature": temperature,
        "transaction_count": transaction_count,
        "average_withdrawal": average_withdrawal,
        "withdrawal_amount": withdrawal_amount,
        "deposit_amount": deposit_amount,
        "opening_cash": opening_cash,
        "cash_remaining": cash_remaining,
        "cash_out": cash_out,
        "replenishment_required": replenishment_required,
        "next_day_cash_requirement": next_day_cash_requirement
    })


df = pd.DataFrame(records)

# Add a few missing values intentionally for the cleaning stage
missing_columns = [
    "temperature",
    "average_withdrawal",
    "deposit_amount"
]

for column in missing_columns:
    missing_indices = np.random.choice(
        df.index,
        size=40,
        replace=False
    )
    df.loc[missing_indices, column] = np.nan


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_root, "data")

os.makedirs(data_folder, exist_ok=True)

output_path = os.path.join(
    data_folder,
    "atm_cash_data_raw.csv"
)

df.to_csv(output_path, index=False)

print("Dataset created successfully.")
print("File location:", output_path)
print("Number of records:", len(df))
print("\nFirst five rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
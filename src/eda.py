import os
import pandas as pd
import matplotlib.pyplot as plt

# Project paths
project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

data_path = os.path.join(
    project_root,
    "data",
    "atm_cash_data_cleaned.csv"
)

graphs_path = os.path.join(
    project_root,
    "graphs"
)

os.makedirs(graphs_path, exist_ok=True)

# Load data
df = pd.read_csv(data_path)

print("Dataset Loaded Successfully")

# -----------------------------
# 1. Monthly Withdrawals
# -----------------------------
monthly = df.groupby("month")["withdrawal_amount"].sum()

plt.figure(figsize=(8,5))
monthly.plot(marker='o')
plt.title("Monthly Withdrawal Amount")
plt.xlabel("Month")
plt.ylabel("Withdrawal Amount")
plt.grid(True)

plt.savefig(os.path.join(graphs_path,
                         "monthly_withdrawals.png"))
plt.close()

# -----------------------------
# 2. City Withdrawals
# -----------------------------
city = df.groupby("city")["withdrawal_amount"].sum()

plt.figure(figsize=(8,5))
city.plot(kind="bar")
plt.title("City Wise Withdrawals")
plt.xlabel("City")
plt.ylabel("Withdrawal Amount")

plt.tight_layout()
plt.savefig(os.path.join(graphs_path,
                         "city_withdrawals.png"))
plt.close()

# -----------------------------
# 3. Weekend Comparison
# -----------------------------
weekend = df.groupby("is_weekend")[
    "withdrawal_amount"
].mean()

plt.figure(figsize=(6,4))
weekend.plot(kind="bar")
plt.title("Weekend vs Weekday")
plt.xticks([0,1],["Weekday","Weekend"],rotation=0)

plt.tight_layout()
plt.savefig(os.path.join(graphs_path,
                         "weekend.png"))
plt.close()

# -----------------------------
# 4. Holiday Comparison
# -----------------------------
holiday = df.groupby("is_holiday")[
    "withdrawal_amount"
].mean()

plt.figure(figsize=(6,4))
holiday.plot(kind="bar")
plt.title("Holiday Effect")
plt.xticks([0,1],["No","Yes"],rotation=0)

plt.tight_layout()
plt.savefig(os.path.join(graphs_path,
                         "holiday.png"))
plt.close()

# -----------------------------
# 5. Festival Comparison
# -----------------------------
festival = df.groupby("festival")[
    "withdrawal_amount"
].mean()

plt.figure(figsize=(8,5))
festival.plot(kind="bar")

plt.title("Festival Impact")

plt.tight_layout()

plt.savefig(os.path.join(graphs_path,
                         "festival.png"))
plt.close()

print("Graphs Generated Successfully")
print("Graphs saved in:", graphs_path)
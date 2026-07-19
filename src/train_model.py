import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ------------------------------------------------
# Paths
# ------------------------------------------------

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

data_path = os.path.join(
    project_root,
    "data",
    "atm_cash_data_cleaned.csv"
)

model_folder = os.path.join(
    project_root,
    "models"
)

os.makedirs(model_folder, exist_ok=True)

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

df = pd.read_csv(data_path)

print("Dataset Loaded Successfully")
print(df.shape)

# ------------------------------------------------
# Features and Target
# ------------------------------------------------

X = df.drop(columns=[
    "record_id",
    "date",
    "next_day_cash_requirement"
])

y = df["next_day_cash_requirement"]

# ------------------------------------------------
# Categorical & Numerical Columns
# ------------------------------------------------

categorical_columns = [
    "atm_id",
    "city",
    "location_type",
    "day_of_week",
    "festival"
]

numerical_columns = [
    col for col in X.columns
    if col not in categorical_columns
]

# ------------------------------------------------
# Preprocessing
# ------------------------------------------------

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numerical_columns),
    ("cat", categorical_transformer, categorical_columns)
])

# ------------------------------------------------
# Model
# ------------------------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# ------------------------------------------------
# Split Data
# ------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ------------------------------------------------
# Train
# ------------------------------------------------

print("\nTraining Model...")

pipeline.fit(X_train, y_train)

print("Training Completed!")

# ------------------------------------------------
# Predictions
# ------------------------------------------------

predictions = pipeline.predict(X_test)

# ------------------------------------------------
# Evaluation
# ------------------------------------------------

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, predictions)

print("\n========== MODEL RESULTS ==========")

print(f"MAE  : {mae:.2f}")
print(f"MSE  : {mse:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

# ------------------------------------------------
# Save Model
# ------------------------------------------------

joblib.dump(
    pipeline,
    os.path.join(model_folder, "atm_model.pkl")
)

print("\nModel Saved Successfully!")
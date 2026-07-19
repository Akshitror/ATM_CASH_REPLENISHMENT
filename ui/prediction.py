import os
import sqlite3
from datetime import datetime
import tkinter.messagebox as messagebox

import customtkinter as ctk
import joblib
import pandas as pd


class PredictionPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#0F172A")

        # ==================================================
        # PROJECT PATHS
        # ==================================================

        self.project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.model_path = os.path.join(
            self.project_root,
            "models",
            "atm_model.pkl"
        )

        self.data_path = os.path.join(
            self.project_root,
            "data",
            "atm_cash_data_cleaned.csv"
        )

        self.database_path = os.path.join(
            self.project_root,
            "database",
            "atm_replenishment.db"
        )

        # ==================================================
        # LOAD MODEL AND DATASET
        # ==================================================

        try:
            self.model = joblib.load(self.model_path)
            self.df = pd.read_csv(self.data_path)

        except Exception as error:
            messagebox.showerror(
                "Loading Error",
                f"Could not load the model or dataset.\n\n{error}"
            )
            return

        # These columns must match train_model.py
        self.feature_columns = [
            column
            for column in self.df.columns
            if column not in [
                "record_id",
                "date",
                "next_day_cash_requirement"
            ]
        ]

        self.categorical_columns = [
            "atm_id",
            "city",
            "location_type",
            "day_of_week",
            "festival"
        ]

        self.input_widgets = {}

        # ==================================================
        # BUILD PAGE
        # ==================================================

        self.create_header()
        self.create_content()

    # ==================================================
    # HEADER
    # ==================================================

    def create_header(self):

        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header_frame.pack(
            fill="x",
            padx=35,
            pady=(25, 10)
        )

        title = ctk.CTkLabel(
            header_frame,
            text="💰 Cash Prediction",
            font=("Segoe UI", 32, "bold"),
            text_color="#F8FAFC"
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header_frame,
            text=(
                "Enter the current ATM conditions to estimate "
                "the next-day cash requirement."
            ),
            font=("Segoe UI", 15),
            text_color="#94A3B8"
        )
        subtitle.pack(
            pady=(5, 0)
        )

    # ==================================================
    # MAIN CONTENT
    # ==================================================

    def create_content(self):

        content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        content_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        # ------------------------------------------------
        # Input section
        # ------------------------------------------------

        input_card = ctk.CTkFrame(
            content_frame,
            fg_color="#1E293B",
            corner_radius=18
        )
        input_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        input_title = ctk.CTkLabel(
            input_card,
            text="ATM Information",
            font=("Segoe UI", 21, "bold"),
            text_color="#F8FAFC"
        )
        input_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        self.scrollable_form = ctk.CTkScrollableFrame(
            input_card,
            fg_color="transparent"
        )
        self.scrollable_form.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.create_input_fields()

        # ------------------------------------------------
        # Result section
        # ------------------------------------------------

        result_container = ctk.CTkFrame(
            content_frame,
            width=370,
            fg_color="#1E293B",
            corner_radius=18
        )
        result_container.pack(
            side="right",
            fill="y",
            padx=(15, 0)
        )

        result_container.pack_propagate(False)

        result_heading = ctk.CTkLabel(
            result_container,
            text="Prediction Result",
            font=("Segoe UI", 22, "bold"),
            text_color="#F8FAFC"
        )
        result_heading.pack(
            pady=(35, 10)
        )

        result_description = ctk.CTkLabel(
            result_container,
            text="Recommended cash required\nfor the next day",
            font=("Segoe UI", 15),
            text_color="#94A3B8",
            justify="center"
        )
        result_description.pack(
            pady=(0, 25)
        )

        self.result_label = ctk.CTkLabel(
            result_container,
            text="₹ --",
            font=("Segoe UI", 38, "bold"),
            text_color="#22C55E"
        )
        self.result_label.pack(
            pady=20
        )

        self.risk_label = ctk.CTkLabel(
            result_container,
            text="Risk Level: --",
            font=("Segoe UI", 16, "bold"),
            text_color="#94A3B8"
        )
        self.risk_label.pack(
            pady=(5, 5)
        )

        self.status_label = ctk.CTkLabel(
            result_container,
            text=(
                "Fill in the ATM information\n"
                "and click Predict Cash."
            ),
            font=("Segoe UI", 14),
            text_color="#94A3B8",
            justify="center",
            wraplength=300
        )
        self.status_label.pack(
            pady=10
        )

        predict_button = ctk.CTkButton(
            result_container,
            text="Predict Cash",
            width=280,
            height=48,
            corner_radius=10,
            font=("Segoe UI", 17, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.predict_cash
        )
        predict_button.pack(
            pady=(35, 12)
        )

        reset_button = ctk.CTkButton(
            result_container,
            text="Reset Fields",
            width=280,
            height=42,
            corner_radius=10,
            font=("Segoe UI", 15),
            fg_color="#334155",
            hover_color="#475569",
            command=self.reset_fields
        )
        reset_button.pack(
            pady=5
        )

    # ==================================================
    # CREATE INPUT FIELDS
    # ==================================================

    def create_input_fields(self):

        for index, column in enumerate(
            self.feature_columns
        ):

            row = index // 2
            col = index % 2

            field_frame = ctk.CTkFrame(
                self.scrollable_form,
                fg_color="transparent"
            )
            field_frame.grid(
                row=row,
                column=col,
                padx=12,
                pady=9,
                sticky="ew"
            )

            self.scrollable_form.grid_columnconfigure(
                col,
                weight=1
            )

            display_name = (
                column
                .replace("_", " ")
                .title()
            )

            label = ctk.CTkLabel(
                field_frame,
                text=display_name,
                font=("Segoe UI", 14, "bold"),
                text_color="#CBD5E1"
            )
            label.pack(
                anchor="w",
                pady=(0, 6)
            )

            if column in self.categorical_columns:

                values = (
                    self.df[column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                values = sorted(values)

                widget = ctk.CTkComboBox(
                    field_frame,
                    values=values,
                    width=245,
                    height=38,
                    state="readonly"
                )

                if values:
                    widget.set(values[0])

            else:

                widget = ctk.CTkEntry(
                    field_frame,
                    width=245,
                    height=38,
                    placeholder_text=(
                        f"Enter {display_name.lower()}"
                    )
                )

                median_value = pd.to_numeric(
                    self.df[column],
                    errors="coerce"
                ).median()

                if pd.notna(median_value):

                    widget.insert(
                        0,
                        str(
                            round(
                                float(median_value),
                                2
                            )
                        )
                    )

            widget.pack(
                fill="x"
            )

            self.input_widgets[column] = widget

    # ==================================================
    # PREDICTION
    # ==================================================

    def predict_cash(self):

        try:
            input_data = {}

            for column in self.feature_columns:

                widget = self.input_widgets[column]
                value = widget.get().strip()

                if value == "":

                    raise ValueError(
                        f"Please enter a value for "
                        f"{column.replace('_', ' ').title()}."
                    )

                if column in self.categorical_columns:

                    input_data[column] = value

                else:

                    input_data[column] = float(value)

            prediction_df = pd.DataFrame(
                [input_data],
                columns=self.feature_columns
            )

            prediction = float(
                self.model.predict(
                    prediction_df
                )[0]
            )

            prediction = max(
                0,
                prediction
            )

            risk_level, recommendation = (
                self.calculate_risk_and_recommendation(
                    input_data,
                    prediction
                )
            )

            self.result_label.configure(
                text=self.format_indian_currency(
                    prediction
                ),
                text_color="#22C55E"
            )

            self.risk_label.configure(
                text=f"Risk Level: {risk_level}",
                text_color=self.get_risk_color(
                    risk_level
                )
            )

            self.status_label.configure(
                text=(
                    f"{recommendation}\n\n"
                    "Prediction saved to history."
                ),
                text_color="#22C55E"
            )

            self.save_prediction(
                input_data,
                prediction,
                risk_level,
                recommendation
            )

        except ValueError as error:

            self.result_label.configure(
                text="₹ --",
                text_color="#EF4444"
            )

            self.risk_label.configure(
                text="Risk Level: --",
                text_color="#94A3B8"
            )

            self.status_label.configure(
                text=str(error),
                text_color="#EF4444"
            )

        except Exception as error:

            self.result_label.configure(
                text="Prediction Error",
                text_color="#EF4444"
            )

            self.risk_label.configure(
                text="Risk Level: --",
                text_color="#94A3B8"
            )

            self.status_label.configure(
                text=str(error),
                text_color="#EF4444"
            )

    # ==================================================
    # RISK AND RECOMMENDATION
    # ==================================================

    def calculate_risk_and_recommendation(
        self,
        input_data,
        prediction
    ):

        opening_cash = float(
            input_data.get(
                "opening_cash",
                0
            )
        )

        cash_remaining = float(
            input_data.get(
                "cash_remaining",
                0
            )
        )

        refill_amount = max(
            0,
            prediction - cash_remaining
        )

        if prediction <= 0 or refill_amount <= 0:

            return (
                "Low",
                "Current ATM cash is sufficient. "
                "Continue normal monitoring."
            )

        shortage_percentage = (
            refill_amount / prediction
        ) * 100

        if (
            cash_remaining <= 0
            or shortage_percentage >= 60
        ):

            return (
                "High",
                "Immediate cash replenishment is recommended."
            )

        if shortage_percentage >= 30:

            return (
                "Medium",
                "Schedule cash replenishment within 24 hours."
            )

        if opening_cash < prediction:

            return (
                "Low",
                "Plan a routine replenishment within 48 hours."
            )

        return (
            "Low",
            "Current ATM cash position is stable."
        )

    def get_risk_color(self, risk_level):

        risk = risk_level.lower()

        if risk == "high":
            return "#EF4444"

        if risk == "medium":
            return "#F59E0B"

        return "#22C55E"

    # ==================================================
    # SAVE PREDICTION TO SQLITE
    # ==================================================

    def save_prediction(
        self,
        input_data,
        prediction,
        risk_level,
        recommendation
    ):

        connection = None

        try:
            connection = sqlite3.connect(
                self.database_path
            )

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO prediction_history (
                    prediction_date,
                    atm_id,
                    city,
                    location_type,
                    opening_cash,
                    withdrawal_amount,
                    deposit_amount,
                    transaction_count,
                    average_withdrawal,
                    temperature,
                    day_of_week,
                    month,
                    is_weekend,
                    is_holiday,
                    festival,
                    predicted_cash_requirement,
                    risk_level,
                    recommendation
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    str(
                        input_data.get(
                            "atm_id",
                            ""
                        )
                    ),
                    str(
                        input_data.get(
                            "city",
                            ""
                        )
                    ),
                    str(
                        input_data.get(
                            "location_type",
                            ""
                        )
                    ),
                    float(
                        input_data.get(
                            "opening_cash",
                            0
                        )
                    ),
                    float(
                        input_data.get(
                            "withdrawal_amount",
                            0
                        )
                    ),
                    float(
                        input_data.get(
                            "deposit_amount",
                            0
                        )
                    ),
                    int(
                        float(
                            input_data.get(
                                "transaction_count",
                                0
                            )
                        )
                    ),
                    float(
                        input_data.get(
                            "average_withdrawal",
                            0
                        )
                    ),
                    float(
                        input_data.get(
                            "temperature",
                            0
                        )
                    ),
                    str(
                        input_data.get(
                            "day_of_week",
                            ""
                        )
                    ),
                    int(
                        float(
                            input_data.get(
                                "month",
                                0
                            )
                        )
                    ),
                    int(
                        float(
                            input_data.get(
                                "is_weekend",
                                0
                            )
                        )
                    ),
                    int(
                        float(
                            input_data.get(
                                "is_holiday",
                                0
                            )
                        )
                    ),
                    str(
                        input_data.get(
                            "festival",
                            ""
                        )
                    ),
                    float(prediction),
                    risk_level,
                    recommendation
                )
            )

            connection.commit()

        except Exception as error:

            messagebox.showwarning(
                "History Warning",
                (
                    "The prediction was completed, but it "
                    "could not be saved to history.\n\n"
                    f"{error}"
                )
            )

        finally:

            if connection is not None:
                connection.close()

    # ==================================================
    # RESET FIELDS
    # ==================================================

    def reset_fields(self):

        for column, widget in self.input_widgets.items():

            if column in self.categorical_columns:

                values = (
                    self.df[column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                values = sorted(values)

                if values:
                    widget.set(values[0])

            else:

                widget.delete(
                    0,
                    "end"
                )

                median_value = pd.to_numeric(
                    self.df[column],
                    errors="coerce"
                ).median()

                if pd.notna(median_value):

                    widget.insert(
                        0,
                        str(
                            round(
                                float(median_value),
                                2
                            )
                        )
                    )

        self.result_label.configure(
            text="₹ --",
            text_color="#22C55E"
        )

        self.risk_label.configure(
            text="Risk Level: --",
            text_color="#94A3B8"
        )

        self.status_label.configure(
            text=(
                "Fill in the ATM information\n"
                "and click Predict Cash."
            ),
            text_color="#94A3B8"
        )

    # ==================================================
    # INDIAN CURRENCY FORMAT
    # ==================================================

    def format_indian_currency(self, amount):

        try:
            amount = round(
                float(amount)
            )

            negative = amount < 0
            amount = abs(amount)

            number_string = str(amount)

            if len(number_string) <= 3:

                formatted = number_string

            else:

                last_three = number_string[-3:]
                remaining = number_string[:-3]

                groups = []

                while len(remaining) > 2:

                    groups.insert(
                        0,
                        remaining[-2:]
                    )

                    remaining = remaining[:-2]

                if remaining:

                    groups.insert(
                        0,
                        remaining
                    )

                formatted = (
                    ",".join(groups)
                    + ","
                    + last_three
                )

            if negative:
                formatted = "-" + formatted

            return f"₹ {formatted}"

        except Exception:
            return "₹ 0"
import os
from datetime import datetime

import customtkinter as ctk
import joblib
import pandas as pd
from tkinter import messagebox


class DashboardPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#0F172A")

        self.project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.data_path = os.path.join(
            self.project_root,
            "data",
            "atm_cash_data_cleaned.csv"
        )

        self.model_path = os.path.join(
            self.project_root,
            "models",
            "atm_model.pkl"
        )

        self.df = None
        self.model = None
        self.dashboard_df = None

        try:
            self.df = pd.read_csv(self.data_path)
            self.model = joblib.load(self.model_path)

        except Exception as error:
            messagebox.showerror(
                "Dashboard Error",
                f"Could not load the dataset or model.\n\n{error}"
            )

        self.create_header()
        self.create_summary_cards()
        self.create_main_content()

        if self.df is not None and self.model is not None:
            self.generate_dashboard_data()

    # ==================================================
    # HEADER
    # ==================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_frame.pack(side="left")

        title = ctk.CTkLabel(
            title_frame,
            text="🏦 ATM Cash Replenishment Dashboard",
            font=("Segoe UI", 30, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_frame,
            text=(
                "Live overview of ATM cash availability, "
                "replenishment needs and model recommendations."
            ),
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        )
        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

        self.clock = ctk.CTkLabel(
            header,
            text="",
            font=("Segoe UI", 15, "bold"),
            text_color="#CBD5E1"
        )
        self.clock.pack(
            side="right",
            padx=10
        )

        self.update_clock()

    def update_clock(self):

        current_time = datetime.now().strftime(
            "%d %b %Y  |  %I:%M:%S %p"
        )

        self.clock.configure(
            text=current_time
        )

        self.after(
            1000,
            self.update_clock
        )

    # ==================================================
    # SUMMARY CARDS
    # ==================================================

    def create_summary_cards(self):

        self.card_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.card_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        for column in range(5):
            self.card_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.total_atms_value = self.create_card(
            column=0,
            title="Total ATMs",
            icon="🏧",
            color="#38BDF8"
        )

        self.need_refill_value = self.create_card(
            column=1,
            title="Need Refill",
            icon="⚠️",
            color="#F97316"
        )

        self.high_priority_value = self.create_card(
            column=2,
            title="High Priority",
            icon="🔴",
            color="#EF4444"
        )

        self.total_cash_value = self.create_card(
            column=3,
            title="Refill Cash",
            icon="💰",
            color="#22C55E"
        )

        self.model_value = self.create_card(
            column=4,
            title="Model",
            icon="🤖",
            color="#A78BFA"
        )

    def create_card(
        self,
        column,
        title,
        icon,
        color
    ):

        card = ctk.CTkFrame(
            self.card_frame,
            fg_color="#1E293B",
            corner_radius=16
        )
        card.grid(
            row=0,
            column=column,
            padx=7,
            pady=5,
            sticky="nsew"
        )

        heading = ctk.CTkLabel(
            card,
            text=f"{icon}  {title}",
            font=("Segoe UI", 14, "bold"),
            text_color="#CBD5E1"
        )
        heading.pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        value = ctk.CTkLabel(
            card,
            text="--",
            font=("Segoe UI", 23, "bold"),
            text_color=color
        )
        value.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        return value

    # ==================================================
    # MAIN CONTENT
    # ==================================================

    def create_main_content(self):

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 20)
        )

        content.grid_columnconfigure(
            0,
            weight=3
        )

        content.grid_columnconfigure(
            1,
            weight=2
        )

        content.grid_rowconfigure(
            0,
            weight=1
        )

        # ------------------------------------------
        # Urgent ATM table
        # ------------------------------------------

        urgent_card = ctk.CTkFrame(
            content,
            fg_color="#1E293B",
            corner_radius=16
        )
        urgent_card.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="nsew"
        )

        urgent_title = ctk.CTkLabel(
            urgent_card,
            text="Top Urgent ATM Replenishments",
            font=("Segoe UI", 20, "bold"),
            text_color="#F8FAFC"
        )
        urgent_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.urgent_scroll = ctk.CTkScrollableFrame(
            urgent_card,
            fg_color="transparent"
        )
        self.urgent_scroll.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.table_columns = [
            ("ATM ID", 90),
            ("City", 115),
            ("Cash Left", 125),
            ("Predicted Need", 145),
            ("Refill Amount", 140),
            ("Priority", 105)
        ]

        for index, (_, width) in enumerate(
            self.table_columns
        ):
            self.urgent_scroll.grid_columnconfigure(
                index,
                weight=1,
                minsize=width
            )

        self.create_table_header()

        # ------------------------------------------
        # Recommendation panel
        # ------------------------------------------

        recommendation_card = ctk.CTkFrame(
            content,
            fg_color="#1E293B",
            corner_radius=16
        )
        recommendation_card.grid(
            row=0,
            column=1,
            padx=(10, 0),
            sticky="nsew"
        )

        recommendation_title = ctk.CTkLabel(
            recommendation_card,
            text="AI Recommendations",
            font=("Segoe UI", 20, "bold"),
            text_color="#F8FAFC"
        )
        recommendation_title.pack(
            anchor="w",
            padx=22,
            pady=(18, 8)
        )

        recommendation_subtitle = ctk.CTkLabel(
            recommendation_card,
            text="Current operational insights",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )
        recommendation_subtitle.pack(
            anchor="w",
            padx=22
        )

        self.recommendation_box = ctk.CTkTextbox(
            recommendation_card,
            fg_color="#172033",
            corner_radius=12,
            font=("Segoe UI", 15),
            text_color="#E2E8F0",
            wrap="word"
        )
        self.recommendation_box.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        self.recommendation_box.configure(
            state="disabled"
        )

    def create_table_header(self):

        for index, (heading, _) in enumerate(
            self.table_columns
        ):

            label = ctk.CTkLabel(
                self.urgent_scroll,
                text=heading,
                height=40,
                fg_color="#334155",
                corner_radius=5,
                font=("Segoe UI", 12, "bold"),
                text_color="#F8FAFC"
            )
            label.grid(
                row=0,
                column=index,
                padx=3,
                pady=3,
                sticky="nsew"
            )

    # ==================================================
    # DASHBOARD DATA
    # ==================================================

    def generate_dashboard_data(self):

        try:
            data = self.df.copy()

            data["date"] = pd.to_datetime(
                data["date"],
                errors="coerce"
            )

            latest_data = (
                data
                .sort_values("date")
                .groupby("atm_id", as_index=False)
                .tail(1)
                .copy()
            )

            excluded_columns = [
                "record_id",
                "date",
                "next_day_cash_requirement"
            ]

            feature_columns = [
                column
                for column in data.columns
                if column not in excluded_columns
            ]

            prediction_input = latest_data[
                feature_columns
            ].copy()

            predictions = self.model.predict(
                prediction_input
            )

            latest_data["predicted_requirement"] = (
                pd.Series(
                    predictions,
                    index=latest_data.index
                )
                .clip(lower=0)
            )

            latest_data["cash_remaining"] = pd.to_numeric(
                latest_data["cash_remaining"],
                errors="coerce"
            ).fillna(0)

            latest_data["recommended_refill"] = (
                latest_data["predicted_requirement"]
                - latest_data["cash_remaining"]
            ).clip(lower=0)

            latest_data["priority"] = latest_data.apply(
                self.calculate_priority,
                axis=1
            )

            priority_order = {
                "High": 1,
                "Medium": 2,
                "Low": 3,
                "No Refill": 4
            }

            latest_data["priority_order"] = (
                latest_data["priority"]
                .map(priority_order)
                .fillna(5)
            )

            latest_data = latest_data.sort_values(
                by=[
                    "priority_order",
                    "recommended_refill"
                ],
                ascending=[
                    True,
                    False
                ]
            )

            self.dashboard_df = latest_data.reset_index(
                drop=True
            )

            self.update_summary_cards()
            self.display_urgent_atms()
            self.update_recommendations()

        except Exception as error:
            messagebox.showerror(
                "Dashboard Error",
                f"Could not generate dashboard data.\n\n{error}"
            )

    # ==================================================
    # PRIORITY
    # ==================================================

    def calculate_priority(self, row):

        predicted = float(
            row["predicted_requirement"]
        )

        remaining = float(
            row["cash_remaining"]
        )

        refill = float(
            row["recommended_refill"]
        )

        if predicted <= 0 or refill <= 0:
            return "No Refill"

        shortage_percentage = (
            refill / predicted
        ) * 100

        if remaining <= 0 or shortage_percentage >= 60:
            return "High"

        if shortage_percentage >= 30:
            return "Medium"

        return "Low"

    # ==================================================
    # SUMMARY UPDATE
    # ==================================================

    def update_summary_cards(self):

        total_atms = len(self.dashboard_df)

        need_refill = len(
            self.dashboard_df[
                self.dashboard_df["recommended_refill"] > 0
            ]
        )

        high_priority = len(
            self.dashboard_df[
                self.dashboard_df["priority"] == "High"
            ]
        )

        total_cash = self.dashboard_df[
            "recommended_refill"
        ].sum()

        self.total_atms_value.configure(
            text=str(total_atms)
        )

        self.need_refill_value.configure(
            text=str(need_refill)
        )

        self.high_priority_value.configure(
            text=str(high_priority)
        )

        self.total_cash_value.configure(
            text=self.format_compact_currency(
                total_cash
            )
        )

        self.model_value.configure(
            text="Random Forest"
        )

    # ==================================================
    # URGENT ATM TABLE
    # ==================================================

    def display_urgent_atms(self):

        for widget in self.urgent_scroll.winfo_children():

            grid_info = widget.grid_info()

            if grid_info:
                row_number = int(
                    grid_info.get("row", 0)
                )

                if row_number > 0:
                    widget.destroy()

        urgent_data = self.dashboard_df[
            self.dashboard_df["recommended_refill"] > 0
        ].head(10)

        if urgent_data.empty:

            label = ctk.CTkLabel(
                self.urgent_scroll,
                text="No ATMs currently require replenishment.",
                font=("Segoe UI", 15),
                text_color="#22C55E"
            )
            label.grid(
                row=1,
                column=0,
                columnspan=len(self.table_columns),
                pady=40
            )

            return

        for row_index, (_, row) in enumerate(
            urgent_data.iterrows(),
            start=1
        ):

            priority = str(row["priority"])

            if priority == "High":
                priority_text = "🔴 HIGH"
                priority_color = "#EF4444"

            elif priority == "Medium":
                priority_text = "🟡 MEDIUM"
                priority_color = "#F59E0B"

            else:
                priority_text = "🔵 LOW"
                priority_color = "#38BDF8"

            values = [
                str(row["atm_id"]),
                str(row["city"]),
                self.format_indian_currency(
                    row["cash_remaining"]
                ),
                self.format_indian_currency(
                    row["predicted_requirement"]
                ),
                self.format_indian_currency(
                    row["recommended_refill"]
                ),
                priority_text
            ]

            row_color = (
                "#263449"
                if row_index % 2 == 0
                else "#1E293B"
            )

            for column_index, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.urgent_scroll,
                    text=value,
                    height=40,
                    fg_color=row_color,
                    corner_radius=4,
                    font=(
                        ("Segoe UI", 11, "bold")
                        if column_index == 5
                        else ("Segoe UI", 11)
                    ),
                    text_color=(
                        priority_color
                        if column_index == 5
                        else "#E2E8F0"
                    )
                )

                label.grid(
                    row=row_index,
                    column=column_index,
                    padx=3,
                    pady=2,
                    sticky="nsew"
                )

    # ==================================================
    # RECOMMENDATIONS
    # ==================================================

    def update_recommendations(self):

        urgent_data = self.dashboard_df[
            self.dashboard_df["recommended_refill"] > 0
        ]

        high_priority = urgent_data[
            urgent_data["priority"] == "High"
        ]

        total_cash = urgent_data[
            "recommended_refill"
        ].sum()

        recommendations = []

        if not high_priority.empty:

            top_atm = high_priority.iloc[0]

            recommendations.append(
                f"🔴 {top_atm['atm_id']} in "
                f"{top_atm['city']} requires immediate refill."
            )

            recommendations.append(
                f"💰 Recommended refill for "
                f"{top_atm['atm_id']}: "
                f"{self.format_indian_currency(top_atm['recommended_refill'])}."
            )

        recommendations.append(
            f"⚠️ {len(urgent_data)} ATMs currently require replenishment."
        )

        recommendations.append(
            f"🚨 {len(high_priority)} ATMs are marked as high priority."
        )

        recommendations.append(
            f"🏦 Total estimated refill cash: "
            f"{self.format_compact_currency(total_cash)}."
        )

        zero_cash_atms = urgent_data[
            urgent_data["cash_remaining"] <= 0
        ]

        if not zero_cash_atms.empty:
            recommendations.append(
                f"❗ {len(zero_cash_atms)} ATMs have zero cash remaining."
            )

        weekend_records = self.dashboard_df[
            self.dashboard_df["is_weekend"] == 1
        ]

        if len(weekend_records) > 0:
            recommendations.append(
                "📅 Weekend demand conditions are present in the latest data."
            )

        recommendations.append(
            "✅ Review the Optimizer page before scheduling refill vehicles."
        )

        self.recommendation_box.configure(
            state="normal"
        )

        self.recommendation_box.delete(
            "0.0",
            "end"
        )

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):
            self.recommendation_box.insert(
                "end",
                f"{index}. {recommendation}\n\n"
            )

        self.recommendation_box.configure(
            state="disabled"
        )

    # ==================================================
    # CURRENCY FORMAT
    # ==================================================

    def format_compact_currency(self, amount):

        try:
            amount = float(amount)

            if amount >= 10_000_000:
                return f"₹ {amount / 10_000_000:.2f} Cr"

            if amount >= 100_000:
                return f"₹ {amount / 100_000:.2f} L"

            if amount >= 1_000:
                return f"₹ {amount / 1_000:.1f} K"

            return f"₹ {amount:,.0f}"

        except Exception:
            return "₹ 0"

    def format_indian_currency(self, amount):

        try:
            amount = round(float(amount))

            negative = amount < 0
            amount = abs(amount)

            amount_string = str(amount)

            if len(amount_string) <= 3:
                formatted = amount_string

            else:
                last_three = amount_string[-3:]
                remaining = amount_string[:-3]

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
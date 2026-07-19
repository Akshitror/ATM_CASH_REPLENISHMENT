import os
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
import joblib
import pandas as pd


class OptimizerPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#0F172A")

        # ==================================================
        # PROJECT PATHS
        # ==================================================

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

        # ==================================================
        # VARIABLES
        # ==================================================

        self.model = None
        self.df = None
        self.optimizer_df = None
        self.filtered_df = None

        self.search_var = ctk.StringVar()
        self.city_var = ctk.StringVar(value="All Cities")
        self.priority_var = ctk.StringVar(value="All Priorities")

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

        # ==================================================
        # BUILD PAGE
        # ==================================================

        self.create_header()
        self.create_summary_cards()
        self.create_filter_section()
        self.create_table_section()

        self.generate_optimizer_data()

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
            pady=(18, 8)
        )

        title = ctk.CTkLabel(
            header,
            text="🚚 ATM Replenishment Optimizer",
            font=("Segoe UI", 30, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Identify ATMs requiring cash replenishment "
                "using machine-learning predictions."
            ),
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        )
        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

    # ==================================================
    # SUMMARY CARDS
    # ==================================================

    def create_summary_cards(self):

        self.summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.summary_frame.pack(
            fill="x",
            padx=30,
            pady=8
        )

        for column in range(4):
            self.summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.total_atms_value = self.create_card(
            parent=self.summary_frame,
            column=0,
            title="Total ATMs",
            icon="🏧",
            text_color="#38BDF8"
        )

        self.refill_atms_value = self.create_card(
            parent=self.summary_frame,
            column=1,
            title="Need Refill",
            icon="⚠️",
            text_color="#F97316"
        )

        self.high_priority_value = self.create_card(
            parent=self.summary_frame,
            column=2,
            title="High Priority",
            icon="🔴",
            text_color="#EF4444"
        )

        self.total_cash_value = self.create_card(
            parent=self.summary_frame,
            column=3,
            title="Total Refill Cash",
            icon="💰",
            text_color="#22C55E"
        )

    def create_card(
        self,
        parent,
        column,
        title,
        icon,
        text_color
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=15
        )
        card.grid(
            row=0,
            column=column,
            padx=8,
            pady=4,
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
            pady=(14, 4)
        )

        value = ctk.CTkLabel(
            card,
            text="--",
            font=("Segoe UI", 25, "bold"),
            text_color=text_color
        )
        value.pack(
            anchor="w",
            padx=18,
            pady=(0, 14)
        )

        return value

    # ==================================================
    # FILTER SECTION
    # ==================================================

    def create_filter_section(self):

        filter_frame = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=14
        )
        filter_frame.pack(
            fill="x",
            padx=30,
            pady=8
        )

        # Grid layout prevents buttons from getting cut off
        filter_frame.grid_columnconfigure(0, weight=3)
        filter_frame.grid_columnconfigure(1, weight=2)
        filter_frame.grid_columnconfigure(2, weight=2)
        filter_frame.grid_columnconfigure(3, weight=0)
        filter_frame.grid_columnconfigure(4, weight=0)
        filter_frame.grid_columnconfigure(5, weight=0)
        filter_frame.grid_columnconfigure(6, weight=0)

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            placeholder_text="Search ATM ID or city...",
            height=40
        )
        self.search_entry.grid(
            row=0,
            column=0,
            padx=(15, 7),
            pady=14,
            sticky="ew"
        )

        cities = (
            self.df["city"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        cities = ["All Cities"] + sorted(cities)

        self.city_menu = ctk.CTkComboBox(
            filter_frame,
            variable=self.city_var,
            values=cities,
            height=40,
            state="readonly"
        )
        self.city_menu.grid(
            row=0,
            column=1,
            padx=7,
            pady=14,
            sticky="ew"
        )

        self.priority_menu = ctk.CTkComboBox(
            filter_frame,
            variable=self.priority_var,
            values=[
                "All Priorities",
                "High",
                "Medium",
                "Low",
                "No Refill"
            ],
            height=40,
            state="readonly"
        )
        self.priority_menu.grid(
            row=0,
            column=2,
            padx=7,
            pady=14,
            sticky="ew"
        )

        apply_button = ctk.CTkButton(
            filter_frame,
            text="Apply Filters",
            width=130,
            height=40,
            font=("Segoe UI", 13, "bold"),
            command=self.apply_filters
        )
        apply_button.grid(
            row=0,
            column=3,
            padx=7,
            pady=14
        )

        reset_button = ctk.CTkButton(
            filter_frame,
            text="Reset",
            width=90,
            height=40,
            fg_color="#475569",
            hover_color="#64748B",
            command=self.reset_filters
        )
        reset_button.grid(
            row=0,
            column=4,
            padx=7,
            pady=14
        )

        export_button = ctk.CTkButton(
            filter_frame,
            text="Export Excel",
            width=120,
            height=40,
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            command=self.export_to_excel
        )
        export_button.grid(
            row=0,
            column=5,
            padx=7,
            pady=14
        )

        refresh_button = ctk.CTkButton(
            filter_frame,
            text="Refresh",
            width=100,
            height=40,
            fg_color="#059669",
            hover_color="#047857",
            command=self.generate_optimizer_data
        )
        refresh_button.grid(
            row=0,
            column=6,
            padx=(7, 15),
            pady=14
        )

        # Pressing Enter applies the filter
        self.search_entry.bind(
            "<Return>",
            lambda event: self.apply_filters()
        )

    # ==================================================
    # TABLE SECTION
    # ==================================================

    def create_table_section(self):

        table_card = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=15
        )
        table_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 20)
        )

        top_frame = ctk.CTkFrame(
            table_card,
            fg_color="transparent"
        )
        top_frame.pack(
            fill="x",
            padx=20,
            pady=(14, 8)
        )

        table_title = ctk.CTkLabel(
            top_frame,
            text="ATM Replenishment Priority List",
            font=("Segoe UI", 19, "bold"),
            text_color="#F8FAFC"
        )
        table_title.pack(side="left")

        self.record_count_label = ctk.CTkLabel(
            top_frame,
            text="0 records",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )
        self.record_count_label.pack(side="right")

        self.table_scroll = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent"
        )
        self.table_scroll.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.table_columns = [
            ("ATM ID", 100),
            ("City", 120),
            ("Cash Remaining", 145),
            ("Predicted Need", 145),
            ("Refill Amount", 145),
            ("Priority", 125),
            ("Recommended Visit", 155)
        ]

        for index, (_, width) in enumerate(
            self.table_columns
        ):
            self.table_scroll.grid_columnconfigure(
                index,
                weight=1,
                minsize=width
            )

        self.create_table_header()

    def create_table_header(self):

        for index, (heading, _) in enumerate(
            self.table_columns
        ):

            label = ctk.CTkLabel(
                self.table_scroll,
                text=heading,
                height=42,
                fg_color="#334155",
                corner_radius=5,
                font=("Segoe UI", 13, "bold"),
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
    # GENERATE OPTIMIZER DATA
    # ==================================================

    def generate_optimizer_data(self):

        try:
            data = self.df.copy()

            data["date"] = pd.to_datetime(
                data["date"],
                errors="coerce"
            )

            # Keep the most recent record of every ATM
            latest_data = (
                data
                .sort_values("date")
                .groupby("atm_id", as_index=False)
                .tail(1)
                .copy()
            )

            # These must match train_model.py
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
                pd.Series(predictions, index=latest_data.index)
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

            latest_data["recommended_visit"] = (
                latest_data["priority"]
                .apply(self.calculate_visit)
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

            self.optimizer_df = latest_data.reset_index(
                drop=True
            )

            self.filtered_df = self.optimizer_df.copy()

            self.update_summary_cards()
            self.display_table(self.filtered_df)

        except Exception as error:
            messagebox.showerror(
                "Optimizer Error",
                f"Could not generate recommendations.\n\n{error}"
            )

    # ==================================================
    # PRIORITY LOGIC
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

        if refill <= 0 or predicted <= 0:
            return "No Refill"

        shortage_percentage = (
            refill / predicted
        ) * 100

        # ATM has almost no cash or a very large shortage
        if remaining <= 0 or shortage_percentage >= 60:
            return "High"

        if shortage_percentage >= 30:
            return "Medium"

        return "Low"

    def calculate_visit(self, priority):

        if priority == "High":
            return "Today"

        if priority == "Medium":
            return "Within 24 Hours"

        if priority == "Low":
            return "Within 48 Hours"

        return "Not Required"

    # ==================================================
    # SUMMARY CARDS UPDATE
    # ==================================================

    def update_summary_cards(self):

        if self.optimizer_df is None:
            return

        total_atms = len(self.optimizer_df)

        refill_atms = len(
            self.optimizer_df[
                self.optimizer_df["recommended_refill"] > 0
            ]
        )

        high_priority = len(
            self.optimizer_df[
                self.optimizer_df["priority"] == "High"
            ]
        )

        total_cash = self.optimizer_df[
            "recommended_refill"
        ].sum()

        self.total_atms_value.configure(
            text=str(total_atms)
        )

        self.refill_atms_value.configure(
            text=str(refill_atms)
        )

        self.high_priority_value.configure(
            text=str(high_priority)
        )

        self.total_cash_value.configure(
            text=self.format_compact_currency(total_cash)
        )

    # ==================================================
    # DISPLAY TABLE
    # ==================================================

    def display_table(self, dataframe):

        # Remove all existing data rows but keep header
        for widget in self.table_scroll.winfo_children():

            grid_info = widget.grid_info()

            if grid_info:
                row_number = int(
                    grid_info.get("row", 0)
                )

                if row_number > 0:
                    widget.destroy()

        self.record_count_label.configure(
            text=f"{len(dataframe)} records"
        )

        if dataframe.empty:

            empty_label = ctk.CTkLabel(
                self.table_scroll,
                text="No matching ATM records found.",
                font=("Segoe UI", 15),
                text_color="#94A3B8"
            )
            empty_label.grid(
                row=1,
                column=0,
                columnspan=len(self.table_columns),
                pady=40
            )

            return

        display_data = dataframe.head(100)

        for row_index, (_, row) in enumerate(
            display_data.iterrows(),
            start=1
        ):

            priority = str(row["priority"])

            if priority == "High":
                priority_text = "🔴 HIGH"
                priority_color = "#EF4444"

            elif priority == "Medium":
                priority_text = "🟡 MEDIUM"
                priority_color = "#F59E0B"

            elif priority == "Low":
                priority_text = "🔵 LOW"
                priority_color = "#38BDF8"

            else:
                priority_text = "🟢 NO REFILL"
                priority_color = "#22C55E"

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
                priority_text,
                str(row["recommended_visit"])
            ]

            row_color = (
                "#263449"
                if row_index % 2 == 0
                else "#1E293B"
            )

            for column_index, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.table_scroll,
                    text=value,
                    height=39,
                    fg_color=row_color,
                    corner_radius=4,
                    font=(
                        ("Segoe UI", 12, "bold")
                        if column_index == 5
                        else ("Segoe UI", 12)
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
    # FILTERS
    # ==================================================

    def apply_filters(self):

        if self.optimizer_df is None:
            return

        filtered = self.optimizer_df.copy()

        search_text = (
            self.search_var.get()
            .strip()
            .lower()
        )

        selected_city = self.city_var.get()
        selected_priority = self.priority_var.get()

        if search_text:

            atm_match = (
                filtered["atm_id"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_text,
                    na=False,
                    regex=False
                )
            )

            city_match = (
                filtered["city"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_text,
                    na=False,
                    regex=False
                )
            )

            filtered = filtered[
                atm_match | city_match
            ]

        if selected_city != "All Cities":

            filtered = filtered[
                filtered["city"].astype(str)
                == selected_city
            ]

        if selected_priority != "All Priorities":

            filtered = filtered[
                filtered["priority"]
                == selected_priority
            ]

        self.filtered_df = filtered.copy()

        self.display_table(self.filtered_df)

    def reset_filters(self):

        self.search_var.set("")
        self.city_var.set("All Cities")
        self.priority_var.set("All Priorities")

        if self.optimizer_df is not None:

            self.filtered_df = self.optimizer_df.copy()

            self.display_table(
                self.filtered_df
            )

    # ==================================================
    # EXPORT REPORT
    # ==================================================

    def export_to_excel(self):

        if self.filtered_df is None or self.filtered_df.empty:

            messagebox.showwarning(
                "No Data",
                "There is no optimizer data available to export."
            )
            return

        default_name = (
            "atm_optimizer_report_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".xlsx"
        )

        save_path = filedialog.asksaveasfilename(
            title="Save Optimizer Report",
            defaultextension=".xlsx",
            initialfile=default_name,
            filetypes=[
                ("Excel Workbook", "*.xlsx")
            ]
        )

        if not save_path:
            return

        try:
            export_columns = [
                "atm_id",
                "city",
                "location_type",
                "cash_remaining",
                "predicted_requirement",
                "recommended_refill",
                "priority",
                "recommended_visit"
            ]

            available_columns = [
                column
                for column in export_columns
                if column in self.filtered_df.columns
            ]

            export_df = self.filtered_df[
                available_columns
            ].copy()

            export_df = export_df.rename(
                columns={
                    "atm_id": "ATM ID",
                    "city": "City",
                    "location_type": "Location Type",
                    "cash_remaining": "Cash Remaining",
                    "predicted_requirement": (
                        "Predicted Cash Requirement"
                    ),
                    "recommended_refill": (
                        "Recommended Refill Amount"
                    ),
                    "priority": "Priority",
                    "recommended_visit": (
                        "Recommended Visit"
                    )
                }
            )

            export_df.to_excel(
                save_path,
                index=False
            )

            messagebox.showinfo(
                "Export Successful",
                f"Optimizer report saved successfully.\n\n{save_path}"
            )

        except ImportError:

            messagebox.showerror(
                "Missing Package",
                "Install openpyxl using:\n\npip install openpyxl"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                f"Could not export the report.\n\n{error}"
            )

    # ==================================================
    # CURRENCY FORMATTING
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
                    groups.insert(0, remaining)

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
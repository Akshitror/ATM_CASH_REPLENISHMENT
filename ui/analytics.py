import os
from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AnalyticsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#0F172A")

        # ==================================================
        # PATHS AND VARIABLES
        # ==================================================

        self.project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.data_path = os.path.join(
            self.project_root,
            "data",
            "atm_cash_data_cleaned.csv"
        )

        self.df = None
        self.canvas = None
        self.current_figure = None

        # ==================================================
        # LOAD DATASET
        # ==================================================

        try:
            self.df = pd.read_csv(self.data_path)

            self.df["date"] = pd.to_datetime(
                self.df["date"],
                errors="coerce"
            )

        except Exception as error:
            messagebox.showerror(
                "Analytics Error",
                f"Could not load the dataset.\n\n{error}"
            )
            return

        # ==================================================
        # BUILD PAGE
        # ==================================================

        self.create_header()
        self.create_summary_cards()
        self.create_chart_buttons()
        self.create_chart_area()

        self.show_monthly_withdrawals()

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
            text="📊 Live ATM Analytics",
            font=("Segoe UI", 30, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Explore live withdrawal patterns, ATM usage, "
                "festival impact and cash availability."
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

        summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        summary_frame.pack(
            fill="x",
            padx=30,
            pady=8
        )

        for column in range(4):
            summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

        total_withdrawal = pd.to_numeric(
            self.df["withdrawal_amount"],
            errors="coerce"
        ).fillna(0).sum()

        total_transactions = pd.to_numeric(
            self.df["transaction_count"],
            errors="coerce"
        ).fillna(0).sum()

        average_cash = pd.to_numeric(
            self.df["cash_remaining"],
            errors="coerce"
        ).fillna(0).mean()

        total_atms = self.df["atm_id"].nunique()

        cards = [
            (
                "Total ATMs",
                str(total_atms),
                "🏧",
                "#38BDF8"
            ),
            (
                "Transactions",
                self.format_compact_number(total_transactions),
                "📄",
                "#A78BFA"
            ),
            (
                "Total Withdrawals",
                self.format_compact_currency(total_withdrawal),
                "💸",
                "#F97316"
            ),
            (
                "Average Cash Left",
                self.format_compact_currency(average_cash),
                "💰",
                "#22C55E"
            )
        ]

        for column, card_data in enumerate(cards):

            title, value, icon, color = card_data

            card = ctk.CTkFrame(
                summary_frame,
                fg_color="#1E293B",
                corner_radius=15
            )
            card.grid(
                row=0,
                column=column,
                padx=7,
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

            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=("Segoe UI", 23, "bold"),
                text_color=color
            )
            value_label.pack(
                anchor="w",
                padx=18,
                pady=(0, 14)
            )

    # ==================================================
    # CHART BUTTONS
    # ==================================================

    def create_chart_buttons(self):

        button_card = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=14
        )
        button_card.pack(
            fill="x",
            padx=30,
            pady=8
        )

        buttons = [
            (
                "Monthly Trend",
                self.show_monthly_withdrawals
            ),
            (
                "City Analysis",
                self.show_city_withdrawals
            ),
            (
                "Top ATMs",
                self.show_top_atms
            ),
            (
                "Festival Impact",
                self.show_festival_impact
            ),
            (
                "Weekend Analysis",
                self.show_weekend_analysis
            ),
            (
                "Cash Distribution",
                self.show_cash_distribution
            )
        ]

        for index, (text, command) in enumerate(buttons):

            button = ctk.CTkButton(
                button_card,
                text=text,
                height=40,
                font=("Segoe UI", 13, "bold"),
                command=command
            )
            button.grid(
                row=0,
                column=index,
                padx=7,
                pady=14,
                sticky="ew"
            )

            button_card.grid_columnconfigure(
                index,
                weight=1
            )

    # ==================================================
    # CHART AREA
    # ==================================================

    def create_chart_area(self):

        self.chart_card = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=16
        )
        self.chart_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 20)
        )

        self.chart_title = ctk.CTkLabel(
            self.chart_card,
            text="Analytics Chart",
            font=("Segoe UI", 20, "bold"),
            text_color="#F8FAFC"
        )
        self.chart_title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.chart_description = ctk.CTkLabel(
            self.chart_card,
            text="",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )
        self.chart_description.pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )

        self.canvas_frame = ctk.CTkFrame(
            self.chart_card,
            fg_color="#FFFFFF",
            corner_radius=10
        )
        self.canvas_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(5, 18)
        )

    # ==================================================
    # DISPLAY FIGURE
    # ==================================================

    def display_figure(
        self,
        figure,
        title,
        description
    ):

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        if self.current_figure is not None:
            plt.close(self.current_figure)

        self.current_figure = figure

        self.chart_title.configure(
            text=title
        )

        self.chart_description.configure(
            text=description
        )

        figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(
            figure,
            master=self.canvas_frame
        )

        self.canvas.draw()

        canvas_widget = self.canvas.get_tk_widget()

        canvas_widget.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    # ==================================================
    # MONTHLY WITHDRAWAL TREND
    # ==================================================

    def show_monthly_withdrawals(self):

        try:
            data = self.df.copy()

            data["withdrawal_amount"] = pd.to_numeric(
                data["withdrawal_amount"],
                errors="coerce"
            ).fillna(0)

            monthly_data = (
                data.groupby("month")["withdrawal_amount"]
                .sum()
                .sort_index()
            )

            month_names = [
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug",
                "Sep", "Oct", "Nov", "Dec"
            ]

            labels = [
                month_names[int(month) - 1]
                if 1 <= int(month) <= 12
                else str(month)
                for month in monthly_data.index
            ]

            figure, axis = plt.subplots(
                figsize=(11, 5.5)
            )

            axis.plot(
                labels,
                monthly_data.values,
                marker="o",
                linewidth=2.5
            )

            axis.fill_between(
                labels,
                monthly_data.values,
                alpha=0.15
            )

            axis.set_title(
                "Monthly Withdrawal Trend",
                fontsize=15,
                fontweight="bold"
            )

            axis.set_xlabel("Month")
            axis.set_ylabel("Total Withdrawal Amount")
            axis.grid(
                True,
                alpha=0.25
            )

            axis.ticklabel_format(
                style="plain",
                axis="y"
            )

            self.display_figure(
                figure,
                "Monthly Withdrawal Trend",
                "Shows the total withdrawal amount recorded for each month."
            )

        except Exception as error:
            self.show_chart_error(error)

    # ==================================================
    # CITY-WISE WITHDRAWALS
    # ==================================================

    def show_city_withdrawals(self):

        try:
            data = self.df.copy()

            data["withdrawal_amount"] = pd.to_numeric(
                data["withdrawal_amount"],
                errors="coerce"
            ).fillna(0)

            city_data = (
                data.groupby("city")["withdrawal_amount"]
                .sum()
                .sort_values(ascending=False)
            )

            figure, axis = plt.subplots(
                figsize=(11, 5.5)
            )

            axis.bar(
                city_data.index.astype(str),
                city_data.values
            )

            axis.set_title(
                "City-wise Total Withdrawals",
                fontsize=15,
                fontweight="bold"
            )

            axis.set_xlabel("City")
            axis.set_ylabel("Withdrawal Amount")

            axis.tick_params(
                axis="x",
                rotation=30
            )

            axis.grid(
                axis="y",
                alpha=0.25
            )

            axis.ticklabel_format(
                style="plain",
                axis="y"
            )

            self.display_figure(
                figure,
                "City-wise Withdrawal Analysis",
                "Compares total cash withdrawals across all cities."
            )

        except Exception as error:
            self.show_chart_error(error)

    # ==================================================
    # TOP BUSY ATMS
    # ==================================================

    def show_top_atms(self):

        try:
            data = self.df.copy()

            data["transaction_count"] = pd.to_numeric(
                data["transaction_count"],
                errors="coerce"
            ).fillna(0)

            top_atms = (
                data.groupby("atm_id")["transaction_count"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .sort_values()
            )

            figure, axis = plt.subplots(
                figsize=(11, 5.5)
            )

            axis.barh(
                top_atms.index.astype(str),
                top_atms.values
            )

            axis.set_title(
                "Top 10 Busiest ATMs",
                fontsize=15,
                fontweight="bold"
            )

            axis.set_xlabel("Total Transactions")
            axis.set_ylabel("ATM ID")

            axis.grid(
                axis="x",
                alpha=0.25
            )

            self.display_figure(
                figure,
                "Top 10 Busiest ATMs",
                "Ranks ATMs by their total number of recorded transactions."
            )

        except Exception as error:
            self.show_chart_error(error)

    # ==================================================
    # FESTIVAL IMPACT
    # ==================================================

    def show_festival_impact(self):

        try:
            data = self.df.copy()

            data["withdrawal_amount"] = pd.to_numeric(
                data["withdrawal_amount"],
                errors="coerce"
            ).fillna(0)

            data["festival"] = (
                data["festival"]
                .fillna("No Festival")
                .astype(str)
            )

            festival_data = (
                data.groupby("festival")["withdrawal_amount"]
                .mean()
                .sort_values(ascending=False)
            )

            figure, axis = plt.subplots(
                figsize=(11, 5.5)
            )

            axis.bar(
                festival_data.index,
                festival_data.values
            )

            axis.set_title(
                "Average Withdrawal During Festivals",
                fontsize=15,
                fontweight="bold"
            )

            axis.set_xlabel("Festival")
            axis.set_ylabel("Average Withdrawal Amount")

            axis.tick_params(
                axis="x",
                rotation=25
            )

            axis.grid(
                axis="y",
                alpha=0.25
            )

            axis.ticklabel_format(
                style="plain",
                axis="y"
            )

            self.display_figure(
                figure,
                "Festival Impact Analysis",
                "Compares average withdrawal activity across festival periods."
            )

        except Exception as error:
            self.show_chart_error(error)

    # ==================================================
    # WEEKEND ANALYSIS
    # ==================================================

    def show_weekend_analysis(self):

        try:
            data = self.df.copy()

            data["withdrawal_amount"] = pd.to_numeric(
                data["withdrawal_amount"],
                errors="coerce"
            ).fillna(0)

            data["day_type"] = data["is_weekend"].apply(
                lambda value: (
                    "Weekend"
                    if int(value) == 1
                    else "Weekday"
                )
            )

            weekend_data = (
                data.groupby("day_type")["withdrawal_amount"]
                .mean()
            )

            labels = weekend_data.index.astype(str)
            values = weekend_data.values

            figure, axis = plt.subplots(
                figsize=(10, 5.5)
            )

            bars = axis.bar(
                labels,
                values,
                width=0.55
            )

            axis.set_title(
                "Weekend vs Weekday Withdrawals",
                fontsize=15,
                fontweight="bold"
            )

            axis.set_xlabel("Day Type")
            axis.set_ylabel("Average Withdrawal Amount")

            axis.grid(
                axis="y",
                alpha=0.25
            )

            axis.ticklabel_format(
                style="plain",
                axis="y"
            )

            for bar in bars:

                height = bar.get_height()

                axis.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    self.format_compact_currency(height),
                    ha="center",
                    va="bottom",
                    fontsize=10
                )

            self.display_figure(
                figure,
                "Weekend and Weekday Comparison",
                "Compares average ATM withdrawals on weekends and weekdays."
            )

        except Exception as error:
            self.show_chart_error(error)

    # ==================================================
    # CASH DISTRIBUTION
    # ==================================================

    def show_cash_distribution(self):

        try:
            cash_data = pd.to_numeric(
                self.df["cash_remaining"],
                errors="coerce"
            ).dropna()

            figure, axis = plt.subplots(
                figsize=(11, 5.5)
            )

            axis.hist(
                cash_data,
                bins=20,
                edgecolor="black",
                alpha=0.8
            )

            average_cash = cash_data.mean()

            axis.axvline(
                average_cash,
                linestyle="--",
                linewidth=2,
                label=(
                    "Average: "
                    + self.format_compact_currency(
                        average_cash
                    )
                )
            )

            axis.set_title(
                "Cash Remaining Distribution",
                fontsize=15,
                fontweight="bold"
            )

            axis.set_xlabel("Cash Remaining")
            axis.set_ylabel("Number of Records")

            axis.grid(
                axis="y",
                alpha=0.25
            )

            axis.ticklabel_format(
                style="plain",
                axis="x"
            )

            axis.legend()

            self.display_figure(
                figure,
                "Cash Remaining Distribution",
                "Shows how remaining ATM cash values are distributed across the dataset."
            )

        except Exception as error:
            self.show_chart_error(error)

    # ==================================================
    # ERROR HANDLING
    # ==================================================

    def show_chart_error(self, error):

        messagebox.showerror(
            "Chart Error",
            f"Could not generate the selected chart.\n\n{error}"
        )

    # ==================================================
    # NUMBER FORMATTING
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

    def format_compact_number(self, number):

        try:
            number = float(number)

            if number >= 10_000_000:
                return f"{number / 10_000_000:.2f} Cr"

            if number >= 100_000:
                return f"{number / 100_000:.2f} L"

            if number >= 1_000:
                return f"{number / 1_000:.1f} K"

            return f"{number:,.0f}"

        except Exception:
            return "0"
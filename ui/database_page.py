import os
import sqlite3
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pandas as pd


class DatabasePage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#0F172A")

        # ==================================================
        # DATABASE PATH
        # ==================================================

        self.project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.database_path = os.path.join(
            self.project_root,
            "database",
            "atm_replenishment.db"
        )

        # ==================================================
        # VARIABLES
        # ==================================================

        self.records_df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()

        self.search_var = ctk.StringVar()
        self.city_var = ctk.StringVar(value="All Cities")
        self.limit_var = ctk.StringVar(value="100")

        self.selected_record_id = None
        self.selected_row_widgets = []

        # ==================================================
        # BUILD PAGE
        # ==================================================

        self.create_header()
        self.create_summary_cards()
        self.create_filter_section()
        self.create_table_section()

        self.load_records()

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

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_frame.pack(side="left")

        title = ctk.CTkLabel(
            title_frame,
            text="🗄 ATM Database Viewer",
            font=("Segoe UI", 30, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_frame,
            text=(
                "View, search, export and manage ATM transaction "
                "records stored in SQLite."
            ),
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        )
        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

        self.connection_label = ctk.CTkLabel(
            header,
            text="● Database Connected",
            font=("Segoe UI", 14, "bold"),
            text_color="#22C55E"
        )
        self.connection_label.pack(
            side="right",
            padx=10
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

        self.total_records_value = self.create_card(
            column=0,
            title="Total Records",
            icon="📄",
            color="#38BDF8"
        )

        self.total_atms_value = self.create_card(
            column=1,
            title="Unique ATMs",
            icon="🏧",
            color="#A78BFA"
        )

        self.total_cities_value = self.create_card(
            column=2,
            title="Cities",
            icon="🏙",
            color="#F97316"
        )

        self.database_size_value = self.create_card(
            column=3,
            title="Database Size",
            icon="💾",
            color="#22C55E"
        )

    def create_card(
        self,
        column,
        title,
        icon,
        color
    ):

        card = ctk.CTkFrame(
            self.summary_frame,
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

        value = ctk.CTkLabel(
            card,
            text="--",
            font=("Segoe UI", 24, "bold"),
            text_color=color
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

        filter_frame.grid_columnconfigure(0, weight=3)
        filter_frame.grid_columnconfigure(1, weight=2)
        filter_frame.grid_columnconfigure(2, weight=1)

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            placeholder_text="Search ATM ID, city or location...",
            height=40
        )
        self.search_entry.grid(
            row=0,
            column=0,
            padx=(15, 7),
            pady=14,
            sticky="ew"
        )

        self.city_menu = ctk.CTkComboBox(
            filter_frame,
            variable=self.city_var,
            values=["All Cities"],
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

        self.limit_menu = ctk.CTkComboBox(
            filter_frame,
            variable=self.limit_var,
            values=[
                "50",
                "100",
                "250",
                "500",
                "All"
            ],
            width=100,
            height=40,
            state="readonly"
        )
        self.limit_menu.grid(
            row=0,
            column=2,
            padx=7,
            pady=14,
            sticky="ew"
        )

        apply_button = ctk.CTkButton(
            filter_frame,
            text="Apply Filters",
            width=125,
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
            width=85,
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

        delete_button = ctk.CTkButton(
            filter_frame,
            text="Delete Selected",
            width=135,
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_selected_record
        )
        delete_button.grid(
            row=0,
            column=6,
            padx=7,
            pady=14
        )

        refresh_button = ctk.CTkButton(
            filter_frame,
            text="Refresh",
            width=90,
            height=40,
            fg_color="#059669",
            hover_color="#047857",
            command=self.load_records
        )
        refresh_button.grid(
            row=0,
            column=7,
            padx=(7, 15),
            pady=14
        )

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
            text="ATM Transaction Records",
            font=("Segoe UI", 19, "bold"),
            text_color="#F8FAFC"
        )
        table_title.pack(side="left")

        self.record_count_label = ctk.CTkLabel(
            top_frame,
            text="0 records displayed",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )
        self.record_count_label.pack(side="right")

        self.selection_label = ctk.CTkLabel(
            table_card,
            text="Selected record: None",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        )
        self.selection_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )

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
            ("ID", "record_id", 65),
            ("ATM ID", "atm_id", 90),
            ("Date", "date", 105),
            ("City", "city", 105),
            ("Location", "location_type", 110),
            ("Transactions", "transaction_count", 105),
            ("Withdrawal", "withdrawal_amount", 125),
            ("Opening Cash", "opening_cash", 125),
            ("Cash Remaining", "cash_remaining", 130),
            ("Cash Out", "cash_out", 80),
            ("Refill Required", "replenishment_required", 105)
        ]

        for index, (_, _, width) in enumerate(
            self.table_columns
        ):
            self.table_scroll.grid_columnconfigure(
                index,
                weight=1,
                minsize=width
            )

        self.create_table_header()

    def create_table_header(self):

        for index, (heading, _, _) in enumerate(
            self.table_columns
        ):

            label = ctk.CTkLabel(
                self.table_scroll,
                text=heading,
                height=42,
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
    # DATABASE CONNECTION
    # ==================================================

    def get_connection(self):

        return sqlite3.connect(
            self.database_path
        )

    # ==================================================
    # LOAD RECORDS
    # ==================================================

    def load_records(self):

        try:
            connection = self.get_connection()

            query = """
                SELECT
                    record_id,
                    atm_id,
                    date,
                    city,
                    location_type,
                    day_of_week,
                    month,
                    is_weekend,
                    is_holiday,
                    festival,
                    temperature,
                    transaction_count,
                    average_withdrawal,
                    withdrawal_amount,
                    deposit_amount,
                    opening_cash,
                    cash_remaining,
                    cash_out,
                    replenishment_required,
                    next_day_cash_requirement,
                    year,
                    day,
                    day_of_year
                FROM atm_records
                ORDER BY date DESC, record_id DESC
            """

            self.records_df = pd.read_sql_query(
                query,
                connection
            )

            connection.close()

            self.filtered_df = self.records_df.copy()

            self.update_city_menu()
            self.update_summary_cards()
            self.apply_filters()

            self.connection_label.configure(
                text="● Database Connected",
                text_color="#22C55E"
            )

        except Exception as error:

            self.connection_label.configure(
                text="● Connection Error",
                text_color="#EF4444"
            )

            messagebox.showerror(
                "Database Error",
                f"Could not load database records.\n\n{error}"
            )

    # ==================================================
    # SUMMARY UPDATE
    # ==================================================

    def update_summary_cards(self):

        total_records = len(self.records_df)

        total_atms = (
            self.records_df["atm_id"].nunique()
            if not self.records_df.empty
            else 0
        )

        total_cities = (
            self.records_df["city"].nunique()
            if not self.records_df.empty
            else 0
        )

        database_size = self.get_database_size()

        self.total_records_value.configure(
            text=f"{total_records:,}"
        )

        self.total_atms_value.configure(
            text=str(total_atms)
        )

        self.total_cities_value.configure(
            text=str(total_cities)
        )

        self.database_size_value.configure(
            text=database_size
        )

    def get_database_size(self):

        try:
            size_bytes = os.path.getsize(
                self.database_path
            )

            if size_bytes >= 1024 * 1024:
                return (
                    f"{size_bytes / (1024 * 1024):.2f} MB"
                )

            if size_bytes >= 1024:
                return (
                    f"{size_bytes / 1024:.1f} KB"
                )

            return f"{size_bytes} B"

        except Exception:
            return "Unknown"

    # ==================================================
    # CITY MENU
    # ==================================================

    def update_city_menu(self):

        if self.records_df.empty:
            cities = ["All Cities"]

        else:
            cities = (
                self.records_df["city"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            cities = [
                "All Cities"
            ] + sorted(cities)

        self.city_menu.configure(
            values=cities
        )

        if self.city_var.get() not in cities:
            self.city_var.set("All Cities")

    # ==================================================
    # FILTERS
    # ==================================================

    def apply_filters(self):

        if self.records_df.empty:
            self.filtered_df = pd.DataFrame()
            self.display_records(
                self.filtered_df
            )
            return

        filtered = self.records_df.copy()

        search_text = (
            self.search_var.get()
            .strip()
            .lower()
        )

        selected_city = self.city_var.get()

        if search_text:

            atm_match = (
                filtered["atm_id"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_text,
                    regex=False,
                    na=False
                )
            )

            city_match = (
                filtered["city"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_text,
                    regex=False,
                    na=False
                )
            )

            location_match = (
                filtered["location_type"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_text,
                    regex=False,
                    na=False
                )
            )

            filtered = filtered[
                atm_match
                | city_match
                | location_match
            ]

        if selected_city != "All Cities":

            filtered = filtered[
                filtered["city"].astype(str)
                == selected_city
            ]

        selected_limit = self.limit_var.get()

        if selected_limit != "All":
            filtered = filtered.head(
                int(selected_limit)
            )

        self.filtered_df = filtered.copy()

        self.clear_selection()
        self.display_records(
            self.filtered_df
        )

    def reset_filters(self):

        self.search_var.set("")
        self.city_var.set("All Cities")
        self.limit_var.set("100")

        self.apply_filters()

    # ==================================================
    # DISPLAY RECORDS
    # ==================================================

    def display_records(self, dataframe):

        for widget in self.table_scroll.winfo_children():

            grid_information = widget.grid_info()

            if grid_information:

                row_number = int(
                    grid_information.get(
                        "row",
                        0
                    )
                )

                if row_number > 0:
                    widget.destroy()

        self.record_count_label.configure(
            text=f"{len(dataframe):,} records displayed"
        )

        if dataframe.empty:

            empty_label = ctk.CTkLabel(
                self.table_scroll,
                text="No matching database records found.",
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

        for display_row, (_, row) in enumerate(
            dataframe.iterrows(),
            start=1
        ):

            record_id = int(
                row["record_id"]
            )

            row_color = (
                "#263449"
                if display_row % 2 == 0
                else "#1E293B"
            )

            row_widgets = []

            for column_index, (
                _,
                column_name,
                _
            ) in enumerate(self.table_columns):

                value = self.format_cell_value(
                    column_name,
                    row[column_name]
                )

                label = ctk.CTkLabel(
                    self.table_scroll,
                    text=value,
                    height=39,
                    fg_color=row_color,
                    corner_radius=4,
                    font=("Segoe UI", 11),
                    text_color="#E2E8F0"
                )

                label.grid(
                    row=display_row,
                    column=column_index,
                    padx=3,
                    pady=2,
                    sticky="nsew"
                )

                label.bind(
                    "<Button-1>",
                    lambda event,
                    selected_id=record_id,
                    widgets=row_widgets: self.select_record(
                        selected_id,
                        widgets
                    )
                )

                row_widgets.append(label)

            # Rebind after all widgets exist
            for label in row_widgets:

                label.bind(
                    "<Button-1>",
                    lambda event,
                    selected_id=record_id,
                    widgets=row_widgets: self.select_record(
                        selected_id,
                        widgets
                    )
                )

    def format_cell_value(
        self,
        column_name,
        value
    ):

        if pd.isna(value):
            return "-"

        currency_columns = [
            "withdrawal_amount",
            "opening_cash",
            "cash_remaining"
        ]

        if column_name in currency_columns:
            return self.format_indian_currency(
                value
            )

        if column_name in [
            "cash_out",
            "replenishment_required"
        ]:

            return (
                "Yes"
                if int(value) == 1
                else "No"
            )

        if column_name == "date":

            try:
                parsed_date = pd.to_datetime(
                    value
                )

                return parsed_date.strftime(
                    "%d-%m-%Y"
                )

            except Exception:
                return str(value)

        return str(value)

    # ==================================================
    # SELECT RECORD
    # ==================================================

    def select_record(
        self,
        record_id,
        widgets
    ):

        for old_widget in self.selected_row_widgets:

            try:
                old_widget.configure(
                    fg_color="#263449"
                )
            except Exception:
                pass

        self.selected_record_id = record_id
        self.selected_row_widgets = widgets

        for widget in widgets:

            widget.configure(
                fg_color="#1D4ED8"
            )

        self.selection_label.configure(
            text=f"Selected record: {record_id}",
            text_color="#38BDF8"
        )

    def clear_selection(self):

        self.selected_record_id = None
        self.selected_row_widgets = []

        self.selection_label.configure(
            text="Selected record: None",
            text_color="#94A3B8"
        )

    # ==================================================
    # DELETE RECORD
    # ==================================================

    def delete_selected_record(self):

        if self.selected_record_id is None:

            messagebox.showwarning(
                "No Record Selected",
                "Click a table row before deleting a record."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            (
                f"Are you sure you want to delete record "
                f"{self.selected_record_id}?\n\n"
                "This action cannot be undone."
            )
        )

        if not confirm:
            return

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM atm_records
                WHERE record_id = ?
                """,
                (
                    self.selected_record_id,
                )
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Record Deleted",
                "The selected database record was deleted successfully."
            )

            self.clear_selection()
            self.load_records()

        except Exception as error:

            messagebox.showerror(
                "Delete Error",
                f"Could not delete the selected record.\n\n{error}"
            )

    # ==================================================
    # EXPORT TO EXCEL
    # ==================================================

    def export_to_excel(self):

        if self.filtered_df.empty:

            messagebox.showwarning(
                "No Data",
                "There are no database records available to export."
            )
            return

        default_filename = (
            "atm_database_records_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".xlsx"
        )

        save_path = filedialog.asksaveasfilename(
            title="Export ATM Database",
            defaultextension=".xlsx",
            initialfile=default_filename,
            filetypes=[
                (
                    "Excel Workbook",
                    "*.xlsx"
                )
            ]
        )

        if not save_path:
            return

        try:
            export_df = self.filtered_df.copy()

            export_df.to_excel(
                save_path,
                index=False
            )

            messagebox.showinfo(
                "Export Successful",
                (
                    "Database records were exported successfully."
                    f"\n\n{save_path}"
                )
            )

        except ImportError:

            messagebox.showerror(
                "Missing Package",
                (
                    "Excel export requires openpyxl.\n\n"
                    "Run this command:\n"
                    "pip install openpyxl"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                f"Could not export database records.\n\n{error}"
            )

    # ==================================================
    # INDIAN CURRENCY
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
import customtkinter as ctk


class AboutPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#0F172A")

        # =====================================================
        # HEADER
        # =====================================================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="ℹ️ About ATM Cash Replenishment Optimization",
            font=("Segoe UI", 30, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="AI Powered ATM Cash Forecasting & Replenishment Management System",
            font=("Segoe UI", 15),
            text_color="#94A3B8"
        )
        subtitle.pack(anchor="w", pady=(5, 0))

        # =====================================================
        # MAIN
        # =====================================================

        body = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        body.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        # =====================================================
        # PROJECT CARD
        # =====================================================

        project = self.create_card(body)
        project.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.heading(project, "🏦 Project")

        self.line(project, "Project Name", "ATM Cash Replenishment Optimization")
        self.line(project, "Version", "1.0")
        self.line(project, "Category", "Artificial Intelligence")
        self.line(project, "Prediction Model", "Random Forest Regressor")
        self.line(project, "Database", "SQLite")
        self.line(project, "Desktop UI", "CustomTkinter")

        # =====================================================
        # DEVELOPER CARD
        # =====================================================

        developer = self.create_card(body)
        developer.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.heading(developer, "👨‍💻 Developer")

        self.line(developer, "Name", "Akshit ")
        self.line(developer, "Course", "Master of Computer Applications")
        self.line(developer, "University", "Lovely Professional University")
        self.line(developer, "Specialization", "Data Science")

        # =====================================================
        # TECHNOLOGIES
        # =====================================================

        tech = self.create_card(body)
        tech.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.heading(tech, "🛠 Technologies Used")

        technologies = [
            "Python",
            "CustomTkinter",
            "SQLite",
            "Pandas",
            "Scikit-Learn",
            "Matplotlib",
            "Joblib",
            "OpenPyXL"
        ]

        for item in technologies:
            ctk.CTkLabel(
                tech,
                text="✔  " + item,
                font=("Segoe UI", 16),
                anchor="w"
            ).pack(anchor="w", padx=20, pady=3)

        # =====================================================
        # FEATURES
        # =====================================================

        feature = self.create_card(body)
        feature.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.heading(feature, "🚀 Features")

        features = [
            "Cash Prediction",
            "ATM Replenishment Optimizer",
            "Live Analytics Dashboard",
            "SQLite Database",
            "Prediction History",
            "Export to Excel",
            "Machine Learning Integration",
            "Professional Banking Interface"
        ]

        for item in features:
            ctk.CTkLabel(
                feature,
                text="✔  " + item,
                font=("Segoe UI", 16),
                anchor="w"
            ).pack(anchor="w", padx=20, pady=3)

        # =====================================================
        # MODEL DETAILS
        # =====================================================

        model = self.create_card(body)
        model.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.heading(model, "🤖 Machine Learning Model")

        description = """

This application predicts the Next-Day Cash Requirement of an ATM using a
Random Forest Regression model trained on historical ATM transaction data.

Dataset Size        : 10,000+ Records

Prediction Target   : Next Day Cash Requirement

Machine Learning    : Random Forest Regressor

Model Accuracy      : 95.08 %

Prediction Storage  : SQLite Database

Analytics           : Matplotlib

Optimization        : AI-based Priority Ranking
"""

        textbox = ctk.CTkTextbox(
            model,
            height=180,
            font=("Segoe UI", 15)
        )

        textbox.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(10, 15)
        )

        textbox.insert("0.0", description)
        textbox.configure(state="disabled")

        # =====================================================
        # FOOTER
        # =====================================================

        footer = ctk.CTkLabel(
            self,
            text="© 2026 ATM Cash Replenishment Optimization | Developed using Python & Machine Learning",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )

        footer.pack(pady=(5, 15))

    # =====================================================
    # CARD
    # =====================================================

    def create_card(self, master):

        return ctk.CTkFrame(
            master,
            fg_color="#1E293B",
            corner_radius=15
        )

    # =====================================================
    # TITLE
    # =====================================================

    def heading(self, master, text):

        ctk.CTkLabel(
            master,
            text=text,
            font=("Segoe UI", 21, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w", padx=20, pady=(18, 12))

    # =====================================================
    # LABEL
    # =====================================================

    def line(self, master, left, right):

        row = ctk.CTkFrame(
            master,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=5
        )

        ctk.CTkLabel(
            row,
            text=left,
            width=150,
            anchor="w",
            font=("Segoe UI", 15, "bold"),
            text_color="#CBD5E1"
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=right,
            anchor="w",
            font=("Segoe UI", 15),
            text_color="#F8FAFC"
        ).pack(side="left")
import customtkinter as ctk

from ui.optimizer import OptimizerPage
from ui.dashboard import DashboardPage
from ui.prediction import PredictionPage
from ui.analytics import AnalyticsPage
from ui.database_page import DatabasePage
from ui.history import HistoryPage
from ui.about import AboutPage


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ATMApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ATM Cash Replenishment Optimization")

        self.geometry("1400x800")

        self.configure(fg_color="#0F172A")

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#1E293B"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # Main Container
        self.container = ctk.CTkFrame(
            self,
            fg_color="#0F172A"
        )

        self.container.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.pages = {}

        self.create_sidebar()

        self.show_page("Dashboard")

    # -----------------------------------

    def create_sidebar(self):

        title = ctk.CTkLabel(
            self.sidebar,
            text="🏦 ATM SYSTEM",
            font=("Segoe UI",24,"bold")
        )

        title.pack(
            pady=(30,40)
        )

        menu = [

            ("Dashboard",DashboardPage),

            ("Predict Cash",PredictionPage),

            ("Optimizer", OptimizerPage),

            ("Analytics",AnalyticsPage),

            ("Database",DatabasePage),

            ("History",HistoryPage),

            ("About",AboutPage)

        ]

        for text,page in menu:

            button = ctk.CTkButton(

                self.sidebar,

                text=text,

                height=45,

                command=lambda p=text:self.show_page(p)

            )

            button.pack(
                padx=20,
                pady=10,
                fill="x"
            )

        exit_button = ctk.CTkButton(

            self.sidebar,

            text="Exit",

            fg_color="red",

            command=self.destroy

        )

        exit_button.pack(
            side="bottom",
            padx=20,
            pady=20,
            fill="x"
        )

    # -----------------------------------

    def show_page(self,name):

        for widget in self.container.winfo_children():
            widget.destroy()

        if name=="Dashboard":
            DashboardPage(self.container).pack(fill="both",expand=True)

        elif name=="Predict Cash":
            PredictionPage(self.container).pack(fill="both",expand=True)

        elif name == "Optimizer":
            OptimizerPage(
                self.container
            ).pack(
                fill="both",
                expand=True
            )

        elif name=="Analytics":
            AnalyticsPage(self.container).pack(fill="both",expand=True)

        elif name=="Database":
            DatabasePage(self.container).pack(fill="both",expand=True)

        elif name=="History":
            HistoryPage(self.container).pack(fill="both",expand=True)

        elif name=="About":
            AboutPage(self.container).pack(fill="both",expand=True)


app=ATMApp()

app.mainloop()
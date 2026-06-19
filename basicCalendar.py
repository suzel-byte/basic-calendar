import calendar
import tkinter as tk
from datetime import date, datetime
from tkinter import ttk


FIXED_HOLIDAYS = [
    ("New Year's Day", 1, 1),
    ("Republic Day", 1, 26),
    ("Independence Day", 8, 15),
    ("Gandhi Jayanti", 10, 2),
    ("Christmas", 12, 25),
]

FESTIVALS_BY_YEAR = {
    2026: [
        ("Guru Gobind Singh Jayanti", 1, 5),
        ("Lohri", 1, 13),
        ("Makar Sankranti / Pongal", 1, 15),
        ("Vasant Panchami / Saraswati Puja", 1, 23),
        ("Maha Shivaratri", 2, 15),
        ("Ramadan Begins", 2, 17),
        ("Holika Dahan", 3, 3),
        ("AP's Birthday",5,6),
        ("Devesh Birthday",2,10),
        ("Holi", 3, 4),
        ("Good Friday", 4, 3),
        ("Holi Bhai Dooj", 3, 5),
        ("Chaitra Navratri Begins", 3, 19),
        ("Eid al-Fitr", 3, 20),
        ("Ram Navami", 3, 26),
        ("Chaitra Navratri Ends", 3, 27),
        ("Mahavir Jayanti", 3, 31),
        ("Hanuman Jayanti", 4, 2),
        ("Good Friday", 4, 3),
        ("Easter Sunday", 4, 5),
        ("Baisakhi / Vaisakhi", 4, 14),
        ("Tamil New Year / Vishu", 4, 14),
        ("Akshaya Tritiya", 4, 19),
        ("Buddha Purnima", 5, 1),
        ("Eid al-Adha", 5, 27),
        ("Muharram", 6, 26),
        ("Guru Purnima", 7, 29),
        ("Friendship Day", 8, 2),
        ("Raksha Bandhan", 8, 28),
        ("Onam", 8, 28),
        ("Krishna Janmashtami", 9, 4),
        ("Ganesh Chaturthi", 9, 14),
        ("Anant Chaturdashi", 9, 24),
        ("Sharad Navratri Begins", 10, 11),
        ("Durga Ashtami", 10, 18),
        ("Maha Navami", 10, 19),
        ("Dussehra", 10, 20),
        ("Karwa Chauth", 10, 29),
        ("Dhanteras", 11, 6),
        ("Naraka Chaturdashi", 11, 7),
        ("Diwali", 11, 8),
        ("Govardhan Puja", 11, 10),
        ("Bhai Dooj", 11, 11),
        ("Chhath Puja", 11, 15),
        ("Guru Nanak Jayanti", 11, 24),
        ("Karthikai Deepam", 11, 24),
        ("Christmas Eve", 12, 24),
    ]
}


class CalendarClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar and Digital Clock")
        self.root.geometry("860x620")
        self.root.minsize(760, 560)
        self.root.configure(bg="#eef3f7")

        today = date.today()
        self.holiday_year = today.year
        self.calendar_year = today.year
        self.calendar_month = today.month

        self._build_styles()
        self._build_layout()
        self._refresh_calendar()
        self._refresh_holidays()
        self._tick()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Main.TFrame", background="#eef3f7")
        style.configure("Panel.TFrame", background="#ffffff", relief="flat")
        style.configure("Title.TLabel", background="#eef3f7", foreground="#1f2937", font=("Segoe UI", 22, "bold"))
        style.configure("Greeting.TLabel", background="#ffffff", foreground="#2563eb", font=("Segoe UI", 24, "bold"))
        style.configure("Clock.TLabel", background="#ffffff", foreground="#111827", font=("Consolas", 38, "bold"))
        style.configure("Date.TLabel", background="#ffffff", foreground="#4b5563", font=("Segoe UI", 14))
        style.configure("Section.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 15, "bold"))
        style.configure("Text.TLabel", background="#ffffff", foreground="#374151", font=("Segoe UI", 11))
        style.configure("Nav.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 6))
        style.configure("Holiday.Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Holiday.Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_layout(self):
        main = ttk.Frame(self.root, style="Main.TFrame", padding=22)
        main.pack(fill="both", expand=True)

        title = ttk.Label(main, text="Calendar and Digital Clock", style="Title.TLabel")
        title.pack(anchor="w", pady=(0, 16))

        content = ttk.Frame(main, style="Main.TFrame")
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        left_panel = ttk.Frame(content, style="Panel.TFrame", padding=20)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(2, weight=1)

        right_panel = ttk.Frame(content, style="Panel.TFrame", padding=20)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(2, weight=1)

        self.greeting_label = ttk.Label(left_panel, style="Greeting.TLabel")
        self.greeting_label.grid(row=0, column=0, sticky="w")

        self.time_label = ttk.Label(left_panel, style="Clock.TLabel")
        self.time_label.grid(row=1, column=0, sticky="w", pady=(8, 0))

        self.date_label = ttk.Label(left_panel, style="Date.TLabel")
        self.date_label.grid(row=2, column=0, sticky="nw", pady=(4, 18))

        calendar_header = ttk.Frame(left_panel, style="Panel.TFrame")
        calendar_header.grid(row=3, column=0, sticky="ew", pady=(8, 10))
        calendar_header.columnconfigure(1, weight=1)

        ttk.Button(calendar_header, text="<", style="Nav.TButton", command=self._previous_month).grid(row=0, column=0)
        self.month_label = ttk.Label(calendar_header, style="Section.TLabel", anchor="center")
        self.month_label.grid(row=0, column=1, sticky="ew")
        ttk.Button(calendar_header, text=">", style="Nav.TButton", command=self._next_month).grid(row=0, column=2)

        self.calendar_text = tk.Text(
            left_panel,
            height=10,
            borderwidth=0,
            bg="#f8fafc",
            fg="#111827",
            font=("Consolas", 13),
            padx=16,
            pady=14,
            wrap="none",
        )
        self.calendar_text.grid(row=4, column=0, sticky="nsew")
        self.calendar_text.configure(state="disabled")

        ttk.Label(right_panel, text="Upcoming Festivals / Holidays", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        self.holiday_year_label = ttk.Label(right_panel, text=f"Current year: {self.holiday_year}", style="Text.TLabel")
        self.holiday_year_label.grid(row=1, column=0, sticky="w", pady=(2, 12))

        self.holiday_table = ttk.Treeview(
            right_panel,
            columns=("date", "name", "days"),
            show="headings",
            style="Holiday.Treeview",
        )
        self.holiday_table.heading("date", text="Date")
        self.holiday_table.heading("name", text="Festival / Holiday")
        self.holiday_table.heading("days", text="In")
        self.holiday_table.column("date", width=92, anchor="w", stretch=False)
        self.holiday_table.column("name", width=190, anchor="w")
        self.holiday_table.column("days", width=70, anchor="center", stretch=False)
        self.holiday_table.grid(row=2, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=self.holiday_table.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.holiday_table.configure(yscrollcommand=scrollbar.set)

    def _tick(self):
        now = datetime.now()
        self.greeting_label.configure(text=self._get_greeting(now.hour))
        self.time_label.configure(text=now.strftime("%I:%M:%S %p"))
        self.date_label.configure(text=now.strftime("%A, %d %B %Y"))
        self.root.after(1000, self._tick)

    def _get_greeting(self, hour):
        if 5 <= hour < 12:
            return "Good Morning"
        if 12 <= hour < 17:
            return "Good Afternoon"
        if 17 <= hour < 21:
            return "Good Evening"
        return "Good Night"

    def _refresh_calendar(self):
        self.month_label.configure(text=f"{calendar.month_name[self.calendar_month]} {self.calendar_year}")
        month_calendar = calendar.TextCalendar(calendar.SUNDAY).formatmonth(self.calendar_year, self.calendar_month)
        self.calendar_text.configure(state="normal")
        self.calendar_text.delete("1.0", tk.END)
        self.calendar_text.insert(tk.END, month_calendar)
        self.calendar_text.configure(state="disabled")

    def _refresh_holidays(self):
        today = date.today()
        current_year_holidays = FIXED_HOLIDAYS + FESTIVALS_BY_YEAR.get(self.holiday_year, [])
        holidays = []

        self.holiday_year_label.configure(text=f"Current year: {self.holiday_year}")

        for name, month, day in current_year_holidays:
            holiday_date = date(self.holiday_year, month, day)
            if holiday_date >= today:
                holidays.append((holiday_date, name, (holiday_date - today).days))

        holidays.sort(key=lambda item: item[0])

        for item in self.holiday_table.get_children():
            self.holiday_table.delete(item)

        if not holidays:
            message = "No more listed holidays this year"
            if self.holiday_year not in FESTIVALS_BY_YEAR:
                message = "Add movable festival dates for this year"
            self.holiday_table.insert("", "end", values=("-", message, "-"))
            return

        for holiday_date, name, days_left in holidays:
            days_text = "Today" if days_left == 0 else f"{days_left} days"
            self.holiday_table.insert("", "end", values=(holiday_date.strftime("%d %b"), name, days_text))

    def _previous_month(self):
        if self.calendar_month == 1:
            self.calendar_month = 12
            self.calendar_year -= 1
        else:
            self.calendar_month -= 1
        self._refresh_calendar()

    def _next_month(self):
        if self.calendar_month == 12:
            self.calendar_month = 1
            self.calendar_year += 1
        else:
            self.calendar_month += 1
        self._refresh_calendar()


if __name__ == "__main__":
    app_root = tk.Tk()
    CalendarClockApp(app_root)
    app_root.mainloop()

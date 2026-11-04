"""Tkinter window for the ATA Martial Arts fee calculator."""

import tkinter as tk
from tkinter import ttk

from athlete import Athlete, Squad
from pricing import WEEKLY_FEES, WEIGHT_CATEGORIES
from validation import (
    validate_category,
    validate_coaching_hours,
    validate_competitions,
    validate_name,
    validate_plan,
    validate_weight,
)

WINDOW_TITLE = "ATA Martial Arts Fee Calculator"
ERROR_COLOUR = "red"
FORM_PADDING = 5
RESULT_ROWS = 7
RESULT_WIDTH = 60
TREE_ROWS = 6
TREE_COLUMNS = (
    "Name",
    "Plan",
    "Weight (kg)",
    "Category",
    "Competitions",
    "Coaching hrs/week",
    "Monthly total",
)


def format_money(amount: float) -> str:
    """Show an amount as pounds with 2 decimal places."""
    return f"£{amount:.2f}"


def get_category_names() -> list:
    """Return just the category names for the drop-down list."""
    names = []
    for name, upper_limit in WEIGHT_CATEGORIES:
        names.append(name)
    return names


class FeeApp:
    """The main window: a form, a breakdown area and an athlete list."""

    def __init__(self, root: tk.Tk) -> None:
        """Build the window and start with an empty squad."""
        self.root = root
        self.squad = Squad()
        root.title(WINDOW_TITLE)
        self.build_form()
        self.build_buttons()
        self.build_results()
        self.build_athlete_list()

    def build_form(self) -> None:
        """Create the labels and input fields."""
        form = ttk.Frame(self.root, padding=FORM_PADDING)
        form.grid(row=0, column=0, sticky="w")

        self.name_entry = self.add_entry(form, "Name", 0)
        self.plan_combo = self.add_combo(
            form, "Plan", 1, list(WEEKLY_FEES)
        )
        self.plan_combo.bind("<<ComboboxSelected>>", self.on_plan_selected)
        self.weight_entry = self.add_entry(form, "Weight (kg)", 2)
        self.category_combo = self.add_combo(
            form, "Weight category", 3, get_category_names()
        )
        self.competitions_entry = self.add_entry(
            form, "Competitions this month", 4
        )
        self.hours_entry = self.add_entry(
            form, "Coaching hours per week", 5
        )

    def add_entry(self, parent: ttk.Frame, label: str, row: int) -> ttk.Entry:
        """Add a label and a text box on one row and return the box."""
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", padx=FORM_PADDING, pady=2
        )
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, sticky="w", pady=2)
        return entry

    def add_combo(
        self, parent: ttk.Frame, label: str, row: int, values: list
    ) -> ttk.Combobox:
        """Add a label and a drop-down list on one row and return it."""
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", padx=FORM_PADDING, pady=2
        )
        combo = ttk.Combobox(parent, values=values, state="readonly")
        combo.grid(row=row, column=1, sticky="w", pady=2)
        return combo

    def build_buttons(self) -> None:
        """Create the buttons and the red error message label."""
        area = ttk.Frame(self.root, padding=FORM_PADDING)
        area.grid(row=1, column=0, sticky="w")

        ttk.Button(
            area, text="Calculate and Add Athlete", command=self.on_calculate
        ).grid(row=0, column=0, padx=FORM_PADDING)
        ttk.Button(
            area, text="Clear Form", command=self.on_clear
        ).grid(row=0, column=1, padx=FORM_PADDING)

        self.error_label = tk.Label(
            self.root, text="", fg=ERROR_COLOUR, wraplength=450,
            justify="left",
        )
        self.error_label.grid(row=2, column=0, sticky="w", padx=FORM_PADDING)

    def build_results(self) -> None:
        """Create the read-only area that shows the itemised breakdown."""
        self.result_text = tk.Text(
            self.root, height=RESULT_ROWS, width=RESULT_WIDTH,
            state="disabled",
        )
        self.result_text.grid(
            row=3, column=0, sticky="w", padx=FORM_PADDING, pady=FORM_PADDING
        )

    def build_athlete_list(self) -> None:
        """Create the table of athletes added so far."""
        self.tree = ttk.Treeview(
            self.root, columns=TREE_COLUMNS, show="headings",
            height=TREE_ROWS,
        )
        for column in TREE_COLUMNS:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=110, anchor="center")
        self.tree.grid(row=4, column=0, padx=FORM_PADDING, pady=FORM_PADDING)

    def on_plan_selected(self, event: tk.Event) -> None:
        """Lock competitions to 0 for Beginner, otherwise unlock it."""
        if self.plan_combo.get() == "Beginner":
            self.set_competitions("0")
            self.competitions_entry.config(state="disabled")
        else:
            self.competitions_entry.config(state="normal")

    def set_competitions(self, text: str) -> None:
        """Put text in the competitions box even if it is locked."""
        self.competitions_entry.config(state="normal")
        self.competitions_entry.delete(0, tk.END)
        self.competitions_entry.insert(0, text)

    def read_athlete(self) -> tuple:
        """Validate every field in order and return (ok, athlete_or_msg)."""
        ok, name = validate_name(self.name_entry.get())
        if not ok:
            return (False, name)
        ok, plan = validate_plan(self.plan_combo.get())
        if not ok:
            return (False, plan)
        ok, weight = validate_weight(self.weight_entry.get())
        if not ok:
            return (False, weight)
        ok, category = validate_category(self.category_combo.get(), weight)
        if not ok:
            return (False, category)
        ok, competitions = validate_competitions(
            plan, self.competitions_entry.get()
        )
        if not ok:
            return (False, competitions)
        ok, hours = validate_coaching_hours(self.hours_entry.get())
        if not ok:
            return (False, hours)
        athlete = Athlete(name, plan, weight, category, competitions, hours)
        return (True, athlete)

    def on_calculate(self) -> None:
        """Validate the form, then add and show the athlete if all is OK."""
        ok, result = self.read_athlete()
        if not ok:
            self.error_label.config(text=result)
            return
        self.error_label.config(text="")
        self.squad.add_athlete(result)
        self.show_breakdown(result)
        self.add_to_list(result)

    def show_breakdown(self, athlete: Athlete) -> None:
        """Write the itemised costs and total into the result area."""
        lines, total = athlete.monthly_breakdown()
        text = "Athlete: " + athlete.name + "\n"
        for label, working, cost in lines:
            text = text + f"{label}: {working} = {format_money(cost)}\n"
        text = text + "Monthly total: " + format_money(total) + "\n"
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.config(state="disabled")

    def add_to_list(self, athlete: Athlete) -> None:
        """Add one row for the athlete to the table."""
        lines, total = athlete.monthly_breakdown()
        row = (
            athlete.name,
            athlete.plan,
            athlete.weight,
            athlete.category,
            athlete.competitions,
            athlete.coach_hours,
            format_money(total),
        )
        self.tree.insert("", tk.END, values=row)

    def on_clear(self) -> None:
        """Empty every field and the error message."""
        self.name_entry.delete(0, tk.END)
        self.plan_combo.set("")
        self.weight_entry.delete(0, tk.END)
        self.category_combo.set("")
        self.set_competitions("")
        self.hours_entry.delete(0, tk.END)
        self.error_label.config(text="")


def main() -> None:
    """Open the fee calculator window."""
    root = tk.Tk()
    FeeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

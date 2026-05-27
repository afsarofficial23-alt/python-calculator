# Improved Advanced Calculator Project (Python + Tkinter)
import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime

from sympy import symbols, solve
from sympy.parsing.sympy_parser import parse_expr

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("750x600")
        self.root.minsize(700, 550)

        # Variables
        self.memory = 0
        self.history = []

        self.display_var = tk.StringVar(value="0")
        self.memory_var = tk.StringVar(value="Memory: 0")

        self.setup_style()
        self.create_ui()

    # =========================
    # STYLING
    # =========================
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("TLabel", font=("Arial", 11))
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"))

    # =========================
    # UI CREATION
    # =========================
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Display
        self.display = ttk.Entry(
            main_frame,
            textvariable=self.display_var,
            font=("Consolas", 24),
            justify="right"
        )
        self.display.pack(fill=tk.X, pady=10)
        self.display.bind("<Return>", lambda e: self.calculate_expression())

        # Memory label
        ttk.Label(main_frame, textvariable=self.memory_var).pack(anchor="w")

        # Notebook Tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        self.create_basic_tab(notebook)
        self.create_scientific_tab(notebook)
        self.create_memory_tab(notebook)
        self.create_history_tab(notebook)
        self.create_converter_tab(notebook)
        self.create_solver_tab(notebook)

    # =========================
    # BASIC CALCULATOR TAB
    # =========================
    def create_basic_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Basic")

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "DEL", "√", "^"]
        ]

        for row in buttons:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=3)

            for btn in row:
                ttk.Button(
                    row_frame,
                    text=btn,
                    command=lambda b=btn: self.button_click(b)
                ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)

    # =========================
    # SCIENTIFIC TAB
    # =========================
    def create_scientific_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Scientific")

        functions = [
            ["sin", "cos", "tan"],
            ["asin", "acos", "atan"],
            ["log", "ln", "exp"],
            ["π", "e", "!"],
            ["deg", "rad", "%"]
        ]

        for row in functions:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=3)

            for func in row:
                ttk.Button(
                    row_frame,
                    text=func,
                    command=lambda f=func: self.advanced_function(f)
                ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)

    # =========================
    # MEMORY TAB
    # =========================
    def create_memory_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Memory")

        buttons = [
            ["M+", "M-"],
            ["MR", "MC"],
            ["MS", "M√"]
        ]

        for row in buttons:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=5)

            for btn in row:
                ttk.Button(
                    row_frame,
                    text=btn,
                    command=lambda b=btn: self.memory_operation(b)
                ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3)

    # =========================
    # HISTORY TAB
    # =========================
    def create_history_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="History")

        top = ttk.Frame(frame)
        top.pack(fill=tk.X, pady=5)

        ttk.Button(top, text="Clear", command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Copy", command=self.copy_history).pack(side=tk.LEFT)

        self.history_listbox = tk.Listbox(frame, font=("Consolas", 11))
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.history_listbox.bind("<Double-Button-1>", self.load_history)

    # =========================
    # UNIT CONVERTER TAB
    # =========================
    def create_converter_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Converter")

        converter_frame = ttk.LabelFrame(frame, text="Unit Converter", padding=10)
        converter_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(converter_frame, text="Type:").grid(row=0, column=0, pady=5)

        self.converter_type = ttk.Combobox(
            converter_frame,
            values=["Length", "Weight", "Temperature"],
            state="readonly"
        )
        self.converter_type.grid(row=0, column=1, pady=5)
        self.converter_type.bind("<<ComboboxSelected>>", self.update_units)

        ttk.Label(converter_frame, text="From:").grid(row=1, column=0)
        self.from_unit = ttk.Combobox(converter_frame, state="readonly")
        self.from_unit.grid(row=1, column=1)

        ttk.Label(converter_frame, text="To:").grid(row=2, column=0)
        self.to_unit = ttk.Combobox(converter_frame, state="readonly")
        self.to_unit.grid(row=2, column=1)

        ttk.Label(converter_frame, text="Value:").grid(row=3, column=0)
        self.convert_entry = ttk.Entry(converter_frame)
        self.convert_entry.grid(row=3, column=1)

        ttk.Button(
            converter_frame,
            text="Convert",
            command=self.convert_units
        ).grid(row=4, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(converter_frame, text="Result: ")
        self.result_label.grid(row=5, column=0, columnspan=2)

    # =========================
    # EQUATION SOLVER TAB
    # =========================
    def create_solver_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Equation Solver")

        ttk.Label(
            frame,
            text="Example: x**2 - 5*x + 6"
        ).pack(pady=5)

        self.eq_entry = ttk.Entry(frame, font=("Arial", 12))
        self.eq_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            frame,
            text="Solve Equation",
            command=self.solve_equation
        ).pack(pady=10)

        self.solution_box = tk.Listbox(frame, font=("Consolas", 11))
        self.solution_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # =========================
    # BUTTON FUNCTIONS
    # =========================
    def button_click(self, value):
        current = self.display_var.get()

        if value == "C":
            self.display_var.set("0")

        elif value == "DEL":
            self.display_var.set(current[:-1] if len(current) > 1 else "0")

        elif value == "=":
            self.calculate_expression()

        elif value == "√":
            try:
                result = math.sqrt(float(current))
                self.display_var.set(str(result))
                self.add_history(f"√({current})", result)
            except Exception:
                messagebox.showerror("Error", "Invalid square root input")

        elif value == "^":
            self.display_var.set(current + "**")

        else:
            if current == "0":
                self.display_var.set(value)
            else:
                self.display_var.set(current + value)

    # =========================
    # CALCULATE
    # =========================
    def calculate_expression(self):
        try:
            expression = self.display_var.get()

            # Safer eval
            allowed = {
                "__builtins__": None,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "pi": math.pi,
                "e": math.e
            }

            result = eval(expression, allowed)

            self.display_var.set(str(result))
            self.add_history(expression, result)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =========================
    # ADVANCED FUNCTIONS
    # =========================
    def advanced_function(self, func):
        try:
            value = float(self.display_var.get())

            operations = {
                "sin": math.sin(math.radians(value)),
                "cos": math.cos(math.radians(value)),
                "tan": math.tan(math.radians(value)),
                "asin": math.degrees(math.asin(value)),
                "acos": math.degrees(math.acos(value)),
                "atan": math.degrees(math.atan(value)),
                "log": math.log10(value),
                "ln": math.log(value),
                "exp": math.exp(value),
                "!": math.factorial(int(value)),
                "deg": math.degrees(value),
                "rad": math.radians(value)
            }

            if func == "π":
                self.display_var.set(str(math.pi))
                return

            if func == "e":
                self.display_var.set(str(math.e))
                return

            if func == "%":
                self.display_var.set(self.display_var.get() + "%")
                return

            result = operations[func]
            self.display_var.set(str(result))

            self.add_history(f"{func}({value})", result)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =========================
    # MEMORY FUNCTIONS
    # =========================
    def memory_operation(self, operation):
        try:
            value = float(self.display_var.get())

            if operation == "M+":
                self.memory += value

            elif operation == "M-":
                self.memory -= value

            elif operation == "MS":
                self.memory = value

            elif operation == "MR":
                self.display_var.set(str(self.memory))
                return

            elif operation == "MC":
                self.memory = 0

            elif operation == "M√":
                self.memory = math.sqrt(self.memory)

            self.memory_var.set(f"Memory: {self.memory}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =========================
    # HISTORY FUNCTIONS
    # =========================
    def add_history(self, expression, result):
        time = datetime.now().strftime("%H:%M:%S")
        entry = f"[{time}] {expression} = {result}"

        self.history.append(entry)
        self.history_listbox.insert(tk.END, entry)

    def clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)

    def copy_history(self):
        selected = self.history_listbox.curselection()

        if selected:
            value = self.history[selected[0]]
            self.root.clipboard_clear()
            self.root.clipboard_append(value)

    def load_history(self, event):
        selected = self.history_listbox.curselection()

        if selected:
            entry = self.history[selected[0]]
            result = entry.split("=")[-1].strip()
            self.display_var.set(result)

    # =========================
    # UNIT CONVERSION
    # =========================
    def update_units(self, event=None):
        data = {
            "Length": ["m", "km", "cm"],
            "Weight": ["kg", "g", "lb"],
            "Temperature": ["C", "F", "K"]
        }

        units = data.get(self.converter_type.get(), [])

        self.from_unit["values"] = units
        self.to_unit["values"] = units

    def convert_units(self):
        try:
            value = float(self.convert_entry.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            conversion_type = self.converter_type.get()

            result = 0

            # Length
            if conversion_type == "Length":
                base = {
                    "m": 1,
                    "km": 1000,
                    "cm": 0.01
                }

                result = value * base[from_unit] / base[to_unit]

            # Weight
            elif conversion_type == "Weight":
                base = {
                    "kg": 1,
                    "g": 0.001,
                    "lb": 0.453592
                }

                result = value * base[from_unit] / base[to_unit]

            # Temperature
            elif conversion_type == "Temperature":
                result = self.convert_temperature(value, from_unit, to_unit)

            self.result_label.config(
                text=f"Result: {value} {from_unit} = {round(result, 4)} {to_unit}"
            )

            self.add_history(
                f"Convert {value} {from_unit} to {to_unit}",
                result
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == "C":
            c = value
        elif from_unit == "F":
            c = (value - 32) * 5 / 9
        else:
            c = value - 273.15

        if to_unit == "C":
            return c
        elif to_unit == "F":
            return c * 9 / 5 + 32
        else:
            return c + 273.15

    # =========================
    # EQUATION SOLVER
    # =========================
    def solve_equation(self):
        try:
            equation_text = self.eq_entry.get()

            x = symbols('x')
            equation = parse_expr(equation_text)

            solutions = solve(equation, x)

            self.solution_box.delete(0, tk.END)

            if solutions:
                for sol in solutions:
                    self.solution_box.insert(tk.END, f"x = {sol}")
            else:
                self.solution_box.insert(tk.END, "No solution found")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# =========================
# MAIN PROGRAM
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sympy as sp

class GraphingCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Graphing Calculator")

        self.x_min = -10
        self.x_max = 10

        self.create_widgets()

    def create_widgets(self):
        self.function_label = ttk.Label(self.master, text="Enter function of x (use '*' for multiplication, e.g., '2*x + 1'):")
        self.function_label.pack(padx=10, pady=5)

        self.function_entry = ttk.Entry(self.master)
        self.function_entry.pack(padx=10, pady=5)
        self.function_entry.focus()

        self.color_label = ttk.Label(self.master, text="Line color:")
        self.color_label.pack(padx=10, pady=5)

        self.color_entry = ttk.Entry(self.master)
        self.color_entry.pack(padx=10, pady=5)
        self.color_entry.insert(0, "blue")  # Default color

        self.zoom_in_button = ttk.Button(self.master, text="Zoom In", command=lambda: self.zoom("in"))
        self.zoom_in_button.pack(side=tk.LEFT, padx=5, pady=20)

        self.zoom_out_button = ttk.Button(self.master, text="Zoom Out", command=lambda: self.zoom("out"))
        self.zoom_out_button.pack(side=tk.RIGHT, padx=5, pady=20)

        self.plot_button = ttk.Button(self.master, text="Plot", command=self.plot_function)
        self.plot_button.pack(pady=20)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_function(self):
        user_input = self.function_entry.get()
        line_color = self.color_entry.get()
        x = sp.symbols('x')
        try:
            func_expr = sp.sympify(user_input, evaluate=False)  # Convert input to a sympy expression without automatic evaluation
            func = sp.lambdify(x, func_expr, modules=['numpy'])
            x_vals = np.linspace(self.x_min, self.x_max, 400)
            y_vals = func(x_vals)

            self.plot.clear()
            self.plot.plot(x_vals, y_vals, color=line_color)
            self.plot.set_title(f"y = {user_input}")
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid function: {e}")
            self.plot.set_title("Error in function. Please check your input.")
            self.canvas.draw()

    def zoom(self, direction):
        center = (self.x_max + self.x_min) / 2
        width = (self.x_max - self.x_min) / 2
        if direction == "in":
            width *= 0.5
        elif direction == "out":
            width *= 2
        self.x_min, self.x_max = center - width, center + width
        self.plot_function()

def main():
    root = tk.Tk()
    app = GraphingCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

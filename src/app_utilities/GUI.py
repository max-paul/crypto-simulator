import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog


class CryptoGuiComponents:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        # Exchange Selection
        exchange_label = ttk.Label(self.master, text="Choose Exchange:")
        exchange_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.exchange_menu = ttk.Combobox(self.master, textvariable=self.app.chosen_exchange, values=self.app.exchanges)
        self.exchange_menu.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.exchange_menu.bind("<<ComboboxSelected>>", lambda event: self.app.on_select_exchange())

        # Symbol Part Selection
        part_label = ttk.Label(self.master, text="Choose Symbol Part:")
        part_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.part_menu = ttk.Combobox(self.master, textvariable=self.app.chosen_part)
        self.part_menu.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        part_button = ttk.Button(self.master, text="Select Symbol Part", command=self.app.on_select_symbol_part)
        part_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        # Symbol Selection
        symbol_label = ttk.Label(self.master, text="Choose Cryptocurrency Symbol:")
        symbol_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.symbol_menu = ttk.Combobox(self.master, textvariable=self.app.crypto_symbol)
        self.symbol_menu.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        symbol_button = ttk.Button(self.master, text="Select Symbol", command=self.app.on_select_crypto_symbol)
        symbol_button.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)

        # Days in Past Entry
        days_label = ttk.Label(self.master, text="Enter Days in Past:")
        days_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        days_entry = ttk.Entry(self.master, textvariable=self.app.days_in_past)
        days_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        # Weekly Investment Entry
        weekly_investment_label = ttk.Label(self.master, text="Enter Weekly Investment Amount:")
        weekly_investment_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        weekly_investment_entry = ttk.Entry(self.master, textvariable=self.app.weekly_investment)
        weekly_investment_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        # Fee Entry
        fee_label = ttk.Label(self.master, text="Enter Fee Amount:")
        fee_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        fee_entry = ttk.Entry(self.master, textvariable=self.app.fee)
        fee_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

        # Simulate Button
        simulate_button = ttk.Button(self.master, text="Simulate", command=self.app.simulate_and_plot)
        simulate_button.grid(row=6, column=0, columnspan=3, pady=10)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(4, 2), dpi=100)  # Adjust the figsize and dpi as needed
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

        # Table (Treeview with Scrollbar)
        columns = ['investment_amount', 'tokens_bought', 'total_tokens', 'total_invested', 'current_value',
                   'return_on_investment']
        self.tree_frame = ttk.Frame(self.master)
        self.tree_frame.grid(row=7, column=3, padx=10, pady=10, sticky="nsew")

        self.treeview = ttk.Treeview(self.tree_frame, columns=columns, show="headings",
                                     height=25)  # Set the desired height

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)  # Adjust the column width as needed

        self.treeview.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.treeview.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.treeview.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.treeview.configure(xscrollcommand=scrollbar_x.set)

        # Configure grid weights to make the frame expandable
        self.master.grid_rowconfigure(10, weight=1)
        self.master.grid_columnconfigure(10, weight=1)
# Download CSV Button
        download_button = ttk.Button(self.master, text="Download CSV", command=self.download_csv)
        download_button.grid(row=8, column=3, padx=10, pady=5, sticky=tk.W)
        # Save Chart Button
        save_chart_button = ttk.Button(self.master, text="Save Chart", command=self.save_chart)
        save_chart_button.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)

    def download_csv(self):
        # Get the data from the Treeview
        data = []
        for child in self.treeview.get_children():
            values = self.treeview.item(child, 'values')
            data.append(values)

        # Create a DataFrame from the data
        df = pd.DataFrame(data, columns=['investment_amount', 'tokens_bought', 'total_tokens',
                                         'total_invested', 'current_value', 'return_on_investment'])

        # Open a file dialog to choose the destination file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False)

    def save_chart(self):
        # Open a file dialog to choose the destination file
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])

        if file_path:
            # Save the chart as a JPG image
            self.app.gui_components.fig.savefig(file_path, format='jpg', dpi=300)

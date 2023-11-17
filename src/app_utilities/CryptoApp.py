import ccxt
import tkinter as tk
from .GUI import CryptoGuiComponents
from .Simulation import Simulation
from .Datahandling import DataHandling


class CryptoInvestmentApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Crypto Investment Simulator")

        # Variables
        self.exchanges = ccxt.exchanges
        self.chosen_exchange = tk.StringVar()
        self.symbol_parts = set()
        self.chosen_part = tk.StringVar()
        self.filtered_symbols = []
        self.crypto_symbol = tk.StringVar()
        self.days_in_past = tk.IntVar()
        self.weekly_investment = tk.DoubleVar()
        self.fee = tk.DoubleVar()

        # Instances of other classes
        self.gui_components = CryptoGuiComponents(self.master, self)
        self.simulation = Simulation(self)
        self.data_handling = DataHandling(self)

    def on_select_exchange(self, event=None):
        self.chosen_exchange.set(self.chosen_exchange.get())
        self.symbol_parts = self.data_handling.display_symbol_parts(self.data_handling.get_exchange_symbols())
        self.data_handling.update_symbol_part_menu()

    def on_select_symbol_part(self, event=None):
        self.chosen_part.set(self.chosen_part.get())
        self.filtered_symbols = self.data_handling.filter_symbols_by_part(
            self.data_handling.get_exchange_symbols(), self.chosen_part.get()
        )
        self.data_handling.update_symbol_menu()

    def on_select_crypto_symbol(self, event=None):
        self.crypto_symbol.set(self.crypto_symbol.get())

    def run_simulation(self):
        return self.simulation.run_simulation()

    def update_table(self, df):
        for child in self.gui_components.treeview.get_children():
            self.gui_components.treeview.delete(child)
        for index, row in df.iterrows():
            values = [str(value) for value in row.tolist()]
            self.gui_components.treeview.insert("", tk.END, values=values)

    def plot_simulation(self, df):
        self.gui_components.ax.clear()
        marker_size = 2

        self.gui_components.ax.plot(df['timestamp'], df['total_invested'], label='Total Invested', marker='o',
                                    markersize=marker_size)
        self.gui_components.ax.plot(df['timestamp'], df['current_value'], label='Current Value', marker='o',
                                    markersize=marker_size)

        title = f"Weekly Investment Simulation - {self.chosen_exchange.get()} - {self.crypto_symbol.get()}"
        self.gui_components.ax.set_title(title, fontsize=6)

        self.gui_components.ax.set_xlabel('Date', fontsize=4)
        self.gui_components.ax.set_ylabel('Amount ($)', fontsize=4)

        # Set smaller tick parameters
        self.gui_components.ax.tick_params(axis='both', which='both', labelsize=4)
        self.gui_components.ax.legend()
        self.gui_components.ax.grid(True)

        self.gui_components.canvas.draw()

    def simulate_and_plot(self):
        investment_simulation = self.run_simulation()
        print("Simulation Results DataFrame:")
        print(investment_simulation)
        self.plot_simulation(investment_simulation)
        # Add this line to check the DataFrame columns
        print("DataFrame Columns:", investment_simulation.columns)
        front_end_df = investment_simulation[[
            'investment_amount', 'tokens_bought', 'total_tokens', 'total_invested', 'current_value',
            'return_on_investment']]
        self.update_table(front_end_df)
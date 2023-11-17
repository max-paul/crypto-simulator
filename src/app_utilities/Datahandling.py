import ccxt
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd


class DataHandling:
    def __init__(self, app):
        self.app = app

    def get_exchange_symbols(self):
        exchange = getattr(ccxt, self.app.chosen_exchange.get())()
        return exchange.load_markets().keys()

    def update_symbol_part_menu(self):
        self.app.chosen_part.set("")  # Clear the current selection
        part_menu = ttk.Combobox(self.app.master, textvariable=self.app.chosen_part,
                                 values=sorted(self.app.symbol_parts))
        part_menu.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    def update_symbol_menu(self):
        symbol_menu = ttk.Combobox(self.app.master, textvariable=self.app.crypto_symbol,
                                   values=self.app.filtered_symbols)
        symbol_menu.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    def display_symbol_parts(self, symbols):
        """Display the available cryptocurrency symbol parts to the user."""
        symbol_parts = set(symbol.split("/")[0] for symbol in symbols)
        return symbol_parts  # Return symbol_parts

    def filter_symbols_by_part(self, symbols, chosen_part):
        """Filter symbols based on the chosen part."""
        return [symbol for symbol in symbols if symbol.startswith(f"{chosen_part}/")]



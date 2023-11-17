import ccxt
import tkinter as tk
from tkinter import ttk
from datetime import datetime,timedelta
import pandas as pd

class DataHandling:
    def __init__(self, app):
        self.app = app

    def get_exchange_symbols(self):
        exchange = getattr(ccxt, self.app.chosen_exchange.get())()
        return exchange.load_markets().keys()

    def update_symbol_part_menu(self):
        self.app.chosen_part.set("")  # Clear the current selection
        part_menu = ttk.Combobox(self.app.master, textvariable=self.app.chosen_part, values=sorted(self.app.symbol_parts))
        part_menu.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    def update_symbol_menu(self):
        symbol_menu = ttk.Combobox(self.app.master, textvariable=self.app.crypto_symbol, values=self.app.filtered_symbols)
        symbol_menu.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
    def display_symbol_parts(self, symbols):
        """Display the available cryptocurrency symbol parts to the user."""
        symbol_parts = set(symbol.split("/")[0] for symbol in symbols)
        return symbol_parts  # Return symbol_parts
    def filter_symbols_by_part(self, symbols, chosen_part):
        """Filter symbols based on the chosen part."""
        return [symbol for symbol in symbols if symbol.startswith(f"{chosen_part}/")]

    def get_historical_crypto_prices(self, exchange, symbol, timeframe, limit, since):
        """Fetch historical cryptocurrency prices and return a DataFrame."""
        since_timestamp = int(since.timestamp() * 1000)
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit, since=since_timestamp)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def calculate_since_date(self, days_in_past):
        """Calculate the datetime object for the specified number of days in the past."""
        return datetime.now() - timedelta(days=days_in_past)

    def calculate_average(self, df):
        """Calculate the average of low and high prices and add it to the DataFrame."""
        df['average-daily'] = (df['low'] + df['high']) / 2

    def calculate_token_amount(self, df, investment, fee):
        """Calculate the amount of the token bought for $5 with a $1 fee and keep track of the rolling total invested."""
        df['amount_bought'] = (investment - fee) / df['low']

    def weekly_average(self, df):
        """Calculate the weekly average of the DataFrame."""
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        weekly_df = df.resample('W-Mon').mean()
        weekly_df.reset_index(inplace=True)
        self.rename_column(weekly_df, "average-daily", "average-weekly")
        return weekly_df

    def rename_column(self, df, old_column_name, new_column_name):
        """Rename a column in the DataFrame."""
        df.rename(columns={old_column_name: new_column_name}, inplace=True)


    def simulate_weekly_investment(self, df, weekly_investment, fee):
        """Simulate weekly investments and update the DataFrame."""
        df['weekly_investment'] = weekly_investment
        df['fee'] = fee
        df['investment_amount'] = df['weekly_investment'] - df['fee']

        df['tokens_bought'] = df['investment_amount'] / df['low']

        # Calculate the total tokens and running total
        df['total_tokens'] = df['tokens_bought'].cumsum()

        # Calculate the total invested and running total
        df['total_invested'] = df['investment_amount'].cumsum()

        # Calculate the current value of the investment
        df['current_value'] = df['total_tokens'] * df['close']

        # Calculate the return on investment
        df['return_on_investment'] = df['current_value'] - df['total_invested']



import ccxt
import pandas as pd
from datetime import datetime, timedelta


class Simulation:
    def __init__(self, app):
        self.app = app

    def run_simulation(self):
        exchange = getattr(ccxt, self.app.chosen_exchange.get())()
        since = self.calculate_since_date(self.app.days_in_past.get())
        historical_crypto_prices = self.get_historical_crypto_prices(
            exchange, self.app.crypto_symbol.get(), '1d', self.app.days_in_past.get(), since
        )
        self.calculate_average(historical_crypto_prices)
        self.calculate_token_amount(historical_crypto_prices, investment=5, fee=1)
        historical_crypto_prices = self.weekly_average(historical_crypto_prices)

        if self.app.days_in_past.get() > len(historical_crypto_prices):
            print("Either the rate limit was reached or the exchange didn't have sufficient information")

        weekly_investment = self.app.weekly_investment.get()
        fee = self.app.fee.get()

        self.simulate_weekly_investment(historical_crypto_prices, weekly_investment, fee)
        return historical_crypto_prices

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

    def get_historical_crypto_prices(self, exchange, symbol, timeframe, limit, since):
        """Fetch historical cryptocurrency prices and return a DataFrame."""
        since_timestamp = int(since.timestamp() * 1000)
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit, since=since_timestamp)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

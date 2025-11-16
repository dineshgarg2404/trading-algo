import pandas as pd
import numpy as np

class DataManager:
    """
    Manages historical data for backtesting.

    This class is responsible for fetching and preparing historical data for the
    backtesting engine. Since a real data source is not available, this class
    generates synthetic data for demonstration purposes.

    DATA GENERATION:
    ================

    - **Synthetic Price Data**: Generates a synthetic price series for NIFTY
      using a random walk model. This simulates realistic price movements.

    - **Date Range**: Creates data for the last five years, as requested.

    - **Output Format**: Returns a pandas DataFrame with a DatetimeIndex and a
      'price' column, which is the format expected by the backtesting engine.
    """

    def get_historical_data(self, years=5):
        """
        Generate synthetic historical NIFTY data for the last few years.

        Args:
            years (int): The number of years of historical data to generate.

        Returns:
            pd.DataFrame: A DataFrame containing the synthetic price data.
        """
        end_date = pd.to_datetime('today')
        start_date = end_date - pd.DateOffset(years=years)

        date_range = pd.date_range(start=start_date, end=end_date, freq='B')

        # Generate a random walk for the NIFTY price
        initial_price = 24000
        daily_volatility = 0.01

        returns = np.random.normal(0, daily_volatility, len(date_range))
        price_changes = np.exp(returns)

        prices = initial_price * np.cumprod(price_changes)

        df = pd.DataFrame({'price': prices}, index=date_range)

        return df

if __name__ == '__main__':
    data_manager = DataManager()
    historical_data = data_manager.get_historical_data()
    print("Generated Historical Data:")
    print(historical_data.head())
    print(historical_data.tail())

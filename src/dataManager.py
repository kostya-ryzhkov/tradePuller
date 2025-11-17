# src/data_manager.py

import os
import yfinance as yf
import pandas as pd
import configparser
from datetime import datetime, timedelta

class DataManager:
    """
    Handles all data fetching, loading, and saving operations.
    """
    def __init__(self, config_path='config.ini'):
        """
        Initializes the DataManager by loading settings from the config file.
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        
        # Store paths from the config file
        self.data_folder = config['DefaultPaths']['data_folder']
        
        # Ensure the data directory exists
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        print("DataManager initialized. Data will be stored in:", self.data_folder)

    def get_stock_data(self, ticker, start_date, end_date):
        """
        Fetches stock data, implementing intelligent caching to minimize downloads.

        Args:
            ticker (str): The stock ticker symbol (e.g., 'AAPL').
            start_date (str): The desired start date in 'YYYY-MM-DD' format.
            end_date (str): The desired end date in 'YYYY-MM-DD' format.

        Returns:
            pandas.DataFrame: A DataFrame containing the requested stock data, or None if an error occurs.
        """
        # Sanitize ticker to be uppercase for consistent file naming
        ticker = ticker.upper()
        file_path = os.path.join(self.data_folder, f"{ticker}.csv")
        
        # Convert string dates to datetime objects for comparison
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        
        try:
            # --- Caching Logic ---
            if os.path.exists(file_path):
                print(f"Local data found for {ticker}. Checking for updates...")
                local_data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
                
                last_saved_date = local_data.index.max()
                
                # If local data is already up-to-date, just return it
                if last_saved_date >= end_date_obj:
                    print(f"Local data for {ticker} is already up to date.")
                    # Filter and return the requested date range from the local file
                    return local_data.loc[start_date:end_date]

                # Adjust the start date to pull only the missing data
                pull_start_date = last_saved_date + timedelta(days=1)
                
            else:
                print(f"No local data for {ticker}. Fetching entire date range.")
                local_data = pd.DataFrame()
                pull_start_date = start_date_obj

            # --- Data Fetching ---
            if pull_start_date <= end_date_obj:
                print(f"Fetching new data for {ticker} from {pull_start_date.strftime('%Y-%m-%d')} to {end_date_obj.strftime('%Y-%m-%d')}...")
                new_data = yf.download(ticker, start=pull_start_date, end=end_date_obj + timedelta(days=1), progress=False)
                
                if new_data.empty:
                    print(f"No new data found for {ticker} in the specified range.")
                else:
                    # Combine old and new data
                    combined_data = pd.concat([local_data, new_data])
                    # Remove potential duplicates and sort by date
                    combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
                    combined_data.sort_index(inplace=True)
                    
                    # Save the updated data back to the CSV
                    combined_data.to_csv(file_path)
                    print(f"Successfully updated local data for {ticker}.")
                    local_data = combined_data

            # Return the final data, filtered by the user's original request
            return local_data.loc[start_date:end_date]

        except Exception as e:
            print(f"An error occurred while fetching data for {ticker}: {e}")
            return None
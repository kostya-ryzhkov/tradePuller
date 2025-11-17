# src/main.py

from dataManager import DataManager
from visualizer import Visualizer
from datetime import datetime, timedelta
import sys

def get_user_tickers():
    """Prompts the user to enter stock tickers and validates the input."""
    while True:
        user_input = input("Enter stock ticker(s) (e.g., AAPL, MSFT, GOOG), or 'q' to quit: ")
        if user_input.lower() in ['q', 'quit']:
            return None
        
        # Process the input: split by comma, remove whitespace, uppercase, and filter out empty strings
        tickers = [ticker.strip().upper() for ticker in user_input.split(',') if ticker.strip()]
        
        if tickers:
            return tickers
        else:
            print("Invalid input. Please enter at least one ticker.")

def get_user_dates():
    """Prompts the user for start and end dates with intelligent defaults."""
    # Default dates
    end_date_default = datetime.now()
    start_date_default = end_date_default - timedelta(days=365)
    
    # Get start date
    while True:
        start_date_str = input(f"Enter start date (YYYY-MM-DD) [Default: {start_date_default.strftime('%Y-%m-%d')}]: ")
        if not start_date_str:
            return start_date_default.strftime('%Y-%m-%d'), end_date_default.strftime('%Y-%m-%d')
        try:
            # Validate format
            datetime.strptime(start_date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Get end date
    while True:
        end_date_str = input(f"Enter end date (YYYY-MM-DD) [Default: {end_date_default.strftime('%Y-%m-%d')}]: ")
        if not end_date_str:
            end_date_str = end_date_default.strftime('%Y-%m-%d')
        try:
            # Validate format and ensure end date is not before start date
            if datetime.strptime(end_date_str, '%Y-%m-%d') < datetime.strptime(start_date_str, '%Y-%m-%d'):
                print("End date cannot be before start date.")
                continue
            return start_date_str, end_date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def run_app():
    """
    The main function to run the stock analysis application.
    """
    # --- A clean welcome banner for the UI ---
    print("=" * 50)
    print("      Welcome to the Stock Spread Analyzer")
    print("=" * 50)
    
    # --- Initialization ---
    # Create instances of our manager classes
    try:
        data_manager = DataManager()
        visualizer = Visualizer()
    except Exception as e:
        print(f"Error during initialization: {e}")
        print("Please ensure your config.ini is set up correctly.")
        sys.exit(1) # Exit if setup fails

    # --- Main Application Loop ---
    while True:
        tickers = get_user_tickers()
        if tickers is None:
            break # User chose to quit

        start_date, end_date = get_user_dates()

        print("\nStarting analysis...")
        print("-" * 20)
        
        # --- Orchestration ---
        for ticker in tickers:
            print(f"Processing: {ticker}")
            
            # 1. Get data using the DataManager
            stock_data = data_manager.get_stock_data(ticker, start_date, end_date)
            
            # 2. Generate plot using the Visualizer
            if stock_data is not None and not stock_data.empty:
                visualizer.plot_high_low_spread(stock_data, ticker, start_date, end_date)
            else:
                print(f"Could not generate plot for {ticker} due to missing data.")
            print("-" * 20)

        print("\nAnalysis complete for all requested tickers.")
        print(f"All charts have been saved to the '{visualizer.output_folder}' directory.")
        
        # Ask to run again
        run_again = input("\nDo you want to analyze more stocks? (y/n): ").lower()
        if run_again != 'y':
            break

    print("\nThank you for using the Stock Spread Analyzer. Goodbye!")


# --- Python's standard entry point ---
if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nApplication interrupted by user. Exiting.")
        sys.exit(0)
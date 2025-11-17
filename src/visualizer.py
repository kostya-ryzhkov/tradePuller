# src/visualizer.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import configparser

class Visualizer:
    """
    Handles the creation and saving of all visualizations.
    """
    def __init__(self, config_path='config.ini'):
        """
        Initializes the Visualizer by loading settings from the config file.
        """
        config = configparser.ConfigParser()
        config.read(config_path)

        # Load visualization settings
        self.style = config['Visualization']['style']
        self.main_color = config['Visualization']['main_color']
        self.font_color = config['Visualization']['font_color']
        self.grid_color = config['Visualization']['grid_color']
        self.font_size = int(config['Visualization']['font_size'])
        self.fig_width = int(config['Visualization']['figure_width'])
        self.fig_height = int(config['Visualization']['figure_height'])

        # Load output path
        self.output_folder = config['DefaultPaths']['output_folder']
        
        # Ensure the output directory exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        print("Visualizer initialized. Charts will be saved in:", self.output_folder)

    def plot_high_low_spread(self, data, ticker, start_date, end_date):
        """
        Generates and saves a plot of the daily High-Low spread for a given stock.

        Args:
            data (pandas.DataFrame): DataFrame containing the stock data. Must include 'High' and 'Low' columns.
            ticker (str): The stock ticker symbol for titling.
            start_date (str): The start date for titling.
            end_date (str): The end date for titling.
        """
        # Sanitize ticker
        ticker = ticker.upper()

        if data is None or data.empty:
            print(f"No data provided for {ticker}. Skipping plot generation.")
            return

        try:
            # --- Data Preparation ---
            # Calculate the spread, which is the core metric we want to visualize
            data['Spread'] = data['High'] - data['Low']

            # --- Plotting ---
            plt.style.use(self.style)
            fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))

            # Plot the spread data
            ax.plot(data.index, data['Spread'], color=self.main_color, linewidth=1.5)

            # --- Styling (The "Bloomberg" Look) ---
            # Set title and labels
            title = f"{ticker}: Daily High-Low Spread ({start_date} to {end_date})"
            ax.set_title(title, color=self.font_color, fontsize=self.font_size + 4, pad=20)
            ax.set_ylabel('Price Spread ($)', color=self.font_color, fontsize=self.font_size)
            
            # Style the axes and grid
            ax.grid(True, color=self.grid_color, linestyle='--', linewidth=0.5)
            ax.tick_params(axis='x', colors=self.font_color, labelsize=self.font_size - 2)
            ax.tick_params(axis='y', colors=self.font_color, labelsize=self.font_size - 2)
            
            # Make the surrounding box (spines) less prominent
            for spine in ax.spines.values():
                spine.set_edgecolor(self.grid_color)
            
            fig.tight_layout() # Adjust plot to prevent labels from overlapping

            # --- Saving the Figure ---
            filename = f"{ticker}_spread_{start_date}_to_{end_date}.png"
            save_path = os.path.join(self.output_folder, filename)
            
            plt.savefig(save_path, dpi=300) # dpi=300 for high resolution
            plt.close(fig) # Close the figure to free up memory
            
            print(f"Successfully saved chart to: {save_path}")

        except Exception as e:
            print(f"An error occurred during plotting for {ticker}: {e}")
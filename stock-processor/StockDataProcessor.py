import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Capture INFO, WARNING, ERROR, and DEBUG logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs.txt", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class StockDataProcessor:
    def __init__(self, csv_file, date_column="Date"):
        """
        Initializes the StockDataProcessor class.

        :param csv_file: Path to the CSV file
        :param date_column: The column name containing dates
        """
        self.csv_file = csv_file
        self.date_column = date_column
        self.df = self._load_data()
        self.clean_headers()

    def _load_data(self):
        """Loads CSV data into a Pandas DataFrame with date parsing."""
        try:
            df = pd.read_csv(self.csv_file, parse_dates=[self.date_column])
            df.set_index(self.date_column, inplace=True)
            df = df.sort_index()
            logging.info(f"✅ Successfully loaded {len(df)} records.")
            return df
        except Exception as e:
            logging.error(f"❌ Error loading data: {e}")
            return pd.DataFrame()

    def clean_headers(self):
        """Removes leading and trailing spaces from column names."""
        if not self.df.empty:
            self.df.columns = self.df.columns.str.strip()
            logging.info("✅ Column headers cleaned.")

    def clean_data(self):
        """Handles missing values by forward-filling."""
        if self.df.empty:
            logging.warning("⚠ No data to clean!")
            return
        self.df.fillna(method="ffill", inplace=True)
        logging.info("✅ Missing values handled using forward-fill.")

    def add_moving_averages(self, column="Close"):
        """
        Adds moving averages for 30, 50, and 100 days.

        :param column: Column to compute moving averages on (default: 'Close')
        """
        if column not in self.df.columns:
            logging.warning(f"⚠ Column '{column}' not found!")
            return

        self.df["MA_30"] = self.df[column].rolling(window=30).mean()
        self.df["MA_50"] = self.df[column].rolling(window=50).mean()
        self.df["MA_100"] = self.df[column].rolling(window=100).mean()

        logging.info("✅ Moving averages (30, 50, 100 days) added.")


    def resample_data(self, freq="W"):
        """
        Resamples the dataset to a different frequency.

        :param freq: Pandas frequency string (D=daily, W=weekly, M=monthly)
        :return: Resampled DataFrame
        """
        if self.df.empty:
            logging.warning("⚠ No data to resample!")
            return pd.DataFrame()
        return self.df.resample(freq).mean()

    def compute_statistics(self, column="Close"):
        """
        Computes basic statistics for a given column.

        :param column: Column to analyze (default: 'Close')
        :return: Dictionary with min, max, and mean values
        """
        if column not in self.df.columns:
            logging.warning(f"⚠ Column '{column}' not found!")
            return {}
        stats = {
            "min": self.df[column].min(),
            "max": self.df[column].max(),
            "mean": self.df[column].mean()
        }
        logging.info(f"📊 Statistics for {column}: {stats}")
        return stats

    def plot_matplotlib(self, column="Close"):
        """Plots the selected column using Matplotlib."""
        if column not in self.df.columns:
            logging.warning(f"⚠ Column '{column}' not found!")
            return
        plt.figure(figsize=(10, 5))
        plt.plot(self.df.index, self.df[column], label=column, color="blue")
        plt.plot(self.df.index, self.df["MA_30"], label="30-Day MA", color="green", linestyle="--")
        plt.plot(self.df.index, self.df["MA_50"], label="50-Day MA", color="orange", linestyle="--")
        plt.plot(self.df.index, self.df["MA_100"], label="100-Day MA", color="red", linestyle="--")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title(f"{column} Price Over Time with Moving Averages")
        plt.legend()
        plt.show()
        logging.info(f"📈 Matplotlib plot displayed for {column}.")

    def plot_plotly(self, column="Close"):
        """Plots the selected column using Plotly for interactive visualization."""
        if column not in self.df.columns:
            logging.warning(f"⚠ Column '{column}' not found!")
            return
        fig = px.line(self.df, x=self.df.index, y=[column, "MA_30", "MA_50", "MA_100"],
                      labels={"value": "Price"}, title=f"{column} Price Over Time with Moving Averages")
        fig.show()
        logging.info(f"📊 Plotly interactive plot displayed for {column}.")

# Usage Example
if __name__ == "__main__":
    stock_processor = StockDataProcessor("data/MEG.csv")
    stock_processor.clean_data()
    stock_processor.add_moving_averages("Close")
    print(stock_processor.compute_statistics("Close"))
    stock_processor.plot_matplotlib("Close")
    stock_processor.plot_plotly("Close")

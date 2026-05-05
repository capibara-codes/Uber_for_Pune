import os
import pandas as pd
import requests
import logging

# Configure logging to track pipeline health
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataExtractor:
    def __init__(self, raw_data_path="data/raw"):
        self.raw_data_path = raw_data_path
        # Create directory if it doesn't exist
        if not os.path.exists(self.raw_data_path):
            os.makedirs(self.raw_data_path)
            logging.info(f"Created directory: {self.raw_data_path}")

    def fetch_from_url(self, url, filename):
        """
        Extracts data from a remote URL (CSV or Parquet).
        Useful for datasets like NYC Taxi or open-source transit data.
        """
        target_path = os.path.join(self.raw_data_path, filename)
        
        try:
            logging.info(f"Starting extraction from {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status() # Check for HTTP errors
            
            with open(target_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logging.info(f"Extraction successful! File saved at: {target_path}")
            return target_path
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to extract data: {e}")
            return None

    def load_to_dataframe(self, file_path):
        """
        Loads the raw file into a Pandas DataFrame for the transformation layer.
        """
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.parquet'):
            return pd.read_parquet(file_path)
        else:
            logging.error("Unsupported file format.")
            return None

if __name__ == "__main__":
    # Example Usage:
    # This URL is a sample of public transit/taxi data often used for these projects
    SAMPLE_URL = "https://github.com/uber-web/kepler.gl-data/raw/master/nyctrips/data.csv"
    
    extractor = DataExtractor()
    raw_file = extractor.fetch_from_url(SAMPLE_URL, "raw_transit_data.csv")
    
    if raw_file:
        df = extractor.load_to_dataframe(raw_file)
        print(f"Extraction Complete. Loaded {len(df)} rows.")

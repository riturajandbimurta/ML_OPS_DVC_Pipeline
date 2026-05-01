import pandas as pd
import os
from sklearn.model_selection import train_test_split
import logging

#making log folder in variable log_dir then making sure it doesnet crash if such folder already exists 
log_dir = 'logs'
os.makedirs(log_dir,exist_ok=True)

#logging configuration :What is logging? It's Python's built-in way of recording what your program is doing — like a diary for your code!
logger = logging.getLogger('data_ingestion') # Create a logger and name it 'data_ingestion'
logger.setLevel('DEBUG')#Record EVERYTHING — even tiny details

#Send log messages to the CONSOLE/TERMINAL"
console_handler = logging.StreamHandler()
console_handler.setFormatter('DEBUG')

log_file_path = os.path.join(log_dir,'data_ingestion.log')## Where to save? → "log/data_ingestion.log"
file_handler = logging.FileHandler(log_file_path)## Create file handler# → opens/creates that file
file_handler.setLevel('DEBUG')# Record everything# → writes ALL levels to file

formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#Both handlers share the same formatter — so terminal and file look identical!

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)#Tell the logger to ALSO send messages to terminal"
logger.addHandler(file_handler)#Tell the logger to ALSO send messages to file"

def load_data(data_url: str)-> pd.DataFrame:
    """Load data from csv file"""
    try:
        df = pd.read_csv(data_url)
        logger.debug('Data loaded from %s',data_url)
        return df
    except pd.errors.ParserError as e:
        logger.error('Fail to load the csv file %s',e)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the data: %s', e)
        raise
    
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data."""
    try:
        df.drop(columns = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace = True)
        df.rename(columns = {'v1': 'target', 'v2': 'text'}, inplace = True)
        logger.debug('Data preprocessing completed')
        return df
    except KeyError as e:
        logger.error('Missing column in the dataframe: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error during preprocessing: %s', e)
        raise
def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    """Save the train and test datasets."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logger.debug('Train and test data saved to %s', raw_data_path)
    except Exception as e:
        logger.error('Unexpected error occurred while saving the data: %s', e)
        raise
    
def main():
    try:
        test_size = 0.2 
        data_path = "https://raw.githubusercontent.com/riturajandbimurta/ML_OPS_DVC_Pipeline/refs/heads/master/experiments/spam.csv"
        df = load_data(data_url=data_path)
        final_df = preprocess_data(df)
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=2)
        save_data(train_data, test_data, data_path='./data')
    except Exception as e:
        logger.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")
        
if __name__== '__main__': #is a safety guard — it makes sure your pipeline only runs when YOU explicitly run the file, not accidentally when someone imports it
     main()

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "raw" / "5-Starfish.csv"

def get_data():
    """ load data from csv file"""
    df = pd.read_csv(DATA_PATH)
    return df.to_dict(orient="records")

def load_df():
    return pd.DataFrame(get_data())
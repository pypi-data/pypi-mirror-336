import os
import pickle
import sqlite3

import pandas as pd

# Define the path to the data directory inside the toxichempy package
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_sample_data_path(filename: str) -> str:
    """
    Retrieve the absolute path of a sample dataset stored in the library.

    Parameters:
    ----------
    filename : str
        The name of the dataset file (e.g., 'iris.csv').

    Returns:
    --------
    str
        Full path to the dataset file.
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Sample dataset '{filename}' not found.")
    return file_path


def load_sample_data(name: str) -> pd.DataFrame:
    """
    Load a sample dataset in any available format.

    Parameters:
    ----------
    name : str
        The dataset name without an extension (e.g., 'iris').

    Returns:
    --------
    pd.DataFrame
        The dataset loaded into a pandas DataFrame.
    """
    extensions = [".csv", ".json", ".xlsx", ".pkl", ".h5", ".db"]

    for ext in extensions:
        file_path = os.path.join(DATA_DIR, f"{name}{ext}")

        if os.path.exists(file_path):
            if ext == ".csv":
                return pd.read_csv(file_path)
            elif ext == ".json":
                return pd.read_json(file_path)
            elif ext in [".xlsx"]:
                return pd.read_excel(file_path)
            elif ext == ".pkl":
                with open(file_path, "rb") as f:
                    return pickle.load(f)
            elif ext == ".h5":
                return pd.read_hdf(file_path, key="df")
            elif ext == ".db":
                conn = sqlite3.connect(file_path)
                try:
                    return pd.read_sql(
                        "SELECT * FROM iris", conn
                    )  # Assuming table name is 'iris'
                finally:
                    conn.close()

    raise FileNotFoundError(
        f"No available dataset formats found for '{name}' in {DATA_DIR}."
    )

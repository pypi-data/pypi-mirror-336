import pickle
import sqlite3
from pathlib import Path

import pandas as pd


def read_file(file_path: str, delimiter=None, **kwargs) -> pd.DataFrame:
    """
    Reads a file into a pandas DataFrame.

    Supports: CSV, TSV, Excel, JSON, Pickle, SQLite, HDF5, TXT.

    Parameters:
    -----------
    file_path : str
        Path to the source file.
    delimiter : str, optional
        Delimiter for text files (default: None).
    **kwargs : dict
        Additional parameters for reading.

    Returns:
    --------
    pd.DataFrame
        Data from the file.
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = Path(file_path).suffix.lower()

    if extension == ".csv":
        return pd.read_csv(file_path, **kwargs)
    elif extension == ".tsv":
        return pd.read_csv(file_path, sep="\t", **kwargs)
    elif extension in [".xlsx", ".xls"]:
        return pd.read_excel(file_path, **kwargs)
    elif extension == ".json":
        return pd.read_json(file_path, **kwargs)
    elif extension in [".pkl", ".pickle"]:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    elif extension in [".h5", ".hdf5", ".hdf"]:
        return pd.read_hdf(file_path, key=kwargs.get("key", "df"))
    elif extension in [".db", ".sqlite", ".sqlite3"]:
        if "query" not in kwargs:
            raise ValueError("For SQLite, 'query' parameter is required.")
        conn = sqlite3.connect(file_path)
        try:
            return pd.read_sql(kwargs["query"], conn)
        finally:
            conn.close()
    elif extension == ".txt":
        # If no delimiter is provided, default to tab.
        if delimiter is None:
            delimiter = "\t"
        try:
            return pd.read_csv(file_path, delimiter=delimiter, **kwargs)
        except pd.errors.ParserError:
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.readlines()
            return pd.DataFrame({"text": data})  # Store as a single-column DataFrame
    else:
        raise ValueError(f"Unsupported file format: {extension}")


def write_file(df: pd.DataFrame, file_path: str, **kwargs) -> bool:
    """
    Writes a pandas DataFrame to a file.

    Supported Formats: CSV, TSV, Excel, JSON, Pickle, SQLite, HDF5, TXT.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to write.
    file_path : str
        Output file path.
    **kwargs : dict
        Additional parameters for writing.

    Returns:
    --------
    bool
        True if writing is successful.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    extension = Path(file_path).suffix.lower()

    if extension == ".csv":
        df.to_csv(file_path, index=False, **kwargs)
    elif extension == ".tsv":
        df.to_csv(file_path, sep="\t", index=False, **kwargs)
    elif extension in [".xlsx", ".xls"]:
        df.to_excel(file_path, index=False, **kwargs)
    elif extension == ".json":
        df.to_json(file_path, orient="records", **kwargs)
    elif extension in [".pkl", ".pickle"]:
        with open(file_path, "wb") as f:
            pickle.dump(df, f)
    elif extension in [".h5", ".hdf5", ".hdf"]:
        df.to_hdf(file_path, key=kwargs.get("key", "df"), mode="w", **kwargs)
    elif extension in [".db", ".sqlite", ".sqlite3"]:
        table_name = kwargs.get("table_name")
        if not table_name:
            raise ValueError("For SQLite, 'table_name' parameter is required.")
        conn = sqlite3.connect(file_path)
        try:
            df.to_sql(
                table_name, conn, if_exists=kwargs.get("if_exists", "fail"), index=False
            )
        finally:
            conn.close()
    elif extension == ".txt":
        # Remove any conflicting 'delimiter' keyword so only 'sep' is used.
        kwargs.pop("delimiter", None)
        sep = kwargs.pop("sep", "\t")
        df.to_csv(file_path, sep=sep, index=False, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

    return True


def convert_file(source_path: str, target_path: str, **kwargs) -> bool:
    """
    Converts a file from one format to another.

    Parameters:
    -----------
    source_path : str
        Path to the source file.
    target_path : str
        Path to the destination file.
    **kwargs : dict
        Additional parameters for reading/writing.

    Returns:
    --------
    bool
        True if conversion is successful, False otherwise.
    """
    source_kwargs = kwargs.pop("source_kwargs", {})
    target_kwargs = kwargs.pop("target_kwargs", {})
    df = read_file(source_path, **source_kwargs)
    return write_file(df, target_path, **target_kwargs)

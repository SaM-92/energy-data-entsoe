# data_loader.py
import pandas as pd

def load_data(uploaded_file):
    """
    Load data from an uploaded file into a pandas DataFrame.

    Args:
        uploaded_file: The file uploaded by the user.

    Returns:
        A pandas DataFrame containing the data from the uploaded file.
    """
    na_values = ["nan", "n/e", "no", "na"]
    file_name = uploaded_file.name
    if file_name.endswith('.csv'):
        return pd.read_csv(uploaded_file, na_values=na_values)
    elif file_name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(uploaded_file, na_values=na_values)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

def clean_data(df_read, time_column):
    """
    Clean the data by setting the time column and handling missing values.

    Args:
        df_read: The DataFrame to be cleaned.
        time_column: The name of the column containing time data.

    Returns:
        The cleaned DataFrame.
    """
    df_read.set_index(time_column, inplace=True)
    df_read.dropna(inplace=True)
    return df_read.reset_index()

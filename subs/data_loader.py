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

def process_data_for_analysis(df_read, time_column):
    """
    Prepares the data for analysis by setting a specified time column as the index and 
    filtering the DataFrame to exclude rows starting from the first occurrence of invalid data.

    This function sets the 'time_column' as the DataFrame's index. It then identifies the first
    occurrence of invalid data, indicated by "-", and excludes all rows from this point onwards, 
    assuming that the data following this point may not be reliable or relevant for analysis.

    Args:
        df_read: pandas DataFrame
            The DataFrame that needs to be prepared.
        time_column: str
            The name of the column in 'df_read' that contains time data.

    Returns:
        pandas DataFrame: The prepared DataFrame with 'time_column' set as the index and
                          data filtered up to the first invalid entry.
    """
    # Set the 'time_column' as the index explicitly
    df_read.set_index(time_column, inplace=True)
    # Find the first row with '-'
    # ENTSO-e puts "-" when data is missing for the future
    if (df_read == "-").any().any():
        first_invalid_row = df_read.eq("-").any(axis=1).idxmax()
        skip_invalid_row = "False"
    else:
        skip_invalid_row = "True"

    if skip_invalid_row == True:
        first_invalid_row_time = first_invalid_row.split(" - ")[0]

        first_invalid_row_time = pd.to_datetime(
            first_invalid_row_time, format="%d.%m.%Y %H:%M"
        )
   
    # reset the index
    df_read.reset_index(inplace=True)
    return df_read

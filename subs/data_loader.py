# data_loader.py
import pandas as pd
import numpy as np

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
    filtering the DataFrame to manage rows with invalid data, indicated by "-".

    This function sets the 'time_column' as the DataFrame's index and checks for the presence of invalid data.
    It marks the first occurrence of invalid data (if any) and provides options for further handling of such data.
    The function returns the DataFrame with the original index reset, along with flags indicating the presence of 
    invalid data and the time of the first invalid row.

    Args:
        df_read: pandas DataFrame
            The DataFrame that needs to be prepared.
        time_column: str
            The name of the column in 'df_read' that contains time data.

    Returns:
        pandas DataFrame: The prepared DataFrame with the original index reset.
        skip_invalid_row: str
            A flag ("True" or "False") indicating whether to skip the row with the first occurrence of invalid data.
        first_invalid_row_time: datetime or np.nan
            The timestamp of the first invalid row, if present; otherwise, np.nan.
    """
    # Set the 'time_column' as the index explicitly
    df_read.set_index(time_column, inplace=True)
    # Find the first row with '-'
    # ENTSO-e puts "-" when data is missing for the future
    first_invalid_row_time =np.nan
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
    return df_read , skip_invalid_row , first_invalid_row_time


def process_uploaded_file(df, job_filter):
    """
    Processes an uploaded file by converting data types to numeric and handling missing values.

    This function takes a DataFrame and a job filter option. It first converts the data types of all
    columns, except the first one, to numeric, handling any errors with coercion. It then processes
    missing values in the DataFrame based on the specified job filter option, which can be to remove,
    interpolate, or forward/backward fill the missing values.

    Args:
        df: pandas DataFrame
            The DataFrame extracted from the uploaded file.
        job_filter: str
            The method chosen for handling missing values. Options include 'Remove',
            'Interpolate', and 'Backward/Forward Filling'.

    Displays:
        The processed DataFrame is displayed in the Streamlit app.
    """


    # Convert data types of columns to numeric, starting from the second column
    for column in df.columns[1:]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Handle missing values based on the job_filter option
    for column in df.columns[1:]:
        if job_filter == "Remove":
            # Remove rows with missing values
            df = df.dropna()
        elif job_filter == "Interpolate":
            # Interpolate missing values
            df = df.interpolate()
        elif job_filter == "Backward/Forward Filling":
            # Forward fill followed by backward fill for missing values
            df = df.ffill().bfill()
    return df        


def convert_time(df, time_column):
    """
    Converts a time column in a DataFrame to a consistent datetime format.

    Args:
        df (pd.DataFrame): The DataFrame containing the time data.
        time_column (str): The name of the time column to be converted.

    Returns:
        pd.DataFrame: The DataFrame with the time column converted to datetime.
    """

    if " - " in df[time_column].iloc[0]:
        # Split the time interval into start and end times
        df["Start Time"] = df[time_column].str.split(" - ", expand=True)[0]

        # Drop the original time column
        df.drop(time_column, inplace=True, axis=1)

        # Convert the "Start Time" to datetime
        df["Start Time"] = pd.to_datetime(df["Start Time"], format="mixed")

        # Assign the datetime values to the original time column name
        df[time_column] = df["Start Time"]

        # Drop the "Start Time" column
        df.drop("Start Time", inplace=True, axis=1)
    else:
        # Convert the time data to datetime
        df[time_column] = pd.to_datetime(df[time_column], format="mixed")

    return df


def process_time_resolution_and_duplicates(df_read, time_column, time_resolution_number, time_resolution_unit, skip_invalid_row, first_invalid_row_time):
    """
    Processes the DataFrame by setting time resolution, handling duplicates, and resampling.

    This function converts the selected time resolution to minutes, sets a specified time column as the index,
    and handles any potential duplicate index values. It then resamples the DataFrame based on the time resolution, 
    interpolating as necessary.

    Args:
        df_read: pandas DataFrame
            The DataFrame to be processed.
        time_column: str
            The name of the column containing time data.
        time_resolution_number: int
            The numeric part of the time resolution (e.g., '15' in '15 minutes').
        time_resolution_unit: str
            The unit part of the time resolution (e.g., 'minutes' or 'hours').
        skip_invalid_row: bool
            Flag indicating whether to skip processing the invalid row.
        first_invalid_row_time: datetime
            The time of the first invalid row, used to trim the DataFrame.

    Returns:
        pandas DataFrame: The processed DataFrame after resampling and handling duplicates.
    """

    # Convert the selected time resolution to minutes
    time_resolution_minutes = time_resolution_number * (60 if time_resolution_unit == "hours" else 1)

    # Set the 'time_column' as the index explicitly
    df_read.set_index(time_column, inplace=True)

    # Find the dataset frequency
    difference = df_read.index.to_series().diff()[1]
    minutes_difference = difference.total_seconds() / 60

    # Keep only the rows until the row before the first_invalid_row
    if not skip_invalid_row:
        df_read = df_read.loc[:first_invalid_row_time - pd.Timedelta(minutes=minutes_difference)]

    # Handle duplicates
    df_read = df_read[~df_read.index.duplicated()]

    # Convert columns to numeric data types
    df_read = df_read.apply(pd.to_numeric, errors="coerce")

    # Resample and interpolate the DataFrame based on the time resolution
    df_read = df_read.resample(f"{time_resolution_minutes}T").interpolate()

    return df_read


        
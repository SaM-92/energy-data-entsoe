import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
import missingno as msno
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
import json

# read csv from a github repo
# df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")


st.set_page_config(page_title="Data Master Mind", page_icon="🚀", layout="wide")

st.image("./header.png")

st.title("Empowering Insights: Navigating ENTSO-E Power System Data")
# st.markdown("### 🚀 Data Master Mind")
st.markdown("Created by Saeed Misaghian")


st.image("./logo.png", width=300)  # adjust width as needed


st.markdown("### 🔗 Upload your data")

# Create a file uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


# Check if a file has been uploaded
if uploaded_file is not None:
    # Define a list of strings that should be considered as NaN
    na_values = ["nan", "n/e", "no", "na"]
    # Read the uploaded CSV file
    df_read = pd.read_csv(uploaded_file, na_values=na_values)
    st.dataframe(df_read)
    fig_col_missing_values, _ = st.columns(2)
    with fig_col_missing_values:
        missing_values = df_read.isnull().sum()

        # Create a DataFrame for the missing values
        missing_df = pd.DataFrame(
            {
                "Column names": missing_values.index,
                "Missing Values": missing_values.values,
            }
        )

        # Create a bar chart with Plotly Express
        fig = px.bar(
            missing_df,
            x="Column names",
            y="Missing Values",
            title="💡 Number of Missing Values per Column",
        )

        # Set the layout to have a transparent background
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
        st.write(fig)

st.markdown("### ⚙️ Dealing with Missing Values")
st.markdown("📝 Please choose how you want to deal with missing values?")
options_to_drop = ["Remove", "Interpolate", "Backward/Forward Filling"]
job_filter2 = st.selectbox("Select the Job", options_to_drop)

if uploaded_file is not None:
    # Convert the data types of the columns to numeric
    for column in df_read.columns[1:]:
        df_read[column] = pd.to_numeric(df_read[column], errors="coerce")

    # Handle missing values for each column except the first one
    for column in df_read.columns[1:]:
        if job_filter2 == "Remove":
            # Remove rows with missing values
            df_read = df_read.dropna()
        elif job_filter2 == "Interpolate":
            # Interpolate missing values
            df_read = df_read.interpolate()
        elif job_filter2 == "Backward/Forward Filling":
            # Forward fill for missing values
            df_read = df_read.ffill()
            # Backward fill for any remaining missing values
            df_read = df_read.bfill()

    st.dataframe(df_read)

st.markdown("### ⏲️ Time Resolution Adjustment")

if uploaded_file is not None:
    # Ask the client for their preferred time resolution
    time_resolution_number = st.number_input(
        "Please enter your preferred time resolution number:", min_value=1
    )
    time_resolution_unit = st.selectbox(
        "Please select the unit of your preferred time resolution:",
        ["minutes", "hours"],
    )

    # Show the clients the list of their DataFrame columns and ask them to choose the column with date and time observations
    time_column = st.selectbox(
        "Please select the column with date and time observations:", df_read.columns
    )

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
            df["Start Time"] = pd.to_datetime(df["Start Time"], format="%d.%m.%Y %H:%M")

            # Assign the datetime values to the original time column name
            df[time_column] = df["Start Time"]

            # Drop the "Start Time" column
            df.drop("Start Time", inplace=True, axis=1)
        else:
            # Convert the time data to datetime
            df[time_column] = pd.to_datetime(df[time_column], format="%d.%m.%Y %H:%M")

        return df

    # Apply the function to your DataFrame
    df_read = convert_time(df_read, time_column)

    # Convert the selected time resolution to minutes
    time_resolution_minutes = time_resolution_number * (
        60 if time_resolution_unit == "hours" else 1
    )

    # Convert the selected time column to datetime
    # df_read[time_column] = pd.to_datetime(df_read[time_column])

    # Resample the data according to the selected time resolution
    df_read = df_read.resample(
        f"{time_resolution_minutes}T", on=time_column
    ).interpolate()

    st.dataframe(df_read)


st.markdown("### 🎨 Visualising the Results")


st.markdown("### 💾 Download the Results")

if uploaded_file is not None:
    # Create a dictionary for the metrics
    metrics_dict = {
        "Total dataset metrics": {
            "Root Mean Squared Error (RMSE)": f"{rmse}",
            "Coefficient of the Variation of the Root Mean Square Error (CVRMSE)": f"{cvrmse}",
            "Normalised mean bias error (NMBE)": f"{nmbe}",
            "Mean absolute error (MAE)": f"{mae}",
            "Range Normalised Root Mean Squared Error (RN_RMSE)": f"{rn_rmse}",
        }
    }

    # Convert the dictionary to a JSON string
    metrics_json = json.dumps(metrics_dict)

    # Create a download button for the JSON string
    st.download_button(
        label="Download metrics in JSON format",
        data=metrics_json,
        file_name="metrics.json",
        mime="application/json",
    )

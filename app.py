import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import plotly.graph_objects as go

st.set_page_config(page_title="Data Master Mind", page_icon="🚀", layout="wide")

st.image("./header.png")

st.title("Empowering Insights: Navigating ENTSO-E Power System Data")
st.markdown("Created by Saeed Misaghian")
st.markdown("📧 sam.misaqian@gmail.com")


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

    # Show the clients the list of their DataFrame columns and ask them to choose the column with date and time observations
    time_column = st.selectbox(
        "Please select the column with date and time observations:", df_read.columns
    )

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

    # Set the 'time_column' as the index explicitly
    df_read.set_index(time_column, inplace=True)

    # find the dataset frequency
    difference = df_read.index.to_series().diff()[1]
    minutes_difference = difference.total_seconds() / 60

    # Keep only the rows until the row before the first_invalid_row
    if skip_invalid_row == False:
        df_read = df_read.loc[
            : first_invalid_row_time - pd.Timedelta(minutes=minutes_difference)
        ]

    # Check for duplicate index values
    duplicates = df_read.index.duplicated()

    # Handle duplicates (for example, by keeping the first occurrence and dropping the others)
    df_read = df_read[~duplicates]
    # be sure that columns are not object (we have already taken care of nan etc.. so we should have only numbers)
    df_read = df_read.apply(pd.to_numeric, errors="coerce")

    df_read = df_read.resample(f"{time_resolution_minutes}T").interpolate()

    st.dataframe(df_read)


st.markdown("### 🎨 Visualising the Results")

import datetime

# Select a range of dates
start_date = datetime.date(2023, 7, 6)
end_date = datetime.date(2023, 7, 8)
date_of_interest = st.date_input("Select a date range", [start_date, end_date])

if uploaded_file is not None:
    df_day_of_interest = df_read.loc[
        date_of_interest[0]
        .strftime("%Y-%m-%d") : date_of_interest[1]
        .strftime("%Y-%m-%d")
    ]

    st.dataframe(df_day_of_interest)

    # Loop over each column in your DataFrame
    fig2 = go.Figure()
    for column in df_day_of_interest.columns:
        fig2.add_trace(
            go.Scatter(
                x=df_day_of_interest.index, y=df_day_of_interest[column], name=column
            )
        )

    # Display the figure in Streamlit
    st.plotly_chart(fig2, use_container_width=True)

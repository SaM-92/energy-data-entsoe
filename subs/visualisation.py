# visualization.py

import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import plotly.graph_objects as go


def visualize_missing_values(df):
    """
    Creates and displays a bar chart visualisation of missing values in each column of a DataFrame.

    This function takes a DataFrame, calculates the number of missing values in each column, and then
    uses Plotly Express to create a bar chart. 

    Args:
        df: pandas DataFrame
            The DataFrame for which missing values are to be visualized.
    """

    # Streamlit layout with two columns, chart will be in the left column
    fig_col_missing_values, _ = st.columns(2)
    with fig_col_missing_values:
        # Calculate missing values
        missing_values = df.isnull().sum()

        # Create a DataFrame for missing values
        missing_df = pd.DataFrame({
            "Column names": missing_values.index,
            "Missing Values": missing_values.values
        })

        # Create a bar chart with Plotly Express
        fig = px.bar(
            missing_df,
            x="Column names",
            y="Missing Values",
            title="💡 Number of Missing Values per Column"
        )

        # Set the layout to have a transparent background
        fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)"
        })

        # Display the chart in Streamlit
        st.write(fig)

def visualize_data_by_date_range(df_read, date_of_interest):
    """
    Visualizes data in the DataFrame for a specified date range.

    This function filters the DataFrame for the provided date range and creates a line plot for 
    each column in the filtered DataFrame using Plotly. The visualization is displayed in the 
    Streamlit app.

    Args:
        df_read: pandas DataFrame
            The DataFrame containing the data to be visualized.
        date_of_interest: list of datetime.date
            A list containing the start and end dates for filtering the DataFrame.

    Displays:
        Line plots for each column in the DataFrame over the specified date range.
    """

    # Filter the DataFrame for the selected date range
    df_day_of_interest = df_read.loc[
        date_of_interest[0].strftime("%Y-%m-%d") : date_of_interest[1].strftime("%Y-%m-%d")
    ]

    # Display the filtered DataFrame
    st.dataframe(df_day_of_interest)

    # Create a line plot for each column in the DataFrame
    fig2 = go.Figure()
    for column in df_day_of_interest.columns:
        fig2.add_trace(
            go.Scatter(
                x=df_day_of_interest.index, y=df_day_of_interest[column], name=column
            )
        )

    # Display the figure in Streamlit
    st.plotly_chart(fig2,use_container_width=True)
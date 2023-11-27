# visualization.py

import pandas as pd
import plotly.express as px
import streamlit as st

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

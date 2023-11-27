# visualization.py

import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import plotly.graph_objects as go
import random


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

def visualise_time_series_data(df_read):
    """
    Visualizes time series data in the DataFrame by creating line plots for daily mean values,
    bar charts for monthly peak values, and bar charts for monthly changes.

    This function iterates over each column in the DataFrame and creates three different types
    of plots using Plotly: a line plot for daily averages, a bar chart for monthly peaks, and
    a bar chart for monthly changes. Each plot uses randomly generated colors for the traces.

    Args:
        df_read: pandas DataFrame
            The DataFrame containing time series data.

    Displays:
        Three figures - one for daily means, one for monthly peaks, and one for monthly changes.
    """

    fig3 = go.Figure()
    fig4 = go.Figure()
    fig5 = go.Figure()

    for column in df_read.columns:
        # Generate a random color
        random_color = 'rgb(%d, %d, %d)' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Resample and calculate mean for each day
        daily_mean = df_read[column].resample('D').mean()

        # Resample for monthly peak and mean
        monthly_peak = df_read[column].resample('M').max()
        monthly_mean = df_read[column].resample('M').sum()
        monthly_change = monthly_mean.diff()

        # Add traces for daily mean, monthly peak, and monthly change
        fig3.add_trace(go.Scatter(x=daily_mean.index, y=daily_mean, name=column, line=dict(color=random_color)))
        fig4.add_trace(go.Bar(x=monthly_peak.index.strftime('%B'), y=monthly_peak, name=column, marker_color=random_color))
        fig5.add_trace(go.Bar(x=monthly_change.index, y=monthly_change, name=f'Monthly Change - {column}', marker_color=random_color))

    # Update layout for each figure
    fig3.update_layout(title={'text': "Daily Load Comparison by Column", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    fig4.update_layout(title='Monthly Peak Values per Column', xaxis_title='Month', yaxis_title='Peak Value', barmode='group')
    fig5.update_layout(title='Monthly Load Change per Column', xaxis_title='Date', yaxis_title='Change in Aggregate Load', barmode='group')

    # Display the figures in Streamlit
    st.plotly_chart(fig3,use_container_width=True)
    st.plotly_chart(fig4,use_container_width=True)
    st.plotly_chart(fig5,use_container_width=True)    
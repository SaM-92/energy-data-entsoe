
import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random
from subs.modules import *


st.markdown("### 📈 Trend Analysis")

if uploaded_file is not None:




    # Assuming df_read has datetime index now after conversion
    for column in df_read.columns:
        # Generate a random color
        random_color = 'rgb(%d, %d, %d)' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Loop over each column in your DataFrame
    fig3 = go.Figure()
    fig4 = go.Figure()
    fig5 = go.Figure()
    for column in df_read.columns:
        # Resample and calculate mean for each day
        daily_mean = df_read[column].resample('D').mean()
        
        monthly_peak = df_read[column].resample('M').max()
        monthly_mean=df_read[column].resample('M').sum()
        monthly_change = monthly_mean.diff()
        

        random_color = 'rgb(%d, %d, %d)' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        fig3.add_trace(
            go.Scatter(
                x=daily_mean.index, y=daily_mean, name=column , line=dict(color=random_color)  # Use the random color
            )
        )
        # Add a bar trace for each column
        fig4.add_trace(
            go.Bar(
                x=monthly_peak.index.strftime('%B'),  # Format the month for the x-axis
                y=monthly_peak,
                name=column,
                marker_color=random_color  # Use the random color for each bar
            )
        )

                # Add a trace for the daily change
        fig5.add_trace(
            go.Bar(
                x=monthly_change.index, 
                y=monthly_change, 
                name=f'Monthly Change - {column}', 
                marker_color=random_color
            )
        )





    fig3.update_layout(
        title={
            'text': "Daily Load Comparison by Column",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )   
    # Update layout for the bar chart
    fig4.update_layout(
        title='Monthly Peak Values per Column',
        xaxis_title='Month',
        yaxis_title='Peak Value',
        barmode='group'
    )
        # Update layout for the bar chart
    fig5.update_layout(
        title='Monthly Load Change per Column',
        xaxis_title='Date',
        yaxis_title='Change in Aggregate Load',
        barmode='group'
    )
    # st.write(fig4)

    # Display the figure in Streamlit
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig5, use_container_width=True)

    # Loop through each column in the DataFrame
    for column in df_read.columns:
        # Get descriptive statistics for the current column
        stats = df_read[column].describe()

        # Construct the summary text with markdown for better formatting
        summary_text = f"""
        ### Statistics for {column}
        **Count**: {stats['count']} data points.\n
        **Mean**: The average is {stats['mean']:.2f}.\n
        **Standard Deviation**: The standard deviation is {stats['std']:.2f}, which indicates variability.\n
        **Minimum**: The smallest observed value is {stats['min']:.2f}.\n
        **25th Percentile**: 25% of the values are {stats['25%']:.2f} or less.\n
        **50th Percentile (Median)**: The median value is {stats['50%']:.2f}.\n
        **75th Percentile**: 75% of the values are {stats['75%']:.2f} or less.\n
        **Maximum**: The largest observed value is {stats['max']:.2f}.
        """

        # Use Streamlit's 'st.markdown()' function to display the summary for the current column
        st.markdown(summary_text)


import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random
from subs.data_loader import load_data, process_data_for_analysis , process_uploaded_file, convert_time , process_time_resolution_and_duplicates
from subs.visualisation import visualize_missing_values

# st.set_page_config(page_title="Data Master Mind", page_icon="🚀", layout="wide")
# st.set_page_config(page_title="Data Master Mind", page_icon="👋🏽", layout="wide")

st.set_page_config(
    page_title="Empowering Insights",
    page_icon="🏭",
)
st.image("./header.png")

st.title("Empowering Insights: Navigating ENTSO-E Power System Data")
st.markdown("Created by Saeed Misaghian")
st.markdown("📧 Contact me: [sam.misaqian@gmail.com](mailto:sam.misaqian@gmail.com)")
st.markdown("🔗 [GitHub](https://github.com/SaM-92)")
st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/)")

def page0():
    st.markdown("""

    ---

    ### About ENTSO-E
    The European Network of Transmission System Operators for Electricity (ENTSO-E) coordinates the cross-border system operations, market developments, and data exchange among Europe's transmission system operators (TSOs). ENTSO-E focuses on ensuring the seamless operation and development of the European electricity market and the electric grid.
   
    📊 [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)
                
    ### Current Service
    This interactive tool is designed to streamline your analysis of ENTSO-E power system data. Here's what you can do:

    #### 1. Data Manipulation
    - **Upload and Clean:** Easily upload your ENTSO-E data and handle missing values.
    - **Visualization:** Instantly visualize your time series data.
    - **Resolution Adjustment:** Modify the data resolution to your preference, such as 5-minute intervals or hourly aggregates.
    - **Download:** After manipulation, download your data for further use.

    #### 2. Trend Analysis
    Get in-depth insights into your data with features such as:
    - **Daily Trends:** Examine the daily patterns within your data.
    - **Load Comparisons:** View side-by-side comparisons of forecasted and actual data loads.
    - **Monthly Peaks and Changes:** Identify peak values and month-over-month changes in the data.
    - **Statistical Summaries:** Access key statistics including mean, min, max, and percentile quantiles.

    This is a demo project, intended to showcase the potential of ENTSO-E data analysis.

    """            
    # ### Getting Started with ENTSO-E Data
    # If you're new to ENTSO-E data, I've created a tutorial to help you get started:

    # 🎥 [Learn how to get ENTSO-E data](https://www.youtube.com/yourvideolink)

    # ### How to Use This Tool
    # Below you can find a demo that guides you through the functionalities of this tool. Begin by uploading your data, then navigate through the features using the sidebar. Enjoy exploring your data and uncovering valuable insights!

    )
    
# Define your pages
def page1():
    st.markdown("# Data Manipulation")

    st.write(
        """This section helps you to """
    )


    st.markdown("### 🔗 Upload your data")

    # Create a file uploader
    uploaded_file = st.file_uploader("Upload your CSV file")


    # Check if a file has been uploaded
    if uploaded_file:
        df_read = load_data(uploaded_file)
        st.dataframe(df_read)

        # Show the clients the list of their DataFrame columns and ask them to 
        # choose the column with date and time observations
        time_column = st.selectbox(
            "Please select the column with date and time observations:", df_read.columns
        )

        # process data for further analysis 
        df_read , skip_invalid_row , first_invalid_row_time= process_data_for_analysis(df_read,time_column)

        # Visualise missing data
        visualize_missing_values(df_read)


    st.markdown("### ⚙️ Dealing with Missing Values")
    st.markdown("📝 Please choose how you want to deal with missing values?")
    options_to_drop = ["Remove", "Interpolate", "Backward/Forward Filling"]
    # users can define the method by which they prefer to deal with missing values
    selected_option_missing_values = st.selectbox("Select the Job", options_to_drop)

    if uploaded_file is not None:
        df_read = process_uploaded_file (df_read,selected_option_missing_values)
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

        # Apply the function to your DataFrame
        df_read = convert_time(df_read, time_column)

        df_read = process_time_resolution_and_duplicates(df_read, time_column, time_resolution_number, time_resolution_unit, skip_invalid_row, first_invalid_row_time)

        st.dataframe(df_read)
        st.session_state['df_read'] = df_read  # Save processed DataFrame to session state for other pages


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

def page2():
    st.markdown("### 📈 Trend Analysis")

    # if uploaded_file is not None:

       # Check if data has been uploaded and processed
    if 'df_read' in st.session_state:
        df_read = st.session_state['df_read']    


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
    else:
        st.error("Please upload data on the Data Manipulation page first.")        


# Sidebar navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio("Select a page:", ('Service Overview','Data Manipulation', 'Trend Analysis'))

if page == 'Data Manipulation':
    page1()
elif page == 'Trend Analysis':
    page2()
elif page == 'Service Overview':
    page0()    
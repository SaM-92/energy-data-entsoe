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

# dashboard title

st.title("ENTSO-E Data Manipulation Dashboard")
st.markdown("### 🚀 Data Master Mind")

st.image("./logo.png", width=300)  # adjust width as needed


st.markdown("### 🔗 Upload your data")

# Create a file uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file
    df_read = pd.read_csv(uploaded_file)
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

st.markdown("### ✔️ Calibration KPIs")

if uploaded_file is not None:
    # Calculate metrics
    rmse = sqrt(mean_squared_error(df_read["simulated"], df_read["metered"]))
    cvrmse = rmse / np.mean(df_read["simulated"]) * 100
    nmbe = (
        np.mean(df_read["simulated"] - df_read["metered"])
        / np.mean(df_read["simulated"])
        * 100
    )
    mae = mean_absolute_error(df_read["simulated"], df_read["metered"])
    rn_rmse = rmse / (np.max(df_read["simulated"]) - np.min(df_read["simulated"]))

    fig_measure_simulated = px.line(
        df_read,
        x="date_time",
        y=["simulated", "metered"],
        color_discrete_sequence=["blue", "red"],
        title="Simulated vs Metered",
    )
    fig_measure_simulated.update_layout(xaxis_title="Date Time", yaxis_title="kWh")
    st.plotly_chart(fig_measure_simulated)

    # Create a DataFrame for the metrics
    metrics_df = pd.DataFrame(
        {
            "Metrics": ["RMSE", "CVRMSE", "NMBE", "MAE", "RN_RMSE"],
            "Values": [rmse, cvrmse, nmbe, mae, rn_rmse],
        }
    )

    # Plot a bar chart of metrics
    fig_metrics = px.bar(metrics_df, x="Metrics", y="Values", title="Metrics Bar Chart")
    fig_metrics.update_layout(xaxis_title="Metrics", yaxis_title="Value")
    st.plotly_chart(fig_metrics)

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(label="RMSE ⏳", value=round(rmse, 2), delta=round(rmse, 2))
    kpi2.metric(label="CVRMSE 📈 ", value=round(cvrmse, 2), delta=round(rmse, 2))
    kpi3.metric(label="NMBE ⏳", value=round(nmbe, 2), delta=round(nmbe, 2))
    kpi4.metric(label="MAE 📈", value=round(mae, 2), delta=round(mae, 2))
    kpi5.metric(label="RN_RMSE ⏳", value=round(rn_rmse, 2), delta=round(rn_rmse, 2))

    # Display the DataFrame as a table in Streamlit
    st.table(metrics_df)


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

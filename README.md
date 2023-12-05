# ENTSO-E Data Analysis Tool

![header](./images/header.png)

## Description

The ENTSO-E Data Analysis Tool is an interactive web application designed to streamline the analysis of the [European Network of Transmission System Operators for Electricity (ENTSO-E)] (https://transparency.entsoe.eu/) power system data. This tool is crafted to facilitate a seamless operation in handling, visualising, and analysing electricity market and grid data across Europe.

![Demo](./images/demo.gif)


## Features

- **Data Upload and Cleaning:** Easily upload ENTSO-E data and handle missing values.
- **Data Visualisation:** Visualise time series data with options to analyse daily means, monthly peaks, and changes.
- **Trend Analysis:** Perform basic analysis with features like load comparisons and statistical summaries.
- **Data Preparation:** Prepare your data by setting time columns, handling invalid rows, and managing duplicates.
- **Interactive UI:** User-friendly interface with functionalities accessible through a sidebar.

## Getting Started

### Prerequisites

- Python 3.10
- Streamlit 1.28
- Pandas 2.1.2
- Plotly 5.18.0

### Installation

Clone the repository and install the required packages:

```
git clone https://github.com/SaM-92/energy-data-entsoe.git

pip install -r requirements.txt
```

### Running the Application

To start the application, run:

```
streamlit run app.py
```

Navigate to the displayed URL in your web browser to interact with the application.

## Modules

- `app.py`: The main application script.
- `data_loader.py`: Module for loading and initial processing of data.
- `visualisation.py`: Creating and configuring data visualizations.

## Usage

1. **Upload Data:** Start by uploading your ENTSO-E data file. 
2. **Data Manipulation:** Clean and prepare your data for analysis.
3. **Visualize Data:** Explore various visualization options for your data.
4. **Analyze Trends:** Utilize the tools provided for trend analysis and statistical insights.

## Contact

For any queries or suggestions, please reach out to [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/) or [sam.misaqian@gmail.com](mailto:sam.misaqian@gmail.com).

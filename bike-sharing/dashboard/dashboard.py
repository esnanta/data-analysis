# layout credit to :
# https://github.com/64SquaresApexLLP/Snowflake_health/tree/Devesh

import io
import os
import streamlit as st
import requests
import zipfile
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

global df_hour_data

# Configuration
GITHUB_URL = 'https://github.com/esnanta/data-analysis/raw/main/Dataset/Bike-sharing-dataset.zip'
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
ZIP_PATH = os.path.join(DATA_FOLDER, 'Bike-sharing-dataset.zip')
DAY_CSV_PATH = os.path.join(DATA_FOLDER, 'day.csv')
HOUR_CSV_PATH = os.path.join(DATA_FOLDER, 'hour.csv')

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

@st.cache_data(show_spinner=False)
def download_and_extract_data(url, zip_path, extract_to):
    """Download and extract dataset."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(zip_path, 'wb') as file:
                file.write(response.content)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True, "Dataset downloaded and extracted successfully!"
        else:
            return False, "Failed to download the dataset. Check the URL."
    except Exception as e:
        return False, f"An error occurred during download: {e}"

@st.cache_data(show_spinner=False)
def load_data(csv_path):
    """Load data from a CSV file."""
    try:
        return pd.read_csv(csv_path), None
    except Exception as e:
        return None, f"An error occurred while loading data: {e}"

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=[
            "Introduction",
            "Questions",
            "Import Libraries",
            "Data Wrangling",
            "Exploratory Data Analysis",
            "Visualization and Explanatory Analysis",
            "Further Analysis",
            "Conclusion",
        ],
        icons=[
            "info-circle",
            "question-circle",
            "code-slash",
            "file-earmark-binary",
            "bar-chart",
            "graph-up-arrow",
            "search",
            "check-circle",
        ],
        menu_icon="cast",
        default_index=0,
    )

# Introduction Section
if selected == "Introduction":
    st.header("Analisis Data Bike Sharing")
    st.write("**Nama:** NANTHA SEUTIA")
    st.write("**Email:** ombakrinai@gmail.com")
    st.write("**ID Dicoding:** ombakrinai@gmail.com")

    st.subheader("Karakteristik Dataset")
    st.write("""
    Both hour.csv and day.csv have the following fields, except hr which is not available in day.csv:

    - **instant**: record index
    - **dteday**: date
    - **season**: season (1:spring, 2:summer, 3:fall, 4:winter)
    - **yr**: year (0:2011, 1:2012)
    - **mnth**: month (1 to 12)
    - **hr**: hour (0 to 23)
    - **holiday**: whether the day is a holiday or not (extracted from holiday schedules)
    - **weekday**: day of the week
    - **workingday**: 1 if the day is neither a weekend nor holiday, otherwise 0
    - **weathersit**:
        - 1: Clear, Few clouds, Partly cloudy
        - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
        - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds
        - 4: Heavy Rain + Ice Pellets + Thunderstorm + Mist, Snow + Fog
    - **temp**: Normalized temperature in Celsius (divided by 41 max)
    - **atemp**: Normalized feeling temperature in Celsius (divided by 50 max)
    - **hum**: Normalized humidity (divided by 100 max)
    - **windspeed**: Normalized wind speed (divided by 67 max)
    - **casual**: count of casual users
    - **registered**: count of registered users
    - **cnt**: total rental bikes including casual and registered users
    """)

    st.subheader("Catatan Tambahan")
    st.write("""
    - **temp** adalah normalisasi temperatur dalam skala 0-1. Contoh: nilai 0,5 berarti suhu berada di tengah antara suhu minimum dan maksimum.
    - **atemp** adalah temperatur yang dirasakan manusia, dipengaruhi oleh kelembapan dan angin, juga dinormalisasi dalam skala 0-1.
    - **casual** untuk pelanggan umum.
    - **registered** untuk pelanggan terdaftar.
    - **cnt** adalah total penyewaan.
    """)

    st.subheader("Insight")
    st.write("""
    Karena informasi pada kedua file relatif sama dan hanya dibedakan oleh variabel 'hr' pada 'hour.csv', 
    data 'hour.csv' dipilih untuk analisis karena memiliki data yang lebih banyak.
    """)

# Questions Section
if selected == "Questions":
    st.header("Menentukan Pertanyaan Bisnis")
    st.write(
        """
        - Apakah faktor lingkungan memengaruhi jumlah penyewaan sepeda?
        - Apa tren penggunaan sepeda sepanjang waktu?
        - Bagaimana performa sistem penyewaan di berbagai musim?
        """
    )

# Import Libraries Section
if selected == "Import Libraries":
    st.header("Import Necessary Libraries")
    st.code(
        """
import pandas as pd
import zipfile
import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
        """
    )

# Data Wrangling Section
if selected == "Data Wrangling":
    wrangling_option = option_menu(
        menu_title="Data Wrangling",
        options=["Gathering Data", "Assessing Data", "Cleaning Data"],
        icons=["download", "search", "broom"],
        menu_icon="gear",
        default_index=0,
        orientation="horizontal"
    )

    if wrangling_option == "Gathering Data":
        st.subheader("Gathering Data")
        # Reset Cache button
        if st.button("Reset Cache"):
            st.cache_data.clear()
            st.success("Cache has been reset!")

        success, message = download_and_extract_data(GITHUB_URL, ZIP_PATH, DATA_FOLDER)
        if success:
            st.success(message)
            df_hour_data, load_error = load_data(HOUR_CSV_PATH)
            if load_error:
                st.error(load_error)
            else:
                st.write("Preview of Hour Data:")
                st.dataframe(df_hour_data.head())
        else:
            st.error(message)

        st.markdown("""
        ### **Insight:**

        - **Continuous Data**: `temp`, `atemp`, `hum`, `windspeed`
        - **Discrete Data**: `instant`, `casual`, `registered`, `cnt`
        - **Ordinal Data**: `season`, `weathersit`, `weekday`
        - **Nominal Data**: `dteday`, `yr`, `mnth`, `hr`, `holiday`, `workingday`
        """)

    if wrangling_option == "Assessing Data":
        st.subheader("Assessing Data")
        df_hour_data, load_error = load_data(HOUR_CSV_PATH)
        if load_error:
            st.error(load_error)
        else:
            st.write("### Dataset Information")

            # Extract DataFrame info into a structured format
            data_info = {
                "Column": df_hour_data.columns,
                "Non-Null Count": [df_hour_data[col].notnull().sum() for col in df_hour_data.columns],
                "Dtype": [df_hour_data[col].dtype for col in df_hour_data.columns],
            }
            info_df = pd.DataFrame(data_info)

            # Display the table
            st.table(info_df)  # st.table for static table or st.dataframe for interactive table

            st.write("### Checks whether ordinal and nominal data have values that match the instructions")
            st.code("""
            # Note : range() function includes the start value but excludes the end value
            valid_ranges = {
                'season': range(1, 5),         # Seasons: 1 to 4
                'weathersit': range(1, 5),     # Weather situations: 1 to 4
                'weekday': range(0, 7),        # Weekday: 0 (Sunday) to 6 (Saturday)
                'yr': [0, 1],                  # Year: 0 (2011), 1 (2012)
                'mnth': range(1, 13),          # Months: 1 to 12
                'hr': range(0, 24),            # Hour: 0 to 23
                'holiday': [0, 1],             # Holiday: 0 (No), 1 (Yes)
                'workingday': [0, 1],          # Working day: 0 (No), 1 (Yes)
            }
            """, language="python")

            valid_ranges = {
                'season': range(1, 5),  # Seasons: 1 to 4
                'weathersit': range(1, 5),  # Weather situations: 1 to 4
                'weekday': range(0, 7),  # Weekday: 0 (Sunday) to 6 (Saturday)
                'yr': [0, 1],  # Year: 0 (2011), 1 (2012)
                'mnth': range(1, 13),  # Months: 1 to 12
                'hr': range(0, 24),  # Hour: 0 to 23
                'holiday': [0, 1],  # Holiday: 0 (No), 1 (Yes)
                'workingday': [0, 1],  # Working day: 0 (No), 1 (Yes)
            }

            invalid_values_report = {}
            for column, valid_range in valid_ranges.items():
                if column in df_hour_data.columns:
                    invalid_rows = df_hour_data[~df_hour_data[column].isin(valid_range)]
                    if not invalid_rows.empty:
                        invalid_values_report[column] = invalid_rows

            if invalid_values_report:
                st.warning("The following columns have invalid data:")
                for column, invalid_rows in invalid_values_report.items():
                    st.write(f"**Column '{column}':** Invalid rows found.")
                    st.dataframe(invalid_rows)
            else:
                st.success("All ordinal and nominal variables have valid data.")

            st.write("### Checking Negative Values for 'casual' and 'registered'")
            invalid_casual_registered = df_hour_data[
                (df_hour_data['casual'] < 0) | (df_hour_data['registered'] < 0)
                ]

            if not invalid_casual_registered.empty:
                st.warning("Negative values found in 'casual' or 'registered' columns:")
                st.dataframe(invalid_casual_registered)
            else:
                st.success("No negative values found in 'casual' or 'registered' columns.")

            st.write("### Checking 'cnt' Consistency with 'casual' and 'registered'")
            discrepancy = df_hour_data[df_hour_data['cnt'] != (df_hour_data['casual'] + df_hour_data['registered'])]

            if not discrepancy.empty:
                st.warning(f"Discrepancies found in {len(discrepancy)} rows:")
                st.dataframe(discrepancy)
            else:
                st.success("No discrepancies: 'cnt' equals (casual + registered) for all rows.")

            st.markdown("""
            ### **Insight**
            - ✅ **Tidak ada data yang bernilai null.**
            - ⚠️ **Kesalahan tipe data:** Kolom `'dteday'` seharusnya memiliki tipe data `'date'`.
            - ✅ **Data ordinal dan nominal sesuai ketentuan.**  
            - ✅ **Tidak ada nilai negatif untuk kolom:** `casual`, `registered`, dan `cnt`.  
            - ✅ **Nilai `cnt` sudah sesuai dengan penjumlahan:** `casual + registered`.  
            """)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.write("### Summary Statistics")
            st.code("""
                summary = df_hour_data.describe()
                print(summary)
            """, language="python")

            # Get the summary statistics of the DataFrame
            summary = df_hour_data.describe()

            # Display the summary in Streamlit
            # Use st.write() for general display or st.dataframe() for a more interactive table
            st.dataframe(summary)

            st.markdown("""
            ### **Insight:**

            - **Setiap kolom** memiliki data sebanyak `17,379` entri, yang artinya **tidak ada missing value**.
            - **Season**, `yr`, `mnth`, `hr` terlihat konsisten berdasarkan jumlah data. Perlu analisis distribusi dengan plot frekuensi untuk pemahaman lebih mendalam.
            - **Holiday** (biner `[0, 1]`):
              - **Mean**: `0.02`, menunjukkan jumlah data **hari libur** yang sedikit.
              - Hari libur bernilai `1` (**true**).
            - **Weekday** (Sunday-Saturday, `0-6`):
              - **Mean**: `3`.
              - Perlu analisis distribusi dengan plot frekuensi untuk pemahaman lebih mendalam.
            - **Workingday** (biner `[0, 1]`):
              - **Mean**: `0.6`, menunjukkan lebih banyak **hari kerja**.
              - Nilai `1` (**true**) untuk hari kerja.
            - **Weathersit**:
              - Menjelaskan **kondisi cuaca** dengan rentang `1-4`.
              - **Mean**: `1.4`, menunjukkan kondisi cuaca lebih banyak **cerah** atau **berawan**.
            - **Temp** dan **atemp**:
              - **Mean**: `0.4`, menunjukkan kondisi cuaca di tengah-tengah antara batas minimal (`0`) dan maksimal (`1`).
            - **Humidity**:
              - **Mean**: `0.6`, menunjukkan kelembaban cenderung sedang.
              - **Min**: `0`, berarti kelembaban **kering**; **Max**: `1`, berarti **saturasi penuh**.
            - **Windspeed**:
              - **Min**: `0`, **Max**: `0.8`, dan **Mean**: `0.2`, menunjukkan kondisi kecepatan angin **rendah**.
            - **Pelanggan umum (casual)**:
              - Distribusi **right skewed** (skewed ke kanan):
                - **Persentil Q1**: `4`, jauh lebih kecil dari **Q3**: `48`.
                - **Standar Deviasi**: `49`, lebih besar dari **Mean**: `35`, menunjukkan data tersebar luas.
            - **Pelanggan terdaftar (registered)**:
              - Distribusi **right skewed**:
                - **Persentil Q1**: `34`, jauh lebih kecil dari **Q3**: `220`.
                - **Standar Deviasi**: `151`, mendekati **Mean**: `153`, menunjukkan variasi data dekat dengan **mean**.
            - **Total sewa (cnt)**:
              - **Standar Deviasi**: `181`, lebih kecil dan tidak terlalu jauh dari **Mean**: `189`.
              - **Min**: `1` dan **Max**: `977`, menunjukkan rentang yang jauh, kemungkinan terdapat **outlier**.
              - **Persentil Q1**: `40`, jauh lebih kecil dari **Q3**: `281`, menunjukkan data cenderung **right skewed**.
              - Data **total sewa (cnt)** dipengaruhi oleh pelanggan **umum (casual)** dan **terdaftar (registered)**.
            """)

    if wrangling_option == "Cleaning Data":
        # Step 1: Display Cleaning Task
        df_hour_data, load_error = load_data(HOUR_CSV_PATH)
        if load_error:
            st.error(load_error)
        else:
            # Display an introductory message
            st.markdown("### Step 1: Define")
            st.markdown("""
            The goal of this step is to prepare the dataset for further analysis by addressing data type issues.

            #### Task:
            - The column **'dteday'** is currently of type `object`. 
            - It needs to be converted to `datetime` to allow proper handling and analysis of date-related information.

            This conversion will ensure that the dates are correctly interpreted, enabling time-based operations and visualizations.

            """)
            # Capture and display the updated DataFrame information
            buffer = io.StringIO()  # Capture df.info() output
            df_hour_data.info(buf=buffer)
            info_output = buffer.getvalue()
            st.text(info_output)
            # Step 2: Perform the Cleaning Task
            st.markdown("### Step 2: Code")
            st.write("Converting the 'dteday' column from `object` to `datetime`")

            # Clean the data by converting 'dteday' column
            df_hour_data['dteday'] = pd.to_datetime(df_hour_data['dteday'])

            # Display the code for transparency
            st.code("df_hour_data['dteday'] = pd.to_datetime(df_hour_data['dteday'])", language="python")

            # Step 3: Verify the Change
            st.markdown("### Step 3: Verify")
            st.write("Now, let's verify that the change has been successfully applied.")
            st.code("df_hour_data.info()", language="python")

            # Capture and display the updated DataFrame information
            buffer = io.StringIO()  # Capture df.info() output
            df_hour_data.info(buf=buffer)
            info_output = buffer.getvalue()
            st.text(info_output)

            # Success message
            st.success(
                "Data cleaning completed successfully. The 'dteday' column has been successfully converted to `datetime`.")

# Exploratory Data Analysis Section
if selected == "Exploratory Data Analysis":
    st.header("Exploratory Data Analysis")
    data = pd.DataFrame(np.random.randn(20, 3), columns=["Feature A", "Feature B", "Feature C"])
    st.write(data.describe())
    st.line_chart(data)

# Visualization and Explanatory Analysis Section
if selected == "Visualization and Explanatory Analysis":
    sub_menu = st.sidebar.radio("Choose a Question", ["Question 1", "Question 2", "Question 3"])

    if sub_menu == "Question 1":
        st.header("Visualization for Question 1")
        st.write("Visualisasi untuk pertanyaan pertama.")
        # Placeholder visualization logic

    if sub_menu == "Question 2":
        st.header("Visualization for Question 2")
        st.write("Visualisasi untuk pertanyaan kedua.")
        # Placeholder visualization logic

    if sub_menu == "Question 3":
        st.header("Visualization for Question 3")
        st.write("Visualisasi untuk pertanyaan ketiga.")
        # Placeholder visualization logic

# Further Analysis Section
if selected == "Further Analysis":
    st.header("Analisis Lanjutan")
    st.write("Detail tentang analisis lanjutan yang dilakukan.")

# Conclusion Section
if selected == "Conclusion":
    st.header("Kesimpulan")
    st.write("Kesimpulan dari analisis data.")

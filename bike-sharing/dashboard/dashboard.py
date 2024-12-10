# layout credit to :
# https://github.com/64SquaresApexLLP/Snowflake_health/tree/Devesh

import io
import os
import streamlit as st
import requests
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from streamlit_option_menu import option_menu

# Configuration
GITHUB_URL = 'https://github.com/esnanta/data-analysis/raw/main/Dataset/Bike-sharing-dataset.zip'
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
ZIP_PATH = os.path.join(DATA_FOLDER, 'Bike-sharing-dataset.zip')
HOUR_CSV_PATH = os.path.join(DATA_FOLDER, 'hour.csv')

# Ensure the data folder exists
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

# Reset cache functionality
def reset_cache():
    """Clear all cached data."""
    st.cache_data.clear()
    st.success("Cache has been cleared!")

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Introduction", "Analysis", "Conclusion"],
        icons=["info-circle", "chart-bar", "check-circle"],
        menu_icon="cast",
        default_index=0,
    )
    # Reset cache button
    if st.button("Reset Data Cache"):
        reset_cache()

# Introduction Section
if selected == "Introduction":
    st.title("🚴 Analisis Data Bike Sharing")
    st.write("### 💡 **Informasi Pengguna**")
    st.write("- **Nama:** NANTHA SEUTIA")
    st.write("- **Email:** [ombakrinai@gmail.com](mailto:ombakrinai@gmail.com)")
    st.write(
        "- **Data Source:** [Dataset Link](https://github.com/esnanta/data-analysis/raw/main/Dataset/Bike-sharing-dataset.zip)"
    )
    st.write("### 🌍 **Background**")
    st.markdown(
        """
        **Bike sharing systems** are a new generation of traditional bike rentals where the entire process—from membership, rental, 
        and return—has become automatic. These systems allow users to easily rent a bike from one location and return it at another.

        🚴 **Global Popularity**:
        - Over 500 bike-sharing programs worldwide, comprising more than 500,000 bicycles.
        - These systems play a crucial role in addressing **traffic**, **environmental**, and **health** issues.

        🧪 **Research Potential**:
        - Unlike other transportation services like buses or subways, bike-sharing systems explicitly record **trip durations**, 
          **departure points**, and **arrival points**.
        - This turns them into a **virtual sensor network**, offering valuable insights into urban mobility patterns.
        - Monitoring this data can potentially help detect significant events within a city.
        """
    )

    st.subheader("Analisis Akan Menjawab Pertanyaan Berikut:")
    st.markdown(
        """
        - Apakah faktor lingkungan memengaruhi jumlah penyewaan sepeda?
        - Apa tren penggunaan sepeda sepanjang waktu?
        - Bagaimana performa sistem penyewaan di berbagai musim?
        """
    )

# Analysis Section
if selected == "Analysis":
    analysis_option = option_menu(
        menu_title="📊 Analisis Data Bike Sharing",
        options=["Q1", "Q2", "Q3"],
        icons=["download", "search", "broom"],
        menu_icon="gear",
        default_index=0,
        orientation="horizontal"
    )

    # Analysis based on selected option
    df, error = load_data(HOUR_CSV_PATH)
    if error:
        st.error(error)
    elif df is not None:
        if df is not None:
            # Question 1: Analysis
            if analysis_option == "Q1":
                st.subheader(
                    "1️⃣ Perbedaan Pola Peminjaman Sepeda Antara Pengguna Umum (Casual) dan Terdaftar (Registered)")

                # Daily Bike Rentals: Casual vs Registered
                daily_data = df.groupby('dteday')[['casual', 'registered']].sum().reset_index()
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=daily_data, x='dteday', y='casual', label='Casual', color='blue', ax=ax)
                sns.lineplot(data=daily_data, x='dteday', y='registered', label='Registered', color='orange', ax=ax)
                ax.set_title('Daily Bike Rentals: Casual vs Registered')
                ax.set_xlabel('Date')
                ax.set_ylabel('Number of Rentals')
                ax.legend()
                st.pyplot(fig)

                st.markdown("""
                **Insight:**
                - Pengguna terdaftar (registered) memiliki grafik yang konsisten lebih tinggi dibandingkan pengguna umum (casual) sepanjang tahun.
                - Pengguna terdaftar kemungkinan besar menggunakan layanan ini secara rutin, misalnya untuk bekerja atau sekolah.
                - Lonjakan aktivitas terlihat selama bulan-bulan musim panas (Mei hingga September), sementara aktivitas menurun pada musim dingin (Desember hingga Februari).
                - Aktivitas pengguna terdaftar mencapai puncaknya sekitar pertengahan musim panas dengan beberapa hari mendekati atau melebihi 7000 penyewaan.
                """)

                # Average Rentals: Working Day vs Weekend
                workingday_data = df.groupby('workingday')[['casual', 'registered']].mean().reset_index()
                workingday_data['day_type'] = workingday_data['workingday'].map({0: 'Weekend/Holiday', 1: 'Working Day'})

                st.write("### Average Rentals: Working Day vs Weekend")
                x = np.arange(len(workingday_data))  # Positions for bars
                width = 0.35  # Width of the bars

                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(x - width / 2, workingday_data['casual'], width, color='blue', label='Casual')
                ax.bar(x + width / 2, workingday_data['registered'], width, color='orange', label='Registered')
                ax.set_title('Average Rentals: Working Day vs Weekend')
                ax.set_ylabel('Number of Rentals')
                ax.set_xlabel('Day Type')
                ax.set_xticks(x)
                ax.set_xticklabels(workingday_data['day_type'])
                ax.legend()
                st.pyplot(fig)

                st.markdown("""
                **Insight:**
                - Pengguna casual memiliki tingkat penyewaan lebih tinggi selama akhir pekan atau hari libur, menunjukkan penggunaan untuk rekreasi.
                - Pengguna terdaftar (registered) cenderung memanfaatkan layanan lebih banyak pada hari kerja, mengindikasikan penggunaan untuk tujuan rutin.
                - Selama hari kerja, penyewaan oleh pengguna terdaftar sangat mendominasi dibandingkan pengguna casual.
                """)


            elif analysis_option == "Q2":
                st.subheader("2️⃣ Apa Tren Penggunaan Sepeda Sepanjang Waktu?")
                st.write("Analysis and visualization for Question 2 will be added here.")

            elif analysis_option == "Q3":
                st.subheader("3️⃣ Bagaimana Performa Sistem Penyewaan di Berbagai Musim?")
                st.write("Analysis and visualization for Question 3 will be added here.")
        else:
            st.error("Dataset could not be loaded. Please check the data source.")

# Conclusion Section
if selected == "Conclusion":
    st.header("Kesimpulan")
    st.write("Kesimpulan dari analisis data.")

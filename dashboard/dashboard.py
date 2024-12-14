# layout credit to :
# https://github.com/64SquaresApexLLP/Snowflake_health/tree/Devesh

import os
import streamlit as st
import requests
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
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
            st.toast("Dataset downloaded and extracted successfully!")
            return True, None
        else:
            return False, "Failed to download the dataset. Check the URL."
    except Exception as e:
        return False, f"An error occurred during download: {e}"

@st.cache_data(show_spinner=False)
def load_data(csv_path):
    """Load data from a CSV file, downloading and extracting if necessary."""
    # Check if the CSV file exists
    if not os.path.exists(csv_path):
        st.toast(f"{csv_path} not found. Downloading and extracting dataset...")
        success, message = download_and_extract_data(GITHUB_URL, ZIP_PATH, DATA_FOLDER)
        if not success:
            return None, message

    # Try to load the CSV file
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
        options=["Introduction", "Dataset", "Analysis", "Clustering", "Conclusion"],
        icons=["info-circle", "file-earmark-text", "bar-chart", "check-circle"],
        # Added missing icon for "Data Background" and "Analysis"
        menu_icon="cast",
        default_index=0,
    )
    # Reset cache button
    if st.button("Reset Data Cache"):
        reset_cache()

# Introduction Section
if selected == "Introduction":
    st.title("Analisis Data Bike Sharing 🚴")
    st.write("**Informasi Pengguna**")
    st.write("- **Nama:** NANTHA SEUTIA")
    st.write("- **Email:** [ombakrinai@gmail.com](mailto:ombakrinai@gmail.com)")

    st.subheader("Analisis Akan Menjawab Pertanyaan Berikut:")
    st.markdown(
        """
        - Bagaimana perbedaan pola peminjaman sepeda antara pengguna umum (casual) dibandingkan dengan pengguna terdaftar (registered)?
        - Pada jam-jam berapakah dalam sehari terdapat konsentrasi penyewaan sepeda tertinggi untuk pengguna umum dan pengguna terdaftar?
        - Bisakah kita mengenali anomali atau kejadian besar (seperti cuaca ekstrem atau hari libur nasional) berdasarkan lonjakan atau penurunan tiba-tiba dalam jumlah penyewaan sepeda (cnt)?
        """
    )

# Data Background Section
elif selected == "Dataset":
    st.subheader("Source")
    st.write(
        "Bike Sharing Dateset : [Link](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)"
    )
    st.subheader("About")

    st.markdown("""
    Bike sharing systems are a new generation of traditional bike rentals where the entire process, from membership to rental and return, has become automatic. Through these systems, users can easily rent a bike from a particular location and return it at another. Currently, there are over 500 bike-sharing programs around the world, comprising over 500,000 bicycles. These systems are of great interest due to their impact on traffic, environmental, and health issues.

    Apart from the practical applications of bike-sharing systems, the data they generate is also highly valuable for research. Unlike other transport services like buses or subways, bike-sharing systems explicitly record travel duration, departure, and arrival locations. This turns bike-sharing systems into virtual sensor networks capable of sensing mobility within cities. As a result, important events within a city, such as weather changes or holidays, could potentially be detected by monitoring this data.
    """)

    st.subheader("Data Set")
    st.markdown("""
    The bike-sharing rental process is highly correlated to environmental and seasonal factors. For example, weather conditions, precipitation, day of the week, season, and time of day can influence rental behaviors. The core dataset includes two years of historical data from the Capital Bikeshare system in Washington, D.C., USA, covering the years 2011 and 2012, which is publicly available at [Capital Bikeshare Data](http://capitalbikeshare.com/system-data).

    The data has been aggregated on an hourly and daily basis, with additional weather and seasonal information added. Weather information is sourced from [Free Meteo](http://www.freemeteo.com).
    """)

# Analysis Section
elif selected == "Analysis":
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
                st.subheader("1️⃣ Perbedaan Pola Peminjaman Sepeda")

                st.write("### Daily Bike Rentals: Casual vs Registered")
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

                st.write("### Average Rentals: Working Day vs Weekend")
                workingday_data = df.groupby('workingday')[['casual', 'registered']].mean().reset_index()
                workingday_data['day_type'] = workingday_data['workingday'].map({0: 'Weekend/Holiday', 1: 'Working Day'})

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


            if analysis_option == "Q2":
                st.subheader("2️⃣ Tren Penggunaan Sepeda Sepanjang Waktu")
                # 1. Casual & Registered Rentals Line Plot by hour
                # Agregasikan data casual dan registered berdasarkan hr
                hourly_data = df.groupby('hr')[['casual', 'registered']].mean().reset_index()

                st.write("### Hourly Rentals: Casual vs Registered")
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=hourly_data, x='hr', y='casual', label='Casual', color='blue', ax=ax)
                sns.lineplot(data=hourly_data, x='hr', y='registered', label='Registered', color='orange', ax=ax)
                ax.set_title('Hourly Rentals: Casual vs Registered')
                ax.set_xlabel('Hour of Day')
                ax.set_ylabel('Average Number of Rentals')
                ax.legend()
                ax.set_xticks(range(0, 24, 2))  # Show every 2 hours on x-axis
                ax.grid(True)
                st.pyplot(fig)

                st.markdown("""
                        **Insight:**
                        - Aktivitas penyewaan pelanggan terdaftar (registered) menunjukkan dua puncak utama:
                            * Pagi (sekitar pukul 8) dan
                            * Sore (sekitar pukul 17-18).
                        - Puncak data pada pelanggan terdaftar (registered) kemungkinan besar mencerminkan perjalanan rutin pergi dan pulang kerja atau sekolah.
                        - Aktivitas pelanggan terdaftar (registered) menurun signifikan di luar jam sibuk ini, terutama pada malam hari.
                        - Penyewaan oleh pengguna umum (casual) lebih konsisten sepanjang hari tanpa puncak yang tajam.
                        - Aktivitas pengguna umum (casual) mencapai puncaknya di sore hari (sekitar pukul 14-16), yang menunjukkan penggunaan untuk rekreasi atau kegiatan santai.
                        """)

                st.write("### Casual & Registered Rentals Heatmap (Weekday vs Hour)")
                # 2. Casual & Registered Rentals Heatmap (Weekday vs Hour)
                # Agregasikan data casual dan registered berdasarkan weekday dan hr
                # Gunakan heatmap untuk menggambarkan intensitas penyewaan
                heatmap_data = df.groupby(['weekday', 'hr'])[['casual', 'registered']].mean().unstack()

                # Create subplots for heatmaps
                fig, axes = plt.subplots(1, 2, figsize=(20, 8), sharey=True)

                # Heatmap for casual
                sns.heatmap(heatmap_data['casual'], cmap='Blues', ax=axes[0], annot=False, cbar=True)
                axes[0].set_title('Casual Rentals Heatmap (Weekday vs Hour)')
                axes[0].set_ylabel('Weekday (0=Sunday)')
                axes[0].set_xlabel('Hour of Day')

                # Heatmap for registered
                sns.heatmap(heatmap_data['registered'], cmap='Oranges', ax=axes[1], annot=False, cbar=True)
                axes[1].set_title('Registered Rentals Heatmap (Weekday vs Hour)')
                axes[1].set_ylabel('')  # Remove y-label for the second plot for cleaner look
                axes[1].set_xlabel('Hour of Day')

                # Show plots
                plt.tight_layout()
                st.pyplot(fig)

                st.markdown("""
                        **Insight:**
                        - Penyewaan oleh pelanggan umum (casual) lebih terkonsentrasi pada akhir pekan (Sabtu, Minggu), sedangkan penyewaan pelanggan terdaftar (registered) lebih tinggi pada hari kerja.
                        - Aktivitas penyewaan pelanggan terdaftar (registered) menunjukkan dua puncak utama: pagi dan sore hari, mungkin berhubungan dengan perjalanan rutin (kerja/sekolah).
                        - Pengguna umum (casual) memiliki pola penyewaan yang lebih merata sepanjang hari, dengan puncak pada sore hari.
                        """)

            if analysis_option == "Q3":
                if analysis_option == "Q3":
                    st.subheader("3️⃣ Anomali lonjakan dan penurunan")

                    # === Bagian 1: Deteksi Anomali ===
                    # 1. Aggregate hourly data to daily data
                    daily_data = df.groupby('dteday').agg({'cnt': 'sum'}).reset_index()

                    # 2. Calculate daily change
                    daily_data['change'] = daily_data['cnt'].diff()
                    daily_data['change'].fillna(0, inplace=True)  # Isi nilai NaN di awal dengan 0

                    # 3. Identify anomalies
                    threshold = daily_data['change'].std() * 2  # Ambang batas: 2 * standar deviasi
                    anomalies = daily_data[abs(daily_data['change']) > threshold]

                    # === Bagian 2: Visualisasi ===
                    st.markdown("### Visualisasi Anomali Penyewaan")

                    # Ensure the 'dteday' column is in datetime format
                    daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])

                    # Create figure and axis for better control
                    fig, ax = plt.subplots(figsize=(14, 7))

                    # Plot garis untuk perubahan harian
                    sns.lineplot(data=daily_data, x='dteday', y='change', ax=ax, label='Daily Change', color='green')

                    # Sorot anomali dengan scatter plot
                    ax.scatter(anomalies['dteday'], anomalies['change'], color='red', label='Anomaly', s=50)

                    # Tambahkan garis horizontal untuk ambang batas
                    ax.axhline(threshold, color='blue', linestyle='--', label='Positive Threshold')
                    ax.axhline(-threshold, color='yellow', linestyle='--', label='Negative Threshold')

                    # Set axis labels and title
                    ax.set_title('Daily Rental Changes with Anomalies Highlighted', fontsize=14)
                    ax.set_xlabel('Date')
                    ax.set_ylabel('Daily Change in Rentals')

                    # Rotate and format X-axis dates for better readability
                    # Set the date format
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

                    # Use MaxNLocator to limit the number of X-axis labels
                    ax.xaxis.set_major_locator(
                        MaxNLocator(integer=True, prune='both', nbins=10))  # Adjust 'nbins' as needed for fewer ticks

                    # Rotate the X-axis labels to prevent overlap
                    fig.autofmt_xdate(rotation=45)

                    # Add legend and grid
                    ax.legend()
                    ax.grid(alpha=0.5)

                    # Adjust layout
                    plt.tight_layout()

                    # Show plot in Streamlit
                    st.pyplot(fig)

                    # === Bagian 3: Analisis ===
                    st.markdown("### Analisis Anomali")
                    st.write(f"Number of anomalies detected: {len(anomalies)}")
                    st.write("Details of Anomalies:")
                    st.dataframe(anomalies)

                    st.markdown("""
                    **Keterangan:**
                    * Garis hijau adalah perubahan jumlah penyewaan sepeda harian. Secara keseluruhan, fluktuasi berada di sekitar 0, menunjukkan pola harian yang relatif stabil dengan beberapa perubahan signifikan.
                    * Titik merah adalah anomali (perubahan signifikan yang melebihi threshold berdasarkan dua kali standar deviasi dari rata-rata perubahan). Ini adalah hari-hari ketika perubahan jumlah penyewaan sepeda sangat besar, baik peningkatan atau penurunan.

                    **Insight:**
                    * Anomali Positif (Peningkatan Penyewaan Drastis):
                        * Titik merah di atas garis 0 menunjukkan peningkatan besar dalam jumlah penyewaan sepeda.
                        * Kemungkinan penyebab adalah cuaca cerah, acara khusus atau liburan, perubahan musim (awal musim semi atau musim panas) cenderung meningkatkan jumlah penyewaan.
                    * Anomali Negatif (Penurunan Penyewaan Drastis):
                        * Titik merah di bawah garis 0 menunjukkan penurunan besar dalam jumlah penyewaan sepeda.
                        * Kemungkinan penyebab adalah cuaca buruk, hari libur tertentu, atau bisa juga perbaikan operasional sepeda.
                    * Anomali lebih sering terlihat pada tahun 2012 dibandingkan dengan tahun 2011. Hal ini mungkin menunjukkan bahwa penggunaan sepeda menjadi populer di tahun kedua.
                    * Perubahan maksimum berkisar antara -5000 hingga +4000. Fluktuasi ini cukup besar dan menunjukkan variabilitas yang tinggi dalam jumlah penyewaan dari hari ke hari.

                    ---
                    """)


                    # === Bagian 2: Analisis Hubungan dengan Kondisi Cuaca ===
                    # 1. Aggregate hourly data for weather and windspeed
                    hourly_aggregated = df.groupby('dteday').agg({
                        'weathersit': lambda x: x.mode()[0],  # Modus untuk kondisi cuaca
                        'windspeed': 'mean',  # Rata-rata kecepatan angin
                        'cnt': 'sum'
                    }).reset_index()

                    # 2. Merge anomalies with weather data
                    merged_data = anomalies.merge(hourly_aggregated, on='dteday', how='left')

                    # 3. Visualize anomalies with windspeed and weathersit
                    st.markdown("### Visualisasi Hubungan dengan Kecepatan Angin dan Cuaca")
                    plt.figure(figsize=(12, 6))
                    sns.scatterplot(data=merged_data, x='change', y='windspeed', hue='weathersit', palette='viridis')
                    plt.axhline(df['windspeed'].mean(), color='red', linestyle='--',
                                label='Average Windspeed')
                    plt.title('Anomalies vs Windspeed and Weathersit')
                    plt.xlabel('Daily Change in Rentals')
                    plt.ylabel('Windspeed')
                    plt.legend(title='Weathersit')
                    plt.tight_layout()

                    # Show plot in Streamlit
                    st.pyplot(plt)

                    # 4. Descriptive statistics for anomalies by weathersit
                    anomalies_weather = merged_data.groupby('weathersit').agg({
                        'change': ['mean', 'std'],  # Statistik untuk perubahan penyewaan
                        'windspeed': ['mean', 'std'],  # Statistik untuk kecepatan angin
                        'dteday': 'count'  # Jumlah hari anomali
                    }).rename(columns={'dteday': 'count_anomalies'})

                    st.markdown("### Statistik Deskriptif untuk Anomali Berdasarkan Cuaca")
                    st.dataframe(anomalies_weather)

                    st.markdown("""
                    **Keterangan:**

                    1. Rentang windspeed dalam anomali:
                        * Sebagian besar nilai windspeed berada dalam kisaran 0.2 (ditandai garis merah horizontal).
                        * Beberapa anomali dengan perubahan besar (baik positif maupun negatif) berada pada windspeed tinggi (> 0.3), yang sepertinya diakibatkan cuaca buruk.

                    2. Distribusi Anomali Berdasarkan Weathersit
                        * weathersit = 1 (Clear, Few Clouds): Didominasi oleh anomali positif (peningkatan rental sepeda).
                        * weathersit = 2 (Mist, Cloudy): Campuran anomali positif dan negatif.
                        * weathersit = 3 (Light Snow/Rain): Didominasi oleh anomali negatif (penurunan rental sepeda).

                    **Insight:**
                    1. Cuaca cerah (weathersit = 1) mendukung peningkatan signifikan dalam penyewaan sepeda meskipun ada anomali.
                    2. Cuaca buruk (weathersit = 3) mengurangi penyewaan secara drastis.
                    3. Kecepatan angin memiliki korelasi moderat dengan anomali, dengan angin rendah meningkatkan penyewaan pada cuaca cerah.
                    """)

# Clustering Section
elif selected == "Clustering":
    df, error = load_data(HOUR_CSV_PATH)
    if error:
        st.error(error)
    elif df is not None:
        st.subheader("Clustering Based On Weathersit & Holiday")

        # Analisis Lanjutan : Clustering Berdasarkan Cuaca
        # Group data by weathersit and calculate mean rentals
        # Group data by weathersit and holiday, and calculate mean rentals
        weather_holiday_clusters = df.groupby(['weathersit', 'holiday']).agg({
            'casual': 'mean',
            'registered': 'mean'
        }).reset_index()

        # Rename columns for better readability
        weather_holiday_clusters.columns = ['Weathersit', 'Holiday', 'Casual Rentals', 'Registered Rentals']

        # Define the full range of weathersit categories (modify based on your dataset if needed)
        weathersit_categories = [1, 2, 3, 4]  # 1: Clear, 2: Mist, 3: Light Snow/Rain, 4: Heavy Rain/Snow

        # Split data into holiday and non-holiday
        holiday_data = weather_holiday_clusters[weather_holiday_clusters['Holiday'] == 1].set_index('Weathersit')
        non_holiday_data = weather_holiday_clusters[weather_holiday_clusters['Holiday'] == 0].set_index('Weathersit')

        # Reindex to include all weathersit categories and fill missing values with 0
        holiday_data = holiday_data.reindex(weathersit_categories, fill_value=0).reset_index()
        non_holiday_data = non_holiday_data.reindex(weathersit_categories, fill_value=0).reset_index()

        # Display clustered data
        st.dataframe(weather_holiday_clusters)

        # Visualization: Compare rentals across weather conditions for holidays and non-holidays
        fig, ax = plt.subplots(figsize=(12, 7))

        bar_width = 0.35
        index = np.arange(len(weathersit_categories))  # Create a consistent index for all weathersit categories

        # Improved color scheme for better visual distinction
        holiday_casual_color = '#1f77b4'  # Dark Blue
        non_holiday_casual_color = '#aec7e8'  # Light Blue
        holiday_registered_color = '#ff7f0e'  # Orange
        non_holiday_registered_color = '#ffbb78'  # Light Orange

        # Plot casual rentals data
        ax.bar(index - bar_width / 2, holiday_data['Casual Rentals'], bar_width, label='Casual Rentals (Holiday)',
               color=holiday_casual_color)
        ax.bar(index - bar_width / 2, non_holiday_data['Casual Rentals'], bar_width,
               label='Casual Rentals (Non-Holiday)', color=non_holiday_casual_color, alpha=0.8)

        # Plot registered rentals data
        ax.bar(index + bar_width / 2, holiday_data['Registered Rentals'], bar_width,
               label='Registered Rentals (Holiday)', color=holiday_registered_color)
        ax.bar(index + bar_width / 2, non_holiday_data['Registered Rentals'], bar_width,
               label='Registered Rentals (Non-Holiday)', color=non_holiday_registered_color, alpha=0.8)

        # Add labels, title, and legend
        ax.set_xlabel('Weathersit')
        ax.set_ylabel('Average Rentals (Casual vs Registered)')
        ax.set_title('Casual vs Registered Rentals by Weathersit and Holiday')
        ax.set_xticks(index)
        ax.set_xticklabels(['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
        ax.legend()

        # Show plot in Streamlit
        st.pyplot(fig)

        st.markdown("""
            **Insight:**
            * Dalam keadaan cuaca apapun, pelanggan terdaftar memiliki jumlah penyewaan terbanyak baik untuk hari libur ataupun kerja.
            * Pelanggan umum lebih banyak menyewa sepeda saat hari libur, sedangkan pelanggan terdaftar lebih banyak saat hari kerja.
            * Cuaca cerah (clear) cenderung memiliki rata-rata penyewaan tertinggi, baik untuk pelanggan umum (casual) maupun pelanggan terdaftar (registered).
            * Kondisi cuaca buruk (heavy rain/snow) memiliki rata-rata penyewaan terendah, menunjukkan pengaruh negatif dari cuaca buruk.
            * Saat cuaca buruk, penyewaan pelanggan umum maupun terdaftar jumlahnya minimal, terlepas apakah hari kerja ataupun libur.
        """)

# Conclusion Section
elif selected == "Conclusion":
    st.header("Kesimpulan")
    # Conclusion for Question 1
    st.subheader("🎯 Kesimpulan Pertanyaan 1")
    st.markdown(
        """
        *Bagaimana perbedaan pola peminjaman sepeda antara pengguna umum (casual) dibandingkan dengan pengguna terdaftar (registered)?*
        """
    )
    st.markdown("""
    - **Data ini** memperlihatkan pentingnya peran layanan sepeda sebagai alat transportasi harian bagi **pelanggan terdaftar (registered)**, 
      sementara bagi **pelanggan umum (casual)**, sepeda lebih banyak digunakan untuk aktivitas rekreasi.
    - **Peningkatan fasilitas** dan ketersediaan sepeda selama **hari kerja** mungkin lebih penting untuk memenuhi kebutuhan pengguna terdaftar.
    - Pada **akhir pekan**, fokus pada pelanggan umum, seperti promosi atau kampanye wisata bersepeda, dapat menarik lebih banyak pengguna.
    """)

    # Conclusion for Question 2
    st.subheader("🎯 Kesimpulan Pertanyaan 2")
    st.markdown(
        """
        *Pada jam-jam berapakah dalam sehari terdapat konsentrasi penyewaan sepeda tertinggi untuk pengguna umum dan pengguna terdaftar?*
        """
    )
    st.markdown("""
    - **Pelanggan terdaftar (registered)** mendominasi penyewaan selama jam sibuk (pagi dan sore), mengindikasikan penggunaan layanan sebagai alat transportasi utama.
    - **Pelanggan umum (casual)** memiliki volume penyewaan yang jauh lebih rendah dibandingkan pengguna terdaftar, tetapi konsisten sepanjang hari.
    - **Perbedaan pola ini** mengindikasikan bahwa pengguna terdaftar lebih terikat pada jadwal harian (misalnya, pekerjaan atau sekolah), sementara pelanggan umum lebih fleksibel dalam memilih waktu penyewaan.
    - Untuk memberi pelayanan maksimal kepada **pelanggan terdaftar (registered)**, ketersediaan sepeda selama **jam sibuk (pagi dan sore)** sangat penting.
    - Untuk **pelanggan umum (casual)**, bisa digunakan promosi dan layanan tambahan di sore hari atau akhir pekan agar dapat meningkatkan penyewaan.
    """)

    # Conclusion for Question 3
    st.subheader("🎯 Kesimpulan Pertanyaan 3")
    st.markdown(
        """
        *Bisakah kita mengenali anomali atau kejadian besar (seperti cuaca ekstrem atau hari libur nasional) berdasarkan lonjakan atau penurunan tiba-tiba dalam jumlah penyewaan sepeda (cnt)?*
        """
    )
    st.markdown("""
    - **Cuaca cerah** cenderung meningkatkan penyewaan meskipun ada anomali, sementara **cuaca buruk** menurunkan penyewaan.
    - **Kecepatan angin** berpengaruh, tetapi efeknya lebih signifikan ketika dikombinasikan dengan kondisi cuaca tertentu.
    """)

    # Conclusion for Advanced Analysis: Clustering Based on Weather
    st.subheader("🎯 Kesimpulan Analisis Lanjutan")
    st.markdown("""***Clustering Berdasarkan Cuaca & Libur***""")
    st.markdown("""
    - Liburan berpengaruh lebih banyak pada pelanggan umum, terutama dalam kondisi cuaca yang lebih baik (cerah atau berkabut). Hal ini terjadi karena kegiatan rekreasi lebih sering dilakukan pada hari libur dengan cuaca yang mendukung.
    - Pelanggan terdaftar memiliki jumlah penggunaan yang tinggi selama hari kerja. Hal ini dipengaruhi oleh kebutuhan perjalanan rutin.
    - Cuaca cerah menunjukkan angka penyewaan tertinggi di semua kategori. Artinya, cuaca berdampak baik dan signifikan terhadap penggunaan sepeda.
    - Cuaca buruk (salju/hujan ringan atau lebat) menyebabkan penurunan drastis penggunaan sepeda, terlepas apakah itu hari libur atau tidak.
    - Promosi atau diskon bisa dibuat untuk pengguna umum (casual) pada hari libur, terutama saat cuaca cerah, agar dapat lebih meningkatkan penggunaan/penyewaan sepeda.
    - Perlu penyediaan perlengkapan atau fasilitas tahan cuaca untuk membantu menjaga jumlah pelanggan saat cuaca berkabut atau sedikit hujan.
    
    """)

else:
    st.error("Dataset could not be loaded. Please check the data source.")


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
        options=["Introduction", "Background", "Analysis", "Conclusion"],
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
    st.write(
        "- **Data Source:** [Dataset Link](https://github.com/esnanta/data-analysis/raw/main/Dataset/Bike-sharing-dataset.zip)"
    )

    st.subheader("Analisis Akan Menjawab Pertanyaan Berikut:")
    st.markdown(
        """
        - Bagaimana perbedaan pola peminjaman sepeda antara pengguna umum (casual) dibandingkan dengan pengguna terdaftar (registered)?
        - Pada jam-jam berapakah dalam sehari terdapat konsentrasi penyewaan sepeda tertinggi untuk pengguna umum dan pengguna terdaftar?
        - Bisakah kita mengenali anomali atau kejadian besar (seperti cuaca ekstrem atau hari libur nasional) berdasarkan lonjakan atau penurunan tiba-tiba dalam jumlah penyewaan sepeda (cnt)?
        """
    )

# Data Background Section
if selected == "Background":
    st.title("Background 🌍")

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
                st.subheader("2️⃣ Apa Tren Penggunaan Sepeda Sepanjang Waktu?")
                st.markdown("""
                **Tahapan analisa:**
                1. Agregasikan data casual dan registered berdasarkan hr.
                    * Tujuannya untuk menemukan jam konsentrasi tinggi untuk pengguna umum (casual) dan terdaftar (registered).
                    * Gunakan line plot untuk menunjukkan pola sepanjang hari.

                2. Heatmap penyewaan berdasarkan jam (hr) dan hari (weekday) dengan mengagregasikan data penyewaan berdasarkan hr dan weekday.
                    * Tujuannya untuk menunjukkan pola penggunaan berdasarkan kombinasi jam dan hari.
                    * Gunakan heatmap untuk menggambarkan intensitas penyewaan.
                """)

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
                        - Data pelanggan umum (casual) lebih terkonsentrasi pada hari weekend (Sabtu, Minggu), sedangkan pelanggan (terdaftar) lebih pada hari-hari kerja.
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
                st.subheader("3️⃣ Anomali berdasarkan lonjakan atau penurunan tiba-tiba")
                if analysis_option == "Q3":
                    st.subheader("3️⃣ Anomali berdasarkan lonjakan atau penurunan tiba-tiba")

                    st.markdown("""
                    **Tahapan analisa:**

                    1. **Analisis Lonjakan dan Penurunan Penyewaan**, untuk mengidentifikasi anomali.
                        * Menghitung Perubahan Penyewaan Harian
                            - Data penyewaan sepeda yang awalnya berbasis jam (hourly) diubah menjadi berbasis harian (daily) dengan menjumlahkan total penyewaan (cnt) setiap harinya menggunakan fungsi `groupby` dan `agg`.
                            - Hitung perubahan harian dalam jumlah penyewaan sepeda menggunakan fungsi `diff()`.
                            - Tambahkan variabel baru bernama `change` untuk menyimpan nilai selisih antara total penyewaan sepeda dari satu hari ke hari berikutnya. Nilai yang kosong di awal data (NaN) diisi dengan 0 menggunakan `fillna(0)`.
                        * Mengidentifikasi Lonjakan dan Penurunan yang Signifikan (Anomali)
                            - Hitung ambang batas untuk mendeteksi anomali menggunakan dua kali standar deviasi (`2 * std`) dari nilai perubahan harian (`change`).
                            - Tandai data yang memiliki nilai perubahan lebih besar atau lebih kecil dari ambang batas ini sebagai anomali.
                        * Visualisasi Perubahan Penyewaan dengan Sorotan Anomali
                            - Buat plot garis untuk menampilkan perubahan jumlah penyewaan harian dari waktu ke waktu.
                            - Sorot anomali dengan menambahkan titik berwarna merah pada plot untuk menunjukkan lonjakan atau penurunan yang signifikan.
                            - Tambahkan garis horizontal untuk menunjukkan ambang batas positif dan negatif, sehingga mempermudah interpretasi visual.
                    """)

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
                    st.markdown("### Visualisasi Perubahan Penyewaan dengan Anomali")
                    plt.figure(figsize=(14, 7))

                    # Plot garis untuk perubahan harian
                    sns.lineplot(data=daily_data, x='dteday', y='change', label='Daily Change', color='green')

                    # Sorot anomali dengan scatter plot
                    plt.scatter(anomalies['dteday'], anomalies['change'], color='red', label='Anomaly', s=50)

                    # Tambahkan garis horizontal untuk ambang batas
                    plt.axhline(threshold, color='blue', linestyle='--', label='Positive Threshold')
                    plt.axhline(-threshold, color='yellow', linestyle='--', label='Negative Threshold')

                    # Perbaiki format tanggal pada sumbu X
                    plt.xticks(rotation=45)
                    plt.title('Daily Rental Changes with Anomalies Highlighted', fontsize=14)
                    plt.xlabel('Date')
                    plt.ylabel('Daily Change in Rentals')
                    plt.legend()
                    plt.grid(alpha=0.5)
                    plt.tight_layout()

                    # Show plot in Streamlit
                    st.pyplot()

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

                    st.markdown("""
                    2. **Analisis Faktor Eksternal** untuk mengidentifikasi apakah anomali penyewaan berkaitan dengan kondisi cuaca tertentu.

                        * Gabungkan data anomali dengan data cuaca dan kecepatan angin.
                            - Kelompokkan data jam ke data harian untuk menghitung statistik rata-rata kecepatan angin (windspeed) dan kondisi cuaca (weathersit) harian.
                            - Gunakan merge untuk menggabungkan data anomali dengan data cuaca dan kecepatan angin berdasarkan kolom tanggal (dteday).
                        * Visualisasi Hubungan antara Perubahan Penyewaan, Kecepatan Angin, dan Situasi Cuaca.
                            - Gunakan scatter plot untuk memvisualisasikan perubahan harian (change) pada penyewaan terhadap kecepatan angin, dengan warna mewakili kondisi cuaca (weathersit).
                            - Tambahkan garis horizontal untuk menyoroti rata-rata kecepatan angin sebagai referensi.
                        * Rangkum Dengan Statistik Deskriptif.
                            - Hitung rata-rata dan standar deviasi untuk perubahan penyewaan (change) dan kecepatan angin (windspeed) berdasarkan situasi cuaca (weathersit).
                            - Tampilkan jumlah hari anomali untuk setiap kondisi cuaca.
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
                    st.pyplot()

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

                    # Analisis Lanjutan : Clustering Berdasarkan Cuaca

                    # Group data by weathersit
                    weathersit_clusters = df.groupby('weathersit').agg({
                        'casual': 'mean',  # Rata-rata penyewaan casual
                        'registered': 'mean',  # Rata-rata penyewaan terdaftar
                        'temp': 'mean',  # Suhu rata-rata
                        'windspeed': 'mean',  # Kecepatan angin rata-rata
                        'hum': 'mean',  # Kelembapan rata-rata
                    }).reset_index()

                    # Rename columns for better readability
                    weathersit_clusters.columns = [
                        'Weathersit', 'Casual Rentals', 'Registered Rentals',
                        'Average Temp', 'Average Windspeed', 'Average Humidity'
                    ]

                    # Display clustered data
                    st.markdown("### Clustering Penyewaan Berdasarkan Cuaca")
                    st.dataframe(weathersit_clusters)

                    # Visualization: Comparing registered and casual rentals across weathersit
                    plt.figure(figsize=(10, 6))
                    bar_width = 0.35
                    index = weathersit_clusters['Weathersit']

                    plt.bar(index - bar_width / 2, weathersit_clusters['Casual Rentals'], bar_width,
                            label='Casual Rentals', color='skyblue')
                    plt.bar(index + bar_width / 2, weathersit_clusters['Registered Rentals'], bar_width,
                            label='Registered Rentals', color='orange')

                    plt.xlabel('Weathersit')
                    plt.ylabel('Average Rentals (Casual vs Registered)')
                    plt.title('Casual vs Registered Rentals by Weathersit')
                    plt.xticks(ticks=weathersit_clusters['Weathersit'],
                               labels=['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
                    plt.legend()
                    plt.tight_layout()

                    # Show plot in Streamlit
                    st.pyplot()

                    st.markdown("""
                    **Insight:**
                    * Cuaca cerah (Clear) cenderung memiliki rata-rata penyewaan tertinggi, baik untuk casual maupun registered.
                    * Kondisi cuaca buruk (Light Snow/Rain dan Heavy Rain/Snow) memiliki rata-rata penyewaan terendah, menunjukkan pengaruh negatif dari cuaca buruk.
                    * Casual rentals lebih sensitif terhadap perubahan cuaca dibandingkan registered rentals.
                    """)

        else:
            st.error("Dataset could not be loaded. Please check the data source.")

# Conclusion Section
if selected == "Conclusion":
    st.header("Kesimpulan")

    # Conclusion for Question 1
    st.subheader("🎯 Kesimpulan Pertanyaan 1")
    st.markdown("""
    - **Data ini** memperlihatkan pentingnya peran layanan sepeda sebagai alat transportasi harian bagi **pelanggan terdaftar (registered)**, 
      sementara bagi **pelanggan umum (casual)**, sepeda lebih banyak digunakan untuk aktivitas rekreasi.
    - **Peningkatan fasilitas** dan ketersediaan sepeda selama **hari kerja** mungkin lebih penting untuk memenuhi kebutuhan pengguna terdaftar.
    - Pada **akhir pekan**, fokus pada pelanggan umum, seperti promosi atau kampanye wisata bersepeda, dapat menarik lebih banyak pengguna.
    """)

    # Conclusion for Question 2
    st.subheader("🎯 Kesimpulan Pertanyaan 2")
    st.markdown("""
    - **Pelanggan terdaftar (registered)** mendominasi penyewaan selama jam sibuk (pagi dan sore), mengindikasikan penggunaan layanan sebagai alat transportasi utama.
    - **Pelanggan umum (casual)** memiliki volume penyewaan yang jauh lebih rendah dibandingkan pengguna terdaftar, tetapi konsisten sepanjang hari.
    - **Perbedaan pola ini** mengindikasikan bahwa pengguna terdaftar lebih terikat pada jadwal harian (misalnya, pekerjaan atau sekolah), sementara pelanggan umum lebih fleksibel dalam memilih waktu penyewaan.
    - Untuk memberi pelayanan maksimal kepada **pelanggan terdaftar (registered)**, ketersediaan sepeda selama **jam sibuk (pagi dan sore)** sangat penting.
    - Untuk **pelanggan umum (casual)**, bisa digunakan promosi dan layanan tambahan di sore hari atau akhir pekan agar dapat meningkatkan penyewaan.
    """)

    # Conclusion for Question 3
    st.subheader("🎯 Kesimpulan Pertanyaan 3")
    st.markdown("""
    - **Cuaca cerah** cenderung meningkatkan penyewaan meskipun ada anomali, sementara **cuaca buruk** menurunkan penyewaan.
    - **Kecepatan angin** berpengaruh, tetapi efeknya lebih signifikan ketika dikombinasikan dengan kondisi cuaca tertentu.
    """)

    # Conclusion for Advanced Analysis: Clustering Based on Weather
    st.subheader("🎯 Kesimpulan Analisis Lanjutan: Clustering Berdasarkan Cuaca")
    st.markdown("""
    - **Kondisi cuaca buruk** (Light Snow/Rain dan Heavy Rain/Snow) memiliki rata-rata penyewaan terendah, menunjukkan pengaruh negatif dari cuaca buruk.
    - **Pelanggan umum (casual)** lebih sensitif terhadap perubahan cuaca dibandingkan dengan **pelanggan terdaftar (registered)**.
    """)

    # Adding some finishing touches to make the conclusions visually appealing.
    st.markdown("---")
    st.markdown("*Penting untuk selalu memperhatikan faktor-faktor eksternal, seperti cuaca dan waktu, untuk merancang strategi layanan yang lebih baik dan sesuai dengan kebutuhan pengguna. Analisis ini memberikan wawasan penting untuk pengelolaan operasional sepeda secara lebih efektif.*")


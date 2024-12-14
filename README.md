# Bike Sharing Data Analysis

This project provides a comprehensive analysis of bike-sharing systems, specifically focusing on the Capital Bikeshare system in Washington D.C. It was completed as part of my study on the Dicoding platform. The dataset includes data from 2011 and 2012, covering both hourly and daily usage.

## Objective
The primary objective of this project is to explore and analyze bike-sharing data to answer the following questions:

1. **How do bike rental patterns differ between casual and registered users?**
2. **What times of the day experience the highest bike rental volumes for casual and registered users?**
3. **How do rental behaviors vary across different time periods (morning, afternoon, evening, and night)?**
4. **Can anomalies or significant events (e.g., extreme weather or national holidays) be identified based on sudden spikes or drops in bike rentals (`cnt`)?**

## Dataset
The dataset, `Bike-sharing-dataset.zip`, includes the following files:

- `day.csv`: Daily bike-sharing data.
- `hour.csv`: Hourly bike-sharing data.

### Notable Columns
The dataset contains various variables that enable a detailed analysis of bike-sharing trends:

- **`casual`**: Count of casual users.
- **`registered`**: Count of registered users.
- **`cnt`**: Total bike rentals (casual + registered).
- **`hr`**: Hour of the day (in the hourly dataset).
- **`holiday`**: Indicator for national holidays (1 for holiday, 0 for non-holiday).
- **`weathersit`**: Weather situation (e.g., clear, cloudy, rainy).
- **`temp`**: Normalized temperature.

## Tools Used
- **Python**: For data manipulation and analysis.
- **Google Colab**: As the development environment for executing Python scripts.
- **Pandas**: For efficient data processing.
- **Matplotlib** and **Seaborn**: For creating insightful visualizations.
- **Streamlit**: To build and deploy the interactive data analysis dashboard.

## Streamlit Dashboard
Explore the interactive dashboard to dive deeper into the analysis:  
[Bike Sharing Data Analysis Dashboard](https://esnanta-bikesharing-analysis.streamlit.app/)

## Analysis Highlights
1. **User Patterns**: Analyzed the rental behaviors of casual and registered users to identify trends.
2. **Peak Hours**: Identified peak rental hours for both user types based on hourly data.
3. **Anomalies and Events**: Investigated anomalies, such as extreme weather or holidays, to determine their impact on bike rentals.
4. **Clustering Analysis**: Grouped rental behaviors into distinct time periods (Morning, Afternoon, Evening, Night) to uncover differences in user activity.

## Clustering Analysis by Time Period
To better understand bike rental behaviors across the day, the dataset was grouped into four time periods:

- **Morning (5:00 AM - 11:00 AM)**  
- **Afternoon (12:00 PM - 4:00 PM)**  
- **Evening (5:00 PM - 8:00 PM)**  
- **Night (9:00 PM - 4:00 AM)**  

### Key Findings:
- During holidays, **casual users** dominate rental activity across all time periods, with the highest activity in the Evening and Night.  
- Registered users are more active during workdays and primarily during Morning and Evening commute hours.  
- Nighttime rentals are generally lower but show a higher proportion of casual users during holidays.

## Insights
1. **User Segmentation**:
   - Casual users are more likely to rent bikes on weekends and holidays for leisure purposes.
   - Registered users consistently use bikes as part of their daily commute.
2. **Time-Based Trends**:
   - The Evening period exhibits the highest rental activity for both user groups, particularly during holidays.
   - Morning rentals are predominantly made by registered users for work commutes.
3. **Impact of Events**:
   - Weather conditions and holidays significantly influence rental patterns, causing spikes or drops in the number of rentals.
4. **Optimization Opportunities**:
   - Bikes and infrastructure can be better distributed to accommodate demand surges during Evening and Night periods, particularly on holidays.

## How to Run the Analysis
1. Clone the repository:
   ```bash
   git clone https://github.com/esnanta/data-analysis.git

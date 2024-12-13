# Bike Sharing Data Analysis

This project is a data analysis of bike-sharing systems, specifically focusing on the Capital Bikeshare system in Washington D.C. It was completed as part of my study on the Dicoding platform. The dataset used contains information from 2011 and 2012, covering both hourly and daily data.

## Objective
The primary objective of this project is to explore and analyze the bike-sharing data to answer the following questions:

1. **How do bike rental patterns differ between casual and registered users?**
2. **What times of the day see the highest concentrations of bike rentals for casual and registered users?**
3. **Can we identify anomalies or major events (such as extreme weather or national holidays) based on sudden spikes or drops in bike rentals (`cnt`)?**

## Dataset
The dataset, `Bike-sharing-dataset.zip`, includes the following files:

- `day.csv`: Daily bike-sharing data.
- `hour.csv`: Hourly bike-sharing data.

The dataset contains variables related to environmental factors, seasonal trends, and rental information. Notable columns include:

- `casual`: Count of casual users.
- `registered`: Count of registered users.
- `cnt`: Total bike rentals (casual+registered).
- `weathersit`: Weather situation.
- `temp`: Normalized temperature.
- `holiday`: Indicator for national holidays.

## Tools Used
- **Python**: For data analysis and visualization.
- **Google Colab**: To write and execute Python code.
- **Pandas**: For data manipulation.
- **Matplotlib** and **Seaborn**: For data visualization.

## Analysis Highlights
- **User Patterns**: Examined the differences in rental behaviors between casual and registered users.
- **Peak Hours**: Identified peak rental hours for both user types using hourly data.
- **Anomalies and Events**: Investigated anomalies in the data, such as significant weather events or holidays, to understand their impact on bike rentals.

## Insights
1. Casual users tend to rent bikes more on weekends and holidays, while registered users display a consistent pattern aligned with work schedules.
2. Peak rental hours for registered users are during morning and evening commute times, whereas casual users favor midday rentals.
3. Sudden spikes or drops in rental counts were often associated with extreme weather conditions or holidays.

## How to Run the Analysis
1. Clone the repository:
   ```bash
   git clone https://github.com/esnanta/data-analysis.git
   ```
2. Extract the `Bike-sharing-dataset.zip` file into the project directory.
3. Open the `bike_sharing_analysis.ipynb` file in Google Colab or Jupyter Notebook.
4. Run all cells to reproduce the analysis and visualizations.

## Future Improvements
- Incorporate machine learning models to predict bike rental demands.
- Expand analysis to include data from more recent years.
- Integrate additional external datasets, such as traffic or public events, to improve anomaly detection.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- Dicoding Platform for providing guidance and resources.
- UCI Machine Learning Repository for the dataset.

Feel free to contribute or reach out with feedback or questions!

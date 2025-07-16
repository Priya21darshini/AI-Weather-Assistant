🌤️ WeatherWise – AI-Powered Weather Assistant

🔍 Overview

WeatherWise is a smart and interactive weather assistant built using Streamlit, OpenWeatherMap API, and Plotly, enhanced with:

🌍 Nearby cities weather visualization on map

📈 Hourly and 5-day temperature forecasts

🌫️ Air Quality Index (AQI) with gas component analysis

🤖 AI-generated weather tips

🕒 Sunrise/Sunset in local timezone

📡 Clean driving condition suggestions

🚀 Features

✅ Get current weather by city

✅ Real-time AQI + pollutant breakdown (PM2.5, NO2, CO, etc.)

✅ Hourly forecast with condition annotations

✅ Interactive 5-day forecast chart

✅ Map view of nearby Indian cities (within 100–150 km)

✅ Personalized weather tips using AI

🛠️ Tech Stack

| Component          | Tech                                    |
| ------------------ | --------------------------------------- |
| Backend API        | OpenWeatherMap API                      |
| Frontend           | Streamlit                               |
| Data Visualization | Plotly, PyDeck                          |
| Map Rendering      | pydeck + geospatial logic               |
| Language           | Python                                  |
| Dataset            | `worldcities.csv` (for cities in India) |

📸 Screenshots

Please refer to the `screenshots/` folder for visuals of the app interface, including:

- Main weather display
- Nearby cities map
- Gas concentration ratios
- Hourly_temperature
-5day_temperature

 ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Priya21darshini/WeatherWise.git
   cd WeatherWise

2.***Create Virtual Environment***

python -m venv venv

3.***Activate the virtual environment***

venv\Scripts\activate

4.***Install dependencies***
 
 pip install -r requirements.txt

5.***Run the app***

streamlit run app.py


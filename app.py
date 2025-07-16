import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd

from weather_api import (
    get_weather,
    get_forecast,
    get_coordinates,
    get_hourly_forecast,
    get_nearby_weather
)
from ai_tip_generator import generate_weather_tip
from visualizer import (
    show_map,
    plot_temp_forecast,
    show_weather_highlights,
    plot_hourly_forecast
)
from utils import get_weather_icon

# ✅ Load environment variables
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
print("✅ DEBUG - API KEY LOADED =", api_key)

# ✅ Streamlit app config
st.set_page_config(page_title="WeatherWise ☁️", layout="centered")
st.title("🌤️ WeatherWise – AI-Powered Weather Assistant")

# ✅ City input
city = st.text_input("Enter a city name:")
st.write("🛠️ Debug: City entered =", city)

# ✅ Main logic on button click
if st.button("Get Weather Report"):
    if not city:
        st.warning("⚠️ Please enter a city name.")
        st.stop()

    st.info("⏳ Fetching weather data...")

    try:
        # 🔹 Get main city weather
        with st.spinner("Getting weather info..."):
            weather_data = get_weather(city)

        if not weather_data:
            st.error("❌ Weather data could not be retrieved.")
            st.stop()

        lat, lon = weather_data['lat'], weather_data['lon']
        icon = get_weather_icon(weather_data['weather'])

        # 🔹 Show current weather
        st.success(f"{icon} **Weather in {city.title()}:** {weather_data['weather']}, {weather_data['temp']}°C")

        # 🔹 AI tip
        with st.spinner("🤖 Generating AI Tip..."):
            try:
                tip = generate_weather_tip(city, weather_data['weather'], weather_data['temp'])
                st.markdown(f"**💡 AI Suggestion:** _{tip}_")
            except Exception:
                st.warning("⚠️ AI tip could not be generated.")

        # 🔹 Nearby weather
        with st.spinner("📡 Loading nearby cities..."):
            try:
                nearby_weather = get_nearby_weather(lat, lon)[:5]
            except Exception as e:
                nearby_weather = []
                st.warning("⚠️ Nearby cities could not be fetched.")
                st.text(f"Error: {e}")

        # 🔹 Map with nearby cities
        st.markdown("### 🗺️ City & Nearby Areas Map")
        try:
            show_map(lat, lon, icon, nearby_locations=nearby_weather)
        except Exception as e:
            st.warning("⚠️ Could not load map.")
            st.text(f"Error: {e}")

        # 🔹 Weather highlights
        show_weather_highlights(
            wind_kph=weather_data.get('wind_kph', 0),
            wind_dir=weather_data.get('wind_dir', '--'),
            sunrise=weather_data.get('sunrise', '--'),
            sunset=weather_data.get('sunset', '--'),
            aqi=weather_data.get('aqi', '--'),
            humidity=weather_data.get('humidity', '--')
        )

        # 🔹 Gas component ratios
        components = weather_data.get("components", {})
        if components:
            st.markdown("### 🌫️ Gas Component Ratios (μg/m³)")
            gas_df = pd.DataFrame(components.items(), columns=["Gas", "Concentration"])
            gas_df = gas_df.sort_values(by="Concentration", ascending=False).reset_index(drop=True)
            st.table(gas_df)

        # 🔹 Hourly forecast
        with st.spinner("Fetching hourly forecast..."):
            hourly_data = get_hourly_forecast(city)

        st.markdown("### ⏰ Hourly Weather Forecast (Next 24 Hours)")
        if hourly_data:
            plot_hourly_forecast(hourly_data)
        else:
            st.info("❗ Hourly forecast not available.")

        # 🔹 5-day forecast
        with st.spinner("Fetching 5-day forecast..."):
            forecast_dates, forecast_temps = get_forecast(city)

        st.markdown(f"### 📈 {len(forecast_dates)}-Day Temperature Forecast")
        if forecast_dates and forecast_temps:
            plot_temp_forecast(forecast_dates, forecast_temps)
        else:
            st.info("⚠️ Forecast data not available.")

        # ✅ Footer
        st.markdown("---")
        st.success("✅ Weather and nearby cities loaded successfully!")

    except Exception as e:
        st.error("❌ An unexpected error occurred.")
        st.text(f"Error: {e}")

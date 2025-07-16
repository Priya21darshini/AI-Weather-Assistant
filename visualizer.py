import streamlit as st
import plotly.graph_objects as go
import pydeck as pdk
from datetime import datetime

# ✅ Show map with main and nearby cities using pydeck
def show_map(lat, lon, icon="📍", nearby_locations=None):
    try:
        locations = [{
            "position": [lon, lat],
            "tooltip": f"{icon} Main City"
        }]

        if nearby_locations:
            for place in nearby_locations:
                temp_display = f"{place['temp']}°C" if place['temp'] is not None else "Temp N/A"
                locations.append({
                    "position": [place["lon"], place["lat"]],
                    "tooltip": f"{place.get('icon', '🌡️')} {place['city']}: {temp_display}"
                })

        st.pydeck_chart(pdk.Deck(
            map_style="light",
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=6,
                pitch=0
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=locations,
                    get_position="position",
                    get_color="[0, 120, 255, 160]",
                    get_radius=8000,
                    pickable=True
                ),
            ],
            tooltip={"text": "{tooltip}"}
        ), use_container_width=True)
    except Exception as e:
        st.warning("⚠️ Map loading failed: " + str(e))


# ✅ Plot 5-day temperature forecast
def plot_temp_forecast(dates, temps):
    if not dates or not temps:
        st.info("📉 No forecast data available.")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=temps,
        mode='lines+markers',
        name='Avg Temp (°C)',
        line=dict(color='orange'),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title=f"📈 {len(dates)}-Day Temperature Forecast",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)


# ✅ Plot hourly forecast for next 24 hours
def plot_hourly_forecast(hourly_data):
    if not hourly_data:
        st.info("⏰ No hourly forecast data available.")
        return

    times = [datetime.strptime(entry['time'], "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p") for entry in hourly_data]
    temps = [entry['temp'] for entry in hourly_data]
    descs = [entry.get('desc') or entry.get('condition', 'N/A') for entry in hourly_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=temps,
        mode='lines+markers+text',
        name='Temp (°C)',
        line=dict(color='skyblue'),
        marker=dict(size=8),
        text=descs,
        textposition='top center'
    ))
    fig.update_layout(
        title="🌡️ Hourly Temperature Forecast (Next 24 Hours)",
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)


# ✅ Display additional weather information
def show_weather_highlights(wind_kph, wind_dir, sunrise, sunset, aqi, humidity):
    st.markdown("### 🌤️ Additional Weather Info")
    st.markdown(f"**🌬️ Wind:** {wind_kph} km/h {wind_dir}")
    st.markdown(f"**🌅 Sunrise:** {sunrise} | **🌇 Sunset:** {sunset}")
    st.markdown(f"**💧 Humidity:** {humidity if humidity is not None else '--'}%")
    st.markdown(f"**💨 AQI (Air Quality):** {aqi if aqi is not None else 'Unavailable'}")

    # 🚗 Driving condition suggestion
    if wind_kph > 30:
        st.warning("🚗 Driving Conditions: Risky ⚠️")
    else:
        st.success("🚗 Driving Conditions: Clear ✅")

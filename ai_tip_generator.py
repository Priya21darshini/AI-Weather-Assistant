def generate_weather_tip(city, weather, temp):
    weather = weather.lower()
    if "rain" in weather:
        return "🌧️ Don’t forget your umbrella today!"
    elif "sun" in weather or "clear" in weather:
        return "☀️ Wear sunglasses and drink water!"
    elif "cloud" in weather:
        return "☁️ A calm day! Perfect for a walk!"
    elif "storm" in weather:
        return "⛈️ Stay indoors and avoid travel!"
    elif "fog" in weather or "mist" in weather:
        return "🌫️ Drive carefully, visibility is low."
    else:
        return "💡 Stay safe and check the forecast before heading out!"

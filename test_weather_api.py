import requests

def get_weather(city):
    api_key = "6de8a3bf1d39409b9f782820251507"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather = data['current']['condition']['text']
        temp = data['current']['temp_c']
        print("✅ Weather API is working!")
        print(f"Weather in {city}: {weather}, {temp}°C")
    else:
        print("❌ Something went wrong.")
        print(f"Status Code: {response.status_code}")
        print(response.text)

# Run the test
get_weather("Lucknow")

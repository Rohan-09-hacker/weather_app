import requests
import geocoder

# Replace this with your actual OpenWeatherMap API key
API_KEY = "f8c1bd24ee98a71d811c64cc27e0ad7e"

def get_user_location():
    """Detects the user's current city based on their IP address."""
    try:
        # Fetches location data using IP geolocation
        g = geocoder.ip('me')
        if g.city:
            return g.city
        return "Bangalore"  # Fallback city if IP lookup fails
    except Exception:
        return "Bangalore"

def get_weather_data(city):
    """Fetches real-time weather data for a given city from OpenWeatherMap."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    # We pass the city, the API key, and 'metric' to get temperatures in Celsius
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric' 
    }
    
    try:
        response = requests.get(base_url, params=params)
        # If the request was successful (Status Code 200)
        if response.status_code == 200:
            data = response.json()
            weather_profile = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].title()
            }
            return weather_profile
        else:
            print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Quick Test Run ---
if __name__ == "__main__":
    print("🛰️ Detecting your location...")
    current_city = get_user_location()
    print(f"📍 Detected City: {current_city}\n")
    
    print(f"🌦️ Fetching weather data for {current_city}...")
    weather = get_weather_data(current_city)
    
    if weather:
        print("-" * 30)
        print(f"City:        {weather['city']}")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Humidity:    {weather['humidity']}%")
        print(f"Condition:   {weather['description']}")
        print("-" * 30)
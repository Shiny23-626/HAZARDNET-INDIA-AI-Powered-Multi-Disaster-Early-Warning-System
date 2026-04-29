import requests

# Replace with your real OpenWeather API key
API_KEY = "YOUR_API_KEY"


def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return None

        weather_info = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }

        return weather_info

    except Exception:
        return None


def predict_hazard(temp, humidity, wind):
    if temp > 40:
        return "High Heatwave Risk"
    elif humidity > 85 and temp < 35:
        return "Flood Risk"
    elif wind > 15:
        return "Storm Risk"
    else:
        return "No Major Hazard"


def get_full_prediction(city):
    data = get_weather_data(city)

    if data is None:
        return None

    hazard = predict_hazard(
        data["temperature"],
        data["humidity"],
        data["wind_speed"]
    )

    return {
        "city": city,
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "wind": data["wind_speed"],
        "description": data["description"],
        "hazard": hazard
    }
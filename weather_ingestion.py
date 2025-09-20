import requests
import psycopg2
from datetime import datetime
from config import API_KEY, CITIES, DB_CONFIG

def fetch_weather(city):
    """Fetch current weather data for a city."""
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        data = response.json()
        if data.get("main"):
            return {
                "city": city,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "fetched_at": datetime.now()
            }
        else:
            print(f"Error fetching data for {city}: {data.get('message')}")
            return None
    except Exception as e:
        print(f"Request error for {city}: {e}")
        return None

def store_weather(data):
    """Store weather data in PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO weather_data (city, temperature, humidity, weather_description, wind_speed, fetched_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data["city"], data["temperature"], data["humidity"],
            data["description"], data["wind_speed"], data["fetched_at"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Data for {data['city']} inserted successfully!")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    for city in CITIES:
        weather_data = fetch_weather(city)
        if weather_data:
            store_weather(weather_data)

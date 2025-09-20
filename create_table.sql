
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature REAL,
    humidity INTEGER,
    weather_description VARCHAR(100),
    wind_speed REAL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

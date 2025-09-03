"""
Configuration file for smart energy and weather dashboard
"""

# Base URL for the weather API
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

"""
Multiple locations for comparison
Keys are city names, values are lat/lon pairs
"""
LOCATIONS = {
    "Kaduna": {"latitude": 10.5105, "longitude": 7.4165},
    "Lagos": {"latitude": 6.5244, "longitude": 3.3792},
    "Abuja": {"latitude": 9.0765, "longitude": 7.3986},
    }

# Weather parameters we want from the API
WEATHER_PARAMS = {
    "hourly": ["temperature_2m", "windspeed_10m"],
    }

# Number of hours to fetch (24 = one day)
FORECAST_HOURS = 24

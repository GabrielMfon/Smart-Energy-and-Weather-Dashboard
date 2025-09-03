import requests
import matplotlib.pyplot as plt
import pygal
from pygal.style import CleanStyle
from datetime import datetime
import random
import config

# ------------------
# Fetch Weather Data
# ------------------
def fetch_weather(city, coords):
    """
    Fetch hourly weather data from Open-Meteo API for a given city
    Returns dict with time, temperature, and windspeed
    """
    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "hourly": ",".join(config.WEATHER_PARAMS["hourly"]),
        "forecast_days": 1, # today only
        }

    try:
        response = requests.get(config.WEATHER_API_URL, params=params,
                                timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None
    
    data = response.json()
    return data["hourly"]

# ----------------------
# Simulate Energy Demand
# ----------------------
def simulate_energy_demand(temperatures, windspeed):
    """
    Improved synthetic energy demand model.
    Assumptions:
      - Higher temperatures -> higher cooling demand
      - Low windspeed -> higher demand (less natural ventilation)
      - Adds random variation
    """
    demand = []
    for temp, wind in zip(temperatures, windspeed):
        base = 50 # baseline load (MW)
        temp_effect = 0.9 * temp
        wind_effect = -0.3 * wind # higher wind reduces demand slightly
        noise = random.uniform(-3, 3) # randomness
        demand.append(base + temp_effect + wind_effect + noise)
    return demand

# --------------------------
# Visualization (Matplotlib)
# --------------------------
def plot_with_matplotlib(city_data):
    """
    Create scientific plots of energy and weather for multiple cities
    """
    plt.figure(figsize=(12, 7))

    for city, data in city_data.items():
        plt.plot(
            data["times"], data["demand"],
            label=f"{city} Energy Demand (MW)"
            )
        plt.plot(
            data["times"], data["temperatures"],
            label=f"{city} Temperature (°C)", linestyle="--"
            )

    plt.title("Energy Demand vs. Temperature Across Cities")
    plt.xlabel("Hour of Day")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("energy_weather_chart.png")
    plt.show()

# ---------------------
# Visualization (Pygal)
# ---------------------
def plot_with_pygal(city_data):
    """
    Create interactive line chart with Pygal for multiple cities
    """
    line_chart = pygal.Line(style=CleanStyle, show_legend=True,
                            x_label_rotation=20)
    line_chart.title = "Interactive Energy Demand vs. Temperature Across Cities"

    # Assume all cities share the same timestamps
    sample_times = next(iter(city_data.values()))["times"]
    line_chart.x_labels = [t.strftime("%H:%M") for t in sample_times]

    for city, data in city_data.items():
        line_chart.add(f"{city} Temp (°C)", data["temperatures"])
        line_chart.add(f"{city} Demand (MW)", data["demand"])

    line_chart.render_to_file("energy_weather_chart.svg")
    print("Interactive chart saved as 'energy_weather_chart.svg'")

# -------------
# Main Pipeline
# -------------
def main():
    city_data = {}

    for city, coords in config.LOCATIONS.items():
        weather_data = fetch_weather(city, coords)
        if not weather_data:
            continue

        # Parse times into datetime objects
        times = [datetime.fromisoformat(t) for t in weather_data["time"]
                 [:config.FORECAST_HOURS]]
        temperatures = weather_data["temperature_2m"][:config.FORECAST_HOURS]
        windspeed = weather_data["windspeed_10m"][:config.FORECAST_HOURS]

        # Simulate energy demand
        demand = simulate_energy_demand(temperatures, windspeed)

        # Store processed data
        city_data[city] = {
            "times": times,
            "temperatures": temperatures,
            "windspeed": windspeed,
            "demand": demand,
            }
    if city_data:
        plot_with_matplotlib(city_data)
        plot_with_pygal(city_data)

if __name__ == "__main__":
    main()

# Smart Energy & Weather Dashboard

##  Project Overview
This project combines **weather data** with **synthetic energy demand modeling** to explore how temperature and windspeed influence power consumption.  
It was inspired by my learning journey through *Python Crash Course* by Eric Matthes.

##  Features
- Fetches real-time weather data from the [Open-Meteo API](https://open-meteo.com/).
- Simulates realistic energy demand based on temperature, windspeed, and random variations.
- Supports multiple cities (Kaduna, Lagos, Abuja by default).
- Visualizes results with:
  - **Matplotlib** (scientific static plots).
  - **Pygal** (interactive SVG charts).
- Handles API errors gracefully and uses datetime objects for professional labeling.

##  Tech Stack
- Python
- Requests (API fetching)
- Matplotlib (data visualization)
- Pygal (interactive visualization)
- Random & Datetime (simulation and time parsing)

##  Example Output
- Energy demand rising with temperature in hot cities.
- Comparison of Kaduna, Lagos, Abuja demand profiles.
- Interactive charts saved as `.svg` and static charts as `.png`.

##  How to Run
1. Clone this repo
2. Install dependencies:
   ```bash
   pip install requests matplotlib pygal

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

# Function to fetch coordinates (latitude, longitude) using Open-Meteo's geocoding API
def get_coordinates(city):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        response = requests.get(url)
        data = response.json()
        if "results" in data:
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
            return lat, lon
        else:
            return None
    except:
        return None

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    unit = unit_choice.get()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    coords = get_coordinates(city)
    if not coords:
        messagebox.showerror("Error", "City not found.")
        return

    lat, lon = coords

    # Choose temperature unit
    temp_unit = "celsius" if unit == "Celsius" else "fahrenheit"

    # Open-Meteo API for current and forecast
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode"
           f"&timezone=auto&temperature_unit={temp_unit}")

    try:
        response = requests.get(url)
        data = response.json()

        current = data["current_weather"]
        daily = data["daily"]

        result_text.set(
            f"Weather in {city.title()}:\n"
            f"🌡 Current: {current['temperature']}°{unit[0]}\n"
            f"💨 Wind: {current['windspeed']} km/h\n\n"
            f"📅 Forecast:\n"
        )

        for i in range(len(daily["time"])):
            date = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a, %d %b")
            result_text.set(result_text.get() +
                            f"{date}: {daily['temperature_2m_min'][i]}° / {daily['temperature_2m_max'][i]}° {unit[0]}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch weather: {e}")


# --- UI Setup ---
root = tk.Tk()
root.title("Weather App 🌦")
root.geometry("400x500")
root.resizable(False, False)

# City input
tk.Label(root, text="Enter City:", font=("Arial", 12)).pack(pady=5)
city_entry = tk.Entry(root, font=("Arial", 12), justify="center")
city_entry.pack(pady=5)

# Unit selection
unit_choice = ttk.Combobox(root, values=["Celsius", "Fahrenheit"], state="readonly")
unit_choice.set("Celsius")
unit_choice.pack(pady=5)

# Search button
tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12), bg="lightblue").pack(pady=10)

# Result display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", font=("Consolas", 11))
result_label.pack(pady=10)

root.mainloop()

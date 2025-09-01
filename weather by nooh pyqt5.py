import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather App 🌤️")
        self.setGeometry(200, 200, 350, 250)
        self.setStyleSheet("background-color: #2E3440; color: white;")

        layout = QVBoxLayout()

        self.title = QLabel("🌍 Enter City Name")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Type city name (e.g., London)")
        self.city_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #88C0D0;")
        layout.addWidget(self.city_input)

        self.search_btn = QPushButton("Get Weather")
        self.search_btn.setStyleSheet("padding: 8px; background: #88C0D0; color: black; font-weight: bold; border-radius: 5px;")
        self.search_btn.clicked.connect(self.get_weather)
        layout.addWidget(self.search_btn)

        self.result = QLabel("")
        self.result.setFont(QFont("Arial", 12))
        self.result.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result)

        self.setLayout(layout)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name!")
            return

        # Use Open-Meteo geocoding API to get lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_data = requests.get(geo_url).json()

        if "results" not in geo_data:
            QMessageBox.warning(self, "Error", "City not found!")
            return

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # Fetch weather data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()

        if "current_weather" in weather_data:
            temp = weather_data["current_weather"]["temperature"]
            wind = weather_data["current_weather"]["windspeed"]
            self.result.setText(f"🌡️ Temp: {temp}°C\n💨 Wind: {wind} km/h")
        else:
            QMessageBox.warning(self, "Error", "Weather data not available.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

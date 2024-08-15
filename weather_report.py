import requests
import matplotlib.pyplot as plt
from urllib.parse import quote

# Example using OpenWeatherMap API (replace with your API and keys)
api_key = '0d2d3cf3f33f90701a4a0a11fbc47400'
city = input("Enter city name : ")
encoded_city=quote(city)
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

# Fetching data from API
response = requests.get(url)
data = response.json()
print(data)
temperature = data.get('main', {}).get('temp')
if response.status_code == 200:

    data = response.json()
    temperature = data.get('main', {}).get('temp')
    if temperature is not None:
        print(f"Current temperature in {city}: {temperature}°C")
    else:
        print(f"Temperature data not available for {city}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

# Extracting relevant weather information
temperature = data['main']['temp']
humidity = data['main']['humidity']
wind_speed = data['wind']['speed']

# Displaying current weather information
print(f'Current weather in {city}:')
print(f'Temperature: {temperature}°C')
print(f'Humidity: {humidity}%')
print(f'Wind Speed: {wind_speed} m/s')

# Example of using Matplotlib to create a simple chart
labels = ['Temperature', 'Humidity', 'Wind Speed']
values = [temperature, humidity, wind_speed]

plt.figure(figsize=(8, 6))
plt.bar(labels, values, color=['blue', 'green', 'orange'])
plt.title(f'Current Weather in {city}')
plt.ylabel('Value')
plt.show()


import flet as ft
import requests
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import os
import base64
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv("API_ENDPOINT")

def main(page: ft.Page):
    page.title = "DynamoDB Data Visualization"

    def fetch_data():
        try:
            response = requests.get(API_ENDPOINT)
            response.raise_for_status()
            data = response.json()
            print("Fetched data:", data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        except json.JSONDecodeError:
            print("Error: Response is not valid JSON")
            return []

    data = fetch_data()
    
    if isinstance(data, dict) and "Items" in data:
        data = data["Items"]

    # Extract data for plotting
    timestamps = [item['timestamp'] for item in data if 'timestamp' in item]
    temperatures = [item['temperature'] for item in data if 'temperature' in item]
    humidities = [item['humidity'] for item in data if 'humidity' in item]

    # Generate the plot
    plt.figure()
    plt.plot(timestamps, temperatures, label="Temperature", color="red")
    plt.plot(timestamps, humidities, label="Humidity", color="blue")
    plt.xlabel("Timestamp")
    plt.ylabel("Readings")
    plt.title("Temperature and Humidity Over Time")
    plt.legend()

    # Save plot to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert the plot image to base64 and create a data URI
    image_data = base64.b64encode(buffer.read()).decode('utf-8')
    img_src = f"data:image/png;base64,{image_data}"
    
    # Create and add image to the page
    img = ft.Image(src=img_src, width=500, height=400)
    page.add(img)

ft.app(target=main)
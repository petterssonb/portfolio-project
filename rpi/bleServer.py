import json
import asyncio
from bleak import BleakClient, BleakScanner
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

CHARACTERISTIC_UUID = os.getenv("CHARACTERISTIC_UUID")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
CA_PATH = os.getenv("AWS_ROOT_CA")
CERT_PATH = os.getenv("AWS_CERT")
KEY_PATH = os.getenv("AWS_PRIVATE_KEY")
AWS_TOPIC = os.getenv("AWS_TOPIC")
SHADOW_TOPIC = os.getenv("SHADOW_TOPIC")

aws_client = AWSIoTMQTTClient("OfficeRpi")
aws_client.configureEndpoint(AWS_ENDPOINT, 8883)
aws_client.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

aws_client.configureAutoReconnectBackoffTime(1, 32, 20)
aws_client.configureOfflinePublishQueueing(-1)
aws_client.configureDrainingFrequency(2)
aws_client.configureConnectDisconnectTimeout(10)
aws_client.configureMQTTOperationTimeout(5)
aws_client.connect()

esp32_address = None
esp32_found = False

def update_shadow(state):
    """Update the device shadow with the latest state."""
    shadow_payload = {
        "state": {
            "reported": state
        }
    }
    aws_client.publish(SHADOW_TOPIC, json.dumps(shadow_payload), 1)
    print("Device shadow updated with:", state)


def notification_handler(sender, data):
    """Handles data received from the ESP32."""
    json_data = data.decode('utf-8')
    print(f"Received data from ESP32: {json_data}")

    payload = json.loads(json_data)
    payload["status"] = "online"

    aws_client.publish(AWS_TOPIC, json.dumps(payload), 1)
    print("Data with status sent to AWS IoT Core:", payload)

    update_shadow({"last_data_received": json_data})


async def find_esp32():
    """Scans for ESP32 and sends offline status while not found."""
    global esp32_address, esp32_found

    last_offline_sent = datetime.now()

    while not esp32_found:
        print("Scanning for ESP32...")
        devices = await BleakScanner.discover()

        if datetime.now() - last_offline_sent >= timedelta(seconds=15):
            payload = {
                "temperature": None,
                "humidity": None,
                "macAddress": None,
                "status": "offline",
            }
            aws_client.publish(AWS_TOPIC, json.dumps(payload), 1)
            print("Offline status sent to AWS IoT Core.")
            last_offline_sent = datetime.now()

        for device in devices:
            if device.name and "ESP32_Sensor" in device.name:
                esp32_address = device.address
                esp32_found = True
                print(f"Found ESP32 with address: {esp32_address}")
                return

        await asyncio.sleep(5)


async def monitor_connection(client):
    """Monitors the connection with the ESP32."""
    global esp32_found, esp32_address
    try:
        while client.is_connected:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"ESP32 disconnected: {e}")
        esp32_found = False
        esp32_address = None
        print("Restarting scan for ESP32...")
        await find_esp32()


async def main():
    global esp32_address, esp32_found
    while True:
        await find_esp32()
        async with BleakClient(esp32_address) as client:
            print(f"Connected to ESP32 with MAC address: {esp32_address}")
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            await monitor_connection(client)


if __name__ == "__main__":
    asyncio.run(main())
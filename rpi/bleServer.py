import json
import asyncio
from bleak import BleakClient, BleakScanner
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
from dotenv import load_dotenv

load_dotenv()

CHARACTERISTIC_UUID = os.getenv("CHARACTERISTIC_UUID")
SERVICE_UUID = os.getenv("SERVICE_UUID")
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
    json_data = data.decode('utf-8')
    print(f"Received data from ESP32: {json_data}")

    aws_client.publish(AWS_TOPIC, json_data, 1)
    print("Data sent to AWS IoT Core on topic", AWS_TOPIC)

    update_shadow({"last_data_received": json_data})

async def main():
    devices = await BleakScanner.discover()
    esp32_address = None

    for device in devices:
        if device.name and "ESP32_Sensor" in device.name:
            esp32_address = device.address
            print(f"Found ESP32 with address: {esp32_address}")
            break

    if not esp32_address:
        print("ESP32 not found")
        return

    async with BleakClient(esp32_address) as client:
        print("Connected to ESP32")
        
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
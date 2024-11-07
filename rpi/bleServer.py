import asyncio
from bleak import BleakClient, BleakScanner
import os
from dotenv import load_dotenv

load_dotenv()

CHARACTERISTIC_UUID = os.getenv("CHARACTERISTIC_UUID")
SERVICE_UUID = os.getenv("SERVICE_UUID")

def notification_handler(sender, data):
    print(f"Received data from ESP32: {data.decode('utf-8')}")

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
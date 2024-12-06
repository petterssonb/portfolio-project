#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>
#include "DHT.h"
#include "config.h"

#define DHTPIN 27
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define GREEN_LED 25
#define BLUE_LED 26

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;
String macAddress;

bool isBlinkingBlue = true;

class MyCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        deviceConnected = true;
        isBlinkingBlue = false;
        digitalWrite(BLUE_LED, HIGH);
    }

    void onDisconnect(BLEServer* pServer) {
        deviceConnected = false;
        isBlinkingBlue = true;
        digitalWrite(BLUE_LED, LOW);
    }
};

void setup() {
    Serial.begin(115200);
    dht.begin();

    pinMode(BLUE_LED, OUTPUT);
    pinMode(GREEN_LED, OUTPUT);

    BLEDevice::init("ESP32_Sensor");
    macAddress = BLEDevice::getAddress().toString().c_str();
    Serial.print("Device MAC Address: ");
    Serial.println(macAddress);

    BLEServer *pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyCallbacks());

    BLEService *pService = pServer->createService(SERVICE_UUID);
    pCharacteristic = pService->createCharacteristic(
                        CHARACTERISTIC_UUID,
                        BLECharacteristic::PROPERTY_NOTIFY
                      );
    pCharacteristic->addDescriptor(new BLE2902());

    pService->start();
    BLEAdvertising *pAdvertising = pServer->getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->start();
    Serial.println("Bluetooth initialized and advertising.");
}

void loop() {
    if (isBlinkingBlue) {
        digitalWrite(BLUE_LED, HIGH);
        delay(200);
        digitalWrite(BLUE_LED, LOW);
        delay(200);
    }

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Failed to read from DHT sensor!");
        return;
    }

    String jsonData = "{\"temperature\": " + String(temperature) + 
                  ", \"humidity\": " + String(humidity) + 
                  ", \"macAddress\": \"" + macAddress + "\"" + 
                  ", \"status\": \"online\"}";
    
    if (deviceConnected) {
        pCharacteristic->setValue(jsonData.c_str());
        pCharacteristic->notify();
        Serial.println("Data sent via BLE: " + jsonData);

        for (int i = 0; i < 4; i++) {
            digitalWrite(GREEN_LED, HIGH);
            delay(200);
            digitalWrite(GREEN_LED, LOW);
            delay(200);
        }
    } else {
        Serial.println("BLE not connected.");
    }
    delay(60000);
}
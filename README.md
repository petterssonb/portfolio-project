# portfolio-project

wished structure:

Protocol	Security Measures
ESP32 -> Raspberry Pi	BLE	Bluetooth pairing and authentication
Raspberry Pi -> AWS IoT Core	MQTT over TLS	AWS IoT certificate-based authentication
AWS IoT Core -> DynamoDB	IoT Rule	Role-based permissions
DynamoDB -> Grafana (Frontend)

use case:

 - Industrial IoT (IIoT): Enables real-time monitoring of environmental conditions in warehouses, factories, and other industrial settings, where temperature and humidity control are crucial for safety and equipment preservation.
 - Data-Driven Insights and Alerts: Leveraging AWS services and Grafana allows for data analysis, anomaly detection, and alert configurations based on environmental conditions, enhancing decision-making and preventive maintenance.
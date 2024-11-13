# portfolio-project

wished structure:

	1.	ESP32 -> Raspberry Pi (via Bluetooth):
	•	The ESP32 collects sensor data and sends it to the Raspberry Pi over Bluetooth.
	2.	Raspberry Pi -> AWS IoT Core:
	•	The Raspberry Pi acts as an intermediary, publishing the data to AWS IoT Core, where it’s securely ingested into AWS.
	3.	AWS IoT Core -> DynamoDB:
	•	IoT Core rules or direct data processing functions can route data to DynamoDB, storing it in a structured way for further processing.
	4.	DynamoDB -> Lambda:
	5.	Lambda -> Grafana:
	•	A DynamoDB stream triggers the Lambda function whenever new data is added. This Lambda function retrieves the new entries, processes them if needed, and then forwards them to Grafana.
	•	The Lambda function sends the processed data to Grafana, where it’s visualized in near real-time.

Key Benefits of This Architecture:

	•	Modular and Scalable: Each component (ESP32, RPi, AWS IoT Core, DynamoDB, Lambda) can be scaled or modified independently.
	•	Reliability and Real-Time Data Flow: With AWS IoT Core and DynamoDB streams, data is quickly moved to Grafana.
	•	Security and Access Control: Using AWS services helps ensure secure and controlled data transfer.

use case:

 - Industrial IoT (IIoT): Enables real-time monitoring of environmental conditions in warehouses, factories, and other industrial settings, where temperature and humidity control are crucial for safety and equipment preservation.
 - Data-Driven Insights and Alerts: Leveraging AWS services and Grafana allows for data analysis, anomaly detection, and alert configurations based on environmental conditions, enhancing decision-making and preventive maintenance.
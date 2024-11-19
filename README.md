## Portfolio Project: IoT Data Pipeline with ESP32, Raspberry Pi, and AWS

This project demonstrates the implementation of a scalable and secure IoT data pipeline, focusing on real-time environmental monitoring and visualization. The architecture integrates an ESP32, Raspberry Pi, AWS IoT Core, DynamoDB, Lambda, and Grafana, enabling real-time data flow, analysis, and visualization.

### Table of Contents

1.  Architecture Overview

2.	Use Case

3.	Project Components

4.	Key Benefits

5.	Setup Instructions

6.	How It Works

7.	Future Improvements

## Architecture Overview

### Data Flow:

1.	ESP32 → Raspberry Pi (via Bluetooth):
   -	The ESP32 collects environmental data (e.g., temperature, humidity) from sensors and transmits it to the Raspberry Pi using Bluetooth.

2.	Raspberry Pi → AWS IoT Core:
  - The Raspberry Pi processes incoming data and publishes it to AWS IoT Core for secure ingestion.

3.	AWS IoT Core → DynamoDB:
  -	IoT Core rules or processing functions route the data to DynamoDB for structured storage.

4.	DynamoDB → Lambda:
 -	DynamoDB Streams trigger a Lambda function to process and format the data.
	
5.	Lambda → Grafana:
 - The processed data is sent to Grafana for real-time visualization and analytics.

### Use Case

This project serves Industrial IoT (IIoT) scenarios, specifically for:
	
 - Real-Time Monitoring: Track environmental conditions such as temperature and humidity in warehouses, factories, and industrial facilities.
	
 - Data-Driven Insights: Enable anomaly detection and alert configurations for proactive decision-making and preventive maintenance.

### Project Components

1.	ESP32:
 - Collects sensor data and sends it to the Raspberry Pi via Bluetooth.

2.	Raspberry Pi:
 - Acts as an intermediary between the ESP32 and AWS IoT Core.
 - Runs a Bluetooth service and publishes sensor data to AWS.

3.	AWS IoT Core:
 - Provides secure ingestion and routing of data from the Raspberry Pi to AWS services.

4.	DynamoDB:
 - Stores sensor data in a structured format, enabling further processing.

5.	AWS Lambda:
 - Processes data from DynamoDB and prepares it for visualization.

6.	Grafana:
 - Visualizes processed data in near real-time.

### Key Benefits

  ### Modular and Scalable:
 - Independent components can be scaled or modified as needed.
 - Real-Time Data Flow:
 - Ensures quick processing and visualization of sensor data.
 - Secure and Reliable:
 - Utilizes AWS services for secure data transfer and controlled access.

### Setup Instructions

Prerequisites

- ***Hardware***:
 - ESP32 with sensors
 - Raspberry Pi
 - AWS Services:
 - AWS IoT Core, DynamoDB, Lambda
 - IAM roles with appropriate permissions
 - Visualization Tools:
 - Grafana with AWS Data Source Plugin

Steps:

 1.	ESP32 Configuration:
 - Connect sensors to the ESP32.
 - Configure Bluetooth communication.
  
2.	Raspberry Pi Setup:
 - Install necessary libraries (pybluez, submodules).
 - Set up a script to receive Bluetooth data and publish it to AWS IoT Core.

3.	AWS IoT Core:
 - Create a Thing and configure certificates.
 - Set up IoT Core rules to route data to DynamoDB.

4.	DynamoDB Table:
 - Create a table to store sensor data with attributes like timestamp, temperature, and humidity.

5.	AWS Lambda:
 - Write a function to process DynamoDB and forward data to Grafana.

6.	Grafana Dashboard:
 - Configure a Grafana dashboard to visualize data using AWS CloudWatch or other data sources.

### How It Works

 1.	The ESP32 collects sensor readings (e.g., temperature, humidity) and sends them to the Raspberry Pi over Bluetooth.

 2.	The Raspberry Pi publishes the data to AWS IoT Core using MQTTS.

 3.	AWS IoT Core routes the data to a DynamoDB table using IoT rules.
 
 4.	Lambda trigger DynamoDB contents

 5.	The processed data is sent to Grafana for visualization in near real-time.

### Future Improvements

 - Add support for more sensors and data types.
 - Incorporate AWS Machine Learning services for predictive analytics.
 - Improve fault tolerance and redundancy using AWS IoT SiteWise or similar services.

### License

This project is licensed under the ***MIT License***. See the ***LICENSE*** file for details.

### Contributions

Contributions are welcome! Please open an issue or submit a pull request for enhancements or bug fixes.

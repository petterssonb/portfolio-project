# portfolio-project

wished structure:

Protocol	Security Measures
ESP32 -> Raspberry Pi	BLE	Bluetooth pairing and authentication
Raspberry Pi -> AWS IoT Core	MQTT over TLS	AWS IoT certificate-based authentication
AWS IoT Core -> DynamoDB	IoT Rule	Role-based permissions
DynamoDB -> Amplify (Frontend)	AppSync or Amplify DataStore	Cognito User Pool or IAM-based permissions

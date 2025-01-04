#include <ArduinoBLE.h>
// #include <math.h>
#include "Arduino_BMI270_BMM150.h"

// float gyro[3];
// float acc[3];
float x;
float y;
float z;
String vals;
// float mag[3];

// Create a BLE Service 
BLEService serviceAcc("180B");
  BLECharacteristic charAccx("2B51", BLERead | BLENotify, 10); 
  BLECharacteristic charAccy("2B52", BLERead | BLENotify, 10); 

BLEService serviceFlag("180D");
  BLECharacteristic charFlag("2A57", BLERead | BLEWrite | BLENotify, 20);

//function prototypes
void details(BLEDevice central);
void writeVal(BLECharacteristic characterstic, int val);
String floatToString(float value1, float value2);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Start BLE module
  if (!BLE.begin()) {
    Serial.println("FAILED TO START BLE!");
    while (1);
  }
  //Begin IMU
  if (!IMU.begin()) {
    Serial.println("FAILED TO INTITIALIZE IMU!");
    while (1);
  }

  // Set BLE device properties
  BLE.setLocalName("Nano33BLE_SingleValue");
  BLE.setAdvertisedService(serviceAcc);

  // Add the characteristic to the service
  serviceAcc.addCharacteristic(charAccx);
  serviceAcc.addCharacteristic(charAccy);
  serviceFlag.addCharacteristic(charFlag);
  
  // Add the service to the BLE stack
  BLE.addService(serviceAcc);
  BLE.addService(serviceFlag);

  // Start advertising
  BLE.advertise();
  Serial.println("BLE device is now advertising!");

}
 
void loop() {
  // Wait for a BLE central to connect
BLEDevice central = BLE.central();
  if (central) {
    //print details
    details(central);

    //wait until write from client
    while(!charFlag.written() && central.connected()){
      Serial.println("Waiting for Conformation.");
      delay(100);
    }

    if(central.connected()){Serial.print("Connection Confirmed.");}

    while (central.connected()) {

      //  Read Values form sensor
      if ( IMU.accelerationAvailable() ) {
        IMU.readAcceleration(x, y, z);

        // String floatString = String(x, 2) + "_" + String(y, 2);
        // char str[floatString.length() + 1];
        // floatString.toCharArray(str, sizeof(str));
        
        // writeVal(charAccx,  str);
        charAccx.writeValue( (byte*)&x, sizeof(float) );
        charAccy.writeValue( (byte*)&y, sizeof(float) );
        // writeVal(charAccy,  inty);
      }
      //delay(100);
    }

    if(!central.connected()){
      Serial.print("Disconnected");
    }
  }
  
}

//write int value to characterstic
void writeVal(BLECharacteristic characterstic, char* value){
  // characterstic.writeValue( (int16_t)value );
  characterstic.writeValue(value, sizeof(value));
  Serial.print("Value sent: ");
  Serial.println(value);
}

void details(BLEDevice central){
  Serial.print("(SELF) Server : ");
  Serial.println(BLE.address());
  Serial.print("Connected to central: ");
  Serial.println(central.address());
}

String floatToString(float value1, float value2) {
  // Convert the float values to strings and combine them with an underscore
  String result = String(value1, 2) + "_" + String(value2, 2); // You can set the decimal precision (2 in this case)
  return result;
}

// // Function prototype: angles(gyro: arr[3], acc: arr[3], mag: arr[3])
// float* angles(float gyro[3], float acc[3], float mag[3]) {
//   float* result = new float[3];  // Array to hold the output: [pitch, roll, yaw]
  
//   // Accelerometer calculations for pitch and roll
//   float pitch = atan2(acc[1], sqrt(acc[0] * acc[0] + acc[2] * acc[2])) * 180.0 / PI;
//   float roll = atan2(-acc[0], acc[2]) * 180.0 / PI;
  
//   // Magnetometer calculation for yaw (corrected for pitch and roll)
//   float magX = mag[0] * cos(pitch) + mag[1] * sin(roll) * sin(pitch) + mag[2] * cos(roll) * sin(pitch);
//   float magY = mag[1] * cos(roll) - mag[2] * sin(roll);
//   float yaw = atan2(magY, magX) * 180.0 / PI;
  
//   // Store the results in the output array
//   result[0] = pitch;
//   result[1] = roll;
//   result[2] = yaw;
  
//   return result;
// }

// String floatToStringConcat(float num1, float num2, float num3) {
//   return String(num1, 2) + "_" + String(num2, 2) + "_" + String(num3, 2)
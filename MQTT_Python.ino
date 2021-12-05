#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"

#include <SPI.h>
#include <MFRC522.h>

DHTesp dht;

constexpr uint8_t RST_PIN = D3;     // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = D4;     // Configurable, see typical pin layout above
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
String tag;

float lightValue;

const char* ssid = "Please_Let_Me_See_My_Kids";
const char* password = "sussybaka";

const char* mqtt_server = "192.168.1.100";

WiFiClient vanieriot;
PubSubClient client(vanieriot);


void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }

  if(topic=="IoTlab/LEDLight"){
    if (messagein == "ON"){
      Serial.println("Light is ON");
      digitalWrite(D8, HIGH);
    }else if (messagein == "OFF") {
      Serial.println("Light is OFF");
      digitalWrite(D8, LOW);
    }else{
      digitalWrite(D8, HIGH);
      delay(200);
      digitalWrite(D8, LOW);
      delay(200);
      digitalWrite(D8, HIGH);
      delay(200);
      digitalWrite(D8, LOW);
    }
  }

  if(topic=="IoTlab/Fan"){
    if (messagein == "ON"){
      Serial.println("Fan is ON");
      digitalWrite(D1, HIGH);
    }else if (messagein == "OFF") {
      Serial.println("Fan is OFF");
      digitalWrite(D1, LOW);
    }else{
      digitalWrite(D1, HIGH);
      delay(200);
      digitalWrite(D1, LOW);
      delay(200);
      digitalWrite(D1, HIGH);
      delay(200);
      digitalWrite(D1, LOW);
    }
  }

  if(topic=="IoTlab/ThresholdTemp"){
    if (messagein == "ON"){
      Serial.println("Threshold Temp is ON");
      digitalWrite(D6, HIGH);
    }else if (messagein == "OFF") {
      Serial.println("Threshold Temp is OFF");
      digitalWrite(D6, LOW);
    }else{
      digitalWrite(D6, HIGH);
      delay(200);
      digitalWrite(D6, LOW);
      delay(200);
      digitalWrite(D6, HIGH);
      delay(200);
      digitalWrite(D6, LOW);
    }
  }

  if(topic=="IoTlab/ThresholdLight"){
    if (messagein == "ON"){
      Serial.println("Threshold Light is ON");
      digitalWrite(D7, HIGH);
    }else if (messagein == "OFF") {
      Serial.println("Threshold Light is OFF");
      digitalWrite(D7, LOW);
    }else{
      digitalWrite(D7, HIGH);
      delay(200);
      digitalWrite(D7, LOW);
      delay(200);
      digitalWrite(D7, HIGH);
      delay(200);
      digitalWrite(D7, LOW);
    }
  }
  
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
 
    
   //  String clientId = "ESP8266Client-";
   // clientId += String(random(0xffff), HEX);
    // Attempt to connect
   // if (client.connect(clientId.c_str())) {
           if (client.connect("vanieriot")) {

      Serial.println("connected");  
      client.subscribe("IoTlab/LEDLight");
      client.subscribe("IoTlab/Fan");
      client.subscribe("IoTlab/ThresholdTemp");
      client.subscribe("IoTlab/ThresholdLight");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {
  
  Serial.begin(115200);
  SPI.begin(); // Init SPI bus
  dht.setup(4, DHTesp::DHT11);
  rfid.PCD_Init(); // Init MFRC522
  pinMode(D6, OUTPUT);
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  pinMode(D1, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}

void loop() {
  
  if (!client.connected()) {
    reconnect();
    }
  if(!client.loop())
    client.connect("vanieriot");

  lightValue = float(analogRead(A0)); // read analog input pin 0
  lightValue = (1024 - lightValue)/10;

  char lightArr[8];
  dtostrf(lightValue,6,2,lightArr);
  
  float temp= dht.getTemperature();
  float hum= dht.getHumidity();
    
    char tempArr [8];
    dtostrf(temp,6,2,tempArr);
    char humArr [8];
    dtostrf(hum,6,2,humArr);
      
     client.publish("IoTlab/ESP","Hello IoTlab");
     client.publish("IoTlab/temperature", tempArr);
     client.publish("IoTlab/humidity", humArr);
     client.publish("IoTlab/light", lightArr);
     
     delay(3000);

  }

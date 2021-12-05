#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <SPI.h>
#include <MFRC522.h>

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

  if(topic=="IoTlab/RFIDAccess"){
    if (messagein == "GRANTED"){
      Serial.println("RFID Granted");
//      Green Light ON
      digitalWrite(D1, HIGH);
      delay(1000);
      digitalWrite(D1, LOW);
    }else if (messagein == "DENIED") {
      Serial.println("RFID Denied");
//      Red Light ON
      digitalWrite(D0, HIGH);
      delay(1000);
      digitalWrite(D0, LOW);
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
           if (client.connect("vanieriot2")) {

      Serial.println("connected");
      client.subscribe("IoTlab/RFIDAccess");
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
  rfid.PCD_Init(); // Init MFRC522
  pinMode(D2, OUTPUT);
  pinMode(D1, OUTPUT);
  pinMode(D0, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  
  if (!client.connected()) {
    reconnect();
    }
  if(!client.loop())
    client.connect("vanieriot2");
    
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  if (rfid.PICC_ReadCardSerial()) {
    for (byte i = 0; i < 4; i++) {
      tag += rfid.uid.uidByte[i];
    }
    Serial.println();
    Serial.println(tag);
    digitalWrite(D2, HIGH);
    delay(100);
    digitalWrite(D2, LOW);
    char buf[tag.length() + 1];
    tag.toCharArray(buf, tag.length() + 1);

    Serial.println("Sending tag...");
    client.publish("IoTlab/tag", buf);
    
    tag = "";
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
    delay(2000);
  }

}

#include <ESP8266WiFi.h>
//wifi config
const char* ssid     = "TP-LINK_AF8E";
const char* password = "14783623";

IPAddress static_ip(192,168,0,101); // A
//IPAddress static_ip(192,168,0,102); //B
//IPAddress static_ip(192,168,0,103); //C
IPAddress gateway(192,168,0,1);
IPAddress subnet(255,255,255,0);

//const char* ssid     = "90E";
//const char* password = "";

//host
const uint16_t port = 8081;
//const char* host = "192.168.8.22";
const char* host = "192.168.0.107";

// uhf reader config
unsigned char incomingByte;
void send_(){
  //byte cmd[] = {0xA5, 0x5A, 0x00, 0x08, 0x00, 0x08, 0x0D, 0x0A};
 // byte cmd[] = {0xA5, 0X5A, 0X00, 0X0A, 0X80, 0X00, 0X64, 0XEE, 0X0D, 0X0A};
  byte cmd[] = {0xA5, 0x5A, 0x00, 0x0A, 0x82, 0x00, 0x10, 0x98, 0x0D, 0x0A};
  Serial.write(cmd, sizeof(cmd));
  Serial.printf("\n");
}

// led
#define wifi_led D6

void setup() {
  //led config
  pinMode(wifi_led,OUTPUT);
  //serial config
  Serial.begin(115200);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  //connection
  WiFi.config(static_ip,gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
  delay(500);
  Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi is connected");
  Serial.println(WiFi.localIP());
}


int counter = 0;
void main_(){
  String t;
  WiFiClient client;
  if (client.connect(host,port)){
      digitalWrite(wifi_led, HIGH);
      send_();
      String msg = "";
      while (Serial.available() > 0){
        incomingByte = Serial.read();
        if (incomingByte <= 15){
          t = "0" + String(incomingByte,HEX);
        }
        else{
          t = String(incomingByte,HEX);
        }
        msg += t;
        Serial.print(t);
        Serial.printf(" ");
      } 
      Serial.print(msg);
      client.println(msg);
      Serial.printf("-----\n");
  }
  delay(400);
  client.stop();
//  counter += 1;
//  if (counter == 10){
//    delay(1000);
//    Serial.print("sleep");
//    counter = 0;
//  }
}

void loop() {
  main_();
  
}

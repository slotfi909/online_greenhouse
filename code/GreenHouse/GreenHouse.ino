#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#include <DHT.h>

#ifndef STASSID
#define STASSID "WIFI"
#define STAPSK "PASSWORD"
#endif

----------------------------------- DHT11 -------------------------------

#define DHT_SENSOR_PIN  D7 // The ESP8266 pin D7 connected to DHT11 sensor
#define DHT_SENSOR_TYPE DHT11
DHT dht_sensor(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);

----------------------------------- DHT11 -------------------------------


const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

const int led = 13;
int sensor_pin = A0;
int output_value ;

String txt = "";

void handleRoot() {
  digitalWrite(led, 1);
  server.send(200, "text/plain", txt);

  digitalWrite(led, 0);
  
}

void handlePost() {
  if (server.hasArg("plain") == false) { // Check if body received
    server.send(200, "text/plain", "Body not received");
    return;
  }
  
  String message = "";
  message += server.arg("plain");
  
  String one = "1";
  String zero = "0";
  Serial.println(message);
  if (message==one)
  {
    Serial.println("in this scope");
    digitalWrite(LED_BUILTIN, LOW);
  }
  else if (message == zero)
  {
    Serial.println("in this scope2");
    digitalWrite(LED_BUILTIN, HIGH);
  }
  

}


void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) { message += " " + server.argName(i) + ": " + server.arg(i) + "\n"; }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void setup(void) {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  dht_sensor.begin(); 

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) { Serial.println("MDNS responder started"); }


  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {

  output_value = analogRead(sensor_pin);
  output_value = map(output_value,1024,360,0,100); //450

  float temperature_C = dht_sensor.readTemperature();
    txt = String(temperature_C) + "\n"+ output_value;
    server.handleClient();
    MDNS.update();
    server.on("/", handleRoot);
    server.on("/post", HTTP_POST, handlePost);
    delay(500);
  // }
  
}

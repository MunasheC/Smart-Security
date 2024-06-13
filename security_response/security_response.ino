#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <MusicBuzzer.h>

const char* ssid = "projectJASON";         // Replace with your network SSID
const char* password = "jason142"; // Replace with your network password

AsyncWebServer server(80);
const int buzzerPin = 9;

void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);

  // Set GPIO pin 9 as output
  pinMode(buzzerPin, OUTPUT);
  // digitalWrite(buzzerPin, LOW);  // Initialize LED to be off
  music.init(buzzerPin);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Print ESP32 IP Address
  Serial.println(WiFi.localIP());

  // Route for "/alert_on"
  server.on("/alert_on", HTTP_GET, [](AsyncWebServerRequest *request){
    music.pinkpanther();
    delay(2000);
    request->send(200, "text/plain", "LED is ON");
    Serial.println("Received alert_on command. LED is ON");
  });

  // Route for "/alert_off" to turn off the LED (optional)
  server.on("/alert_off", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(buzzerPin, LOW); // Turn off the LED
    request->send(200, "text/plain", "LED is OFF");
    Serial.println("Received alert_off command. LED is OFF");
  });

  // Start server
  server.begin();
}

void loop(){
  // Nothing to do here, all logic is handled by server events
}

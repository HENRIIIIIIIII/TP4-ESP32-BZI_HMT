#include <WiFi.h>
 
const char* ssid = "ESP_serveur";
const char* password = "12345678";
 
const char* host = "192.168.4.1";  // IP du serveur AP ESP32 Python
const uint16_t port = 1234;
 
const int buttonPin = 0;
bool lastButtonState = HIGH;
 
WiFiClient client;
 
void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
 
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
 
  Serial.print("Connexion au WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connecté!");
}
 
void loop() {
  bool currentButtonState = digitalRead(buttonPin);
 
  if (lastButtonState == HIGH && currentButtonState == LOW) {
    Serial.println("Bouton pressé, envoi demande changement couleur");
 
    if (client.connect(host, port)) {
      client.print("CHANGE");
      client.stop();
      Serial.println("Message envoyé.");
    } else {
      Serial.println("Erreur connexion au serveur.");
    }
    delay(300);  // debounce
  }
 
  lastButtonState = currentButtonState;
  delay(10);
}
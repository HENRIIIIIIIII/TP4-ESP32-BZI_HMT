# TP4-ESP32-BZI_HMT
## ESP32 Mise en route
### Mise à jour des firmeward et installation d'un interperteur phyton
Pour programmer en phyton nous devons utiliser IDE Thonny (comme conseillé dans la donnée), avant même de commencer a tapé du code il faut.
Installer un interperteur phyton sur l'ESP32-S3, voici la marche à suivre :
- il faut tout d'abord débracher l'ESP (important !)
- en bas à gauche nous pouvons configurer le COM d'entrée pour notre ESP32 (COM : interface d'entrée/sortie utilisée pour connecter des périphériques série à un ordinateur)
- appuyer sur le bouton boot et le maintenir tout en branchant sur le pc ce qui va faire apparaitre un nouveau numero de COM dans mon cas le COM9 (voir capture d'écrant).
- puis cliquer sur installer ou mettre jour MicroPython (voir capture d'écrant).
- sur le nouvelle onglet il faut selection le même port COM, cocher la case pour ecraser le progamme une fois flashé et enfin selectionner le type d'appereil et la dernière version (voir capture d'écrant).

![Capture d’écran 2025-05-27 120221](https://github.com/user-attachments/assets/f3a2b64d-13ea-4ee8-8441-b734bda6d39d)

Toutes ces étapes nous ont permis de pouvoir flasher notre programme (l'envoyer à notre ESP) une fois celuit-ci écrit. Nous pouvons enfin crée un fichier main.py et commencer à coder.
### Mise jour pour interpreteur Ardiuno
- Installer VS Code
- Insaller le plug-in PlatformIO sur le site : https://platformio.org/

  ![image](https://github.com/user-attachments/assets/e6e3d23e-6a86-4681-b69d-c1c3ffa13240)
  
- Ouvrir les paramètre et crée un nouveau projet 
  
  ![image](https://github.com/user-attachments/assets/c70aef62-2fac-44b0-94f6-cf572a731679)

- Selectioner le bon modèle la configuration des port ce fait automatiquement 

Pour flasher le programme en Ardiuno il faut
- Il faut maintenir le boutton boot
- appuyer une fois sur reset
- en continuant de maintenir le bouton boot
- il faut build le programme (compiler et 
  
### Explication et stratégie du code 
#### mise en route et verification d'un programme flashé

Pour commencé nous avons verifier le fonctionement de l'appareil grace à un code exemple sur le site : https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/

```
from machine import Pin # importation des classe Pin broches (GPIO) de la carte
from time import sleep  # permet d'utiliser la fonction sleep 
led = Pin(2, Pin.OUT)  # determine les pin d'entrée et de sortie
while True:  # Boucle infinie
  led.value(not led.value()) # lis l'état actuel de la LED (0 ou 1) inverse l'état et réecrit la nouvelle valeur
  sleep(0.5)  # met le programme en pause pendant 0.5 secode pour pouvoir voir la LED à l'oeil nu

```
  
Ce dernier sert à alimenter la PIN n°2 (GPIO 2: broche contrôlable) de notre ESP32, en branchant une LED allons de la PIN n°2 au GND la PIN nommé G sur la carte, la LED clignote. Ce qui veut dire que notre code a été flashé correctement sur l'appareil.
### Explication du fonctionement de la LED RGB WS2812

Selon le datasheet la LED RGB communique via GPIO 48 (General Purpose Input/Output, entrée/sortie) : https://dl.espressif.com/dl/SCH_ESP32-S3-DEVKITC-1_V1_20210312C.pdf
Nous recuperons aussi la réference de la LED ce qui nous permet d'aller à son datasheet et de comprendre son fontionement à la page 8. http://www.normandled.com/upload/202105/SK6812MINI-HS%20LED%20Datasheet.pdf

![image](https://github.com/user-attachments/assets/863adfb6-4316-4e94-a3d6-d4bdee54b486)


Nous comprenons donc qu'une trame de 24 bits est communiqué et que chaque couleur et séparer en 8 partie chaque LED (R/G/B) recupére les information lié à ça couleur.

## Changement de la couleur d'une LED RGB en appuyant sur le boutton boot phyton
Importation de librairi pour les pin, la led et le temps
```
from machine import Pin
from neopixel import NeoPixel
import time

```
LED :
"pin = Pin(48, Pin.OUT)" : Définit la broche GPIO48 en mode sortie pour envoyer des données au NeoPixel
"neo = NeoPixel(pin, 1)" : Crée un objet NeoPixel branché sur pin avec 1 seule LED.
"colors = [(10, 0, 0), (0, 10, 0), (0, 0, 10)]" : Liste des couleurs à afficher (rouge, vert, bleu) sous forme de (R, G, B).
"color_index = 0" : Variable pour garder en mémoire quelle couleur est affichée actuellement.

```
# Initialisation NeoPixel sur GPIO48
pin = Pin(48, Pin.OUT)
neo = NeoPixel(pin, 1)

# Couleurs à faire défiler : Rouge, Vert, Bleu
colors = [(10, 0, 0), (0, 10, 0), (0, 0, 10)] #les valeurs par defaut 255 luminosité maximal, regler à 10 pour le confort des yeux
color_index = 0

# Configuration du bouton BOOT sur GPIO0 (avec pull-up)
button = Pin(0, Pin.IN, Pin.PULL_UP)

# Appliquer la couleur initiale (rouge)
neo[0] = colors[color_index]
neo.write()

```

Configuration du bouton boot :
"button = Pin(0, Pin.IN, Pin.PULL_UP)" : Définit la broche GPIO0 (le bouton BOOT) en mode entrée avec une résistance pull-up.
et Le bouton lira 1 quand il n’est pas appuyé et 0 quand il est appuyé.
"neo[0] = colors[color_index]" : Met la LED à la première couleur de la liste (ici rouge au début).
"neo.write()" : Envoie les données à la LED pour allumer la bonne couleur.

Explication de la boucle :
"while True:" Démarre une boucle infinie (le code à l'intérieur tourne en continu)
"if button.value() == 0:" Vérifie si le bouton est appuyé (valeur 0).
"color_index = (color_index + 1) % len(colors) Passe à la couleur suivante dans la liste.
Le % (modulo) permet de revenir au début après la dernière couleur (rouge → vert → bleu → rouge...).
"neo[0] = colors[color_index]" : Change la couleur affichée sur la LED.
"neo.write()" : Met à jour la LED avec la nouvelle couleur.
"print("Couleur actuelle :", colors[color_index])" : Affiche dans la console la couleur actuellement utilisée. pour verification

Anti rebond :
"while button.value() == 0:
  time.sleep(0.01)" : Attend que le bouton soit relâché avant de continuer (évite les doubles appuis).
  
"time.sleep(0.2)" : Petite pause pour éviter que l'appui soit détecté plusieurs fois (anti-rebond).

## Changement de la couleur d'une LED RGB en appuyant sur le boutton boot Arduino
Nous avons choisi de séparer la partie du code qui permet de changer la couleur de son propre ESP
et l'autre code permetant de changer la couleur de l'autre ESP (voir plus bas)

librairie de base pour arduino 
librairie pour le fonctionemment de la LED RGB
```
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>  //lib for LED_RGB fonction
```
Préparation et contrôle d’une LED NeoPixel sur GPIO48, 
définition du bouton boot sur GPIO0.
Initialisent le tableau de couleur à émettre ainsi qu’un compteur pour changer la couleur.

Adafruit_NeoPixel est une classe de Adafruit NeoPixel C++ library.
NEO_GRBW -> Indique à la bibliothèque comment interpréter les données de couleur : G (vert), R (rouge), B (bleu).
NEO_KHZ800 ->  Indique à la bibliothèque la fréquence du signal de données requise pour la LED
```
Adafruit_NeoPixel LED_RGB(1,48,NEO_GRBW + NEO_KHZ800);
const int BOOT_BUTTON = 0;  // GPIO0 is the boot button
 
uint8_t rgbColor[] = {0, 0, 0};  // Start with all colors off
uint8_t counter = 0;  // Conteur
```
fonctionement de la LED RGB 
initialisation de la luminositer et du bouton BOOT
```
void setup()
{
  LED_RGB.begin();  // Start function
  LED_RGB.setBrightness(45);  // To not hurt eyes
  pinMode(BOOT_BUTTON, INPUT);  // Configure boot button as input
}
```
fonction main 
Lecture du bouton boot
interation pour changement de couleur avec reset pour revenir à la couleur de base (rouge).

Serial.println() ->  affiche l'etat du bouton sur terminal.

buttonState : état bouton.
```
void loop()
{
  // Read the boot button state
  int buttonState = digitalRead(BOOT_BUTTON);
 
  // Print button state to serial monitor
  Serial.println(buttonState);
 
  // Change LED color based on button state
  if (buttonState == LOW)
  {  // Button is pressed (active LOW)
    if(counter < 4)
    {
      counter++;  // Increment counter and wrap around at 4
    }
    else
    {
      counter = 0;  // Reset counter
    }
   
  }
```
Selection de la couleur en fonction de l'incrementation fait précedement
Chaque case correspond à une couleur.
``` 
  // Toggle RGB based on counter
  switch (counter)
  {
    // Red
    case 0:
      rgbColor[0] = 255;
      rgbColor[1] = 0;
      rgbColor[2] = 0;
      break;
   
    // Green
    case 1:
      rgbColor[0] = 0;
      rgbColor[1] = 255;
      rgbColor[2] = 0;
      break;
   
    // Blue
    case 2:
      rgbColor[0] = 0;
      rgbColor[1] = 0;
      rgbColor[2] = 255;
      break;
  }
```
Application des variables pour afficher la couleur.

LED_RGB -> Adafruit_NeoPixel est un objet
.Color(r, g, b) -> regroupe toutes les données dans la variable color (32 bit)
setPixelColor(0, uint32_t) -> le 0 met la première LED à la couleur que l'on choisit.

on ajoute un délais pour une meilleur lecture du bouton
```
  // Set the LED color
  LED_RGB.setPixelColor(0, uint32_t(LED_RGB.Color(rgbColor[0], rgbColor[1], rgbColor[2])));
  LED_RGB.show();
   
  delay(100);  // Small delay to prevent too rapid reading
```
## Comunication entre deux ESP
Pour cette partie, nous allons faire en sorte lorsque les deux ESP (phyton et en arduino) communique entre eux une fois cela fait le boutton boot devrais changer la couleur de la LED de l'autre appareil.
### Moyen de communication 
comme expliquer sur ce lien internet : https://esp32io.com/tutorials/communication-between-two-esp32
notre appareil dispose de plusieur moyen de communication, tout depend de la distance entre nos deux ESP.

![Capture d’écran 2025-05-28 141305](https://github.com/user-attachments/assets/ed1bbcf5-beb5-43a7-a47d-bde39f2a79bb)

Nous allons donc utiliser la communication en wifi comme dans le tutoriel.
Vue que nous allons connecter les deux ESP en mode LAN (résaux local) donc un des deux va servir de routeur (TCP client/TCP server), nous n'avons pas besoin de se connecter à internet.
Nous avons choisit d'utiliser l'ESP phyton en tant que TCP server car la bibliotech socket facilite le code 
Et l'ESP en Arduino servira de TCP client donc c'est lui qui va envoyer la commande pour changer les couleurs.

## Communication en wifi TCP SERVER phyton


network permet de connecter l’ESP32 au Wi-Fi
socket sert à envoyer/recevoir des données sur ce réseau.
```
import socket
import network
```
Pour le clignotement de la couleur 
```
# État pour le clignotement
led_on = True
last_blink = time.ticks_ms()

```
Configuration du point d'accès wifi :
ap est un objet qui représente le point d’accès WiFi 
ap.config(essid='ESP_serveur', password='12345678', authmode=3) ESP_serveur nom du wifi
12345678 mot de passe
auhmode 3 type de sécurité WPA2 type de sécurité
```
# --- WiFi point d'accès ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP_serveur', password='12345678', authmode=3)  # AP sécurisé

print("AP démarré avec IP :", ap.ifconfig()[0])
```
Création d'un serveur TCP sur l’ESP32 qui écoute sur le port 1234, accepte jusqu’à 1 connexion en attente, et ne bloque pas l’exécution quand il n’y a pas de client connecté.
Cela permet de gérer les connexions entrantes sans interrompre le reste du programme
```
# --- TCP server setup ---
addr = socket.getaddrinfo('0.0.0.0', 1234)[0][-1]
server_socket = socket.socket()
server_socket.bind(addr)
server_socket.listen(1)
server_socket.setblocking(False)
print("Serveur TCP lancé sur port 1234")
```
Applique une couleur initiale sur la LED NeoPixel et définit une fonction qui fait tourner la couleur parmi une liste chaque fois qu’elle est appelée.
Simple et efficace pour gérer un cycle de couleurs.

```
# --- Applique couleur initiale ---
neo[0] = colors[color_index]
neo.write()

def change_color():
    global color_index
    color_index = (color_index + 1) % len(colors)
    neo[0] = colors[color_index]
    neo.write()
    print("Couleur changée:", colors[color_index])
```
Gestion du clignotement de la LED tout les 0.5 seconde.
Détecte un appui sur le bouton et ne change la couleur qu’une fois par appui, même si on maintiens le bouton enfoncé.
Le programme attend qu'on relâches le bouton avant d’accepter un nouvel appui, et ajoute un petit délai pour éviter les faux déclenchements liés au bruit mécanique du bouton.

```
# --- Boucle principale ---
while True:
    now = time.ticks_ms()

    # Clignotement toutes les 0.5 secondes
    if time.ticks_diff(now, last_blink) >= 500:
        led_on = not led_on
        if led_on:
            neo[0] = colors[color_index]
        else:
            neo[0] = (0, 0, 0)  # Éteint la LED
        neo.write()
        last_blink = now

    # Gestion du bouton local
    if button.value() == 0:
        change_color()
        while button.value() == 0:
            time.sleep(0.01)  # Antirebond
        time.sleep(0.2)  # Petite pause après appui
```
Vérifie si un client se connecte au serveur.
S’il reçoit le message "CHANGE", il change la couleur de la LED.
Ensuite, il ferme la connexion.
S’il n’y a pas de client, il continue sans bloquer.

```
# Accepter connexion client
try:
    cl, addr = server_socket.accept()
    print("Client connecté:", addr)
    cl.settimeout(2)
    data = cl.recv(1024)
    if data:
        msg = data.decode('utf-8').strip()
        print("Message reçu:", msg)
        if msg == "CHANGE":
            change_color()
    cl.close()
except OSError:
    pass

time.sleep(0.01)
```

## Communication en wifi TCP Client Arduino
L'ESP codé en Arduino sera le client c'est donc lui qui va provoquer le changement de couleur
sur l'autre ESP server en appuyant sur le boutton boot :

cette librairie nous permet de paramétrer la connection au wifi
`#include <WiFi.h>`
Initialisation des coordonée pour la connexion au ESP server
SSID nom du wifi
password mot de passse du wifi
host adresse IP de l'ESP32
```
const char* ssid = "ESP_serveur";
const char* password = "12345678";
 
const char* host = "192.168.4.1";  // IP du serveur AP ESP32 Python
const uint16_t port = 1234;
 
const int buttonPin = 0;
bool lastButtonState = HIGH;
```
Crée un objet client qui représente une connexion TCP au serveur WiFi.
`WiFiClient client;`
initialise la connexion série, configure un bouton.
Lance la connexion WiFi en mode client, et attend jusqu’à être connecté
tout en affichant l’état dans le terminal.
```
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
```
détecte précisément un appui sur le bouton
Envoie une requête "CHANGE" au serveur pour changer la couleur sur l'autre ESP32
Evite les rebonds, et mémorise l’état du bouton pour la prochaine lecture.
```
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
```

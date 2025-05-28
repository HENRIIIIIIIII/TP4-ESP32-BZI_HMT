# TP4-ESP32-BZI_HMT
## ESP32 Partie python
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
### Explication et stratégie du code en phyton
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
#### Explication du fonctionement de la LED RGB WS2812

Selon le datasheet la LED RGB communique via GPIO 48 (General Purpose Input/Output, entrée/sortie) : https://dl.espressif.com/dl/SCH_ESP32-S3-DEVKITC-1_V1_20210312C.pdf
Nous recuperons aussi la réference de la LED ce qui nous permet d'aller à son datasheet et de comprendre son fontionement à la page 8. http://www.normandled.com/upload/202105/SK6812MINI-HS%20LED%20Datasheet.pdf

![image](https://github.com/user-attachments/assets/863adfb6-4316-4e94-a3d6-d4bdee54b486)


Nous comprenons donc qu'une trame de 24 bits est communiqué et que chaque couleur et séparer en 8 partie chaque LED (R/G/B) recupére les information lié à ça couleur.

#### Changement de la couleur d'une LED RGB en appuyant sur le boutton boot
Bibliotech : 

"from machine import Pin" : importe la classe "Pin" qui nous permet de controler les broche GPIO de l'esp32.
"from neopixel import NeoPixel" : importe la classe "NeoPixel" pour contoler les LED RGB comme celle de type WS2812.
"import time" : Importe le module time pour pouvoir faire des pauses (sleep) dans le programme.

```
from machine import Pin
from neopixel import NeoPixel
import time

```
LED :
"pin = Pin(48, Pin.OUT)" : Définit la broche GPIO48 en mode sortie pour envoyer des données au NeoPixel
"neo = NeoPixel(pin, 1)" : Crée un objet NeoPixel branché sur pin avec 1 seule LED.
"colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]" : Liste des couleurs à afficher (rouge, vert, bleu) sous forme de (R, G, B).
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

## Comunication entre deux ESP
Pour cette partie, nous allons faire en sorte lorsque les deux ESP (phyton et arduino) communique entre eux une fois cela fait le boutton boot devrais changer la couleur de la LED de l'autre appareil.
Si il ne communique pas alors le boot change la couleur de son propre ESP.
### Moyen de communication 
comme expliquer sur ce lien internet : https://esp32io.com/tutorials/communication-between-two-esp32
notre appareil dispose de plusieur moyen de communication, tout depend de la distance entre nos deux ESP

![Capture d’écran 2025-05-28 141305](https://github.com/user-attachments/assets/ed1bbcf5-beb5-43a7-a47d-bde39f2a79bb)
### Communication en wifi partie phyton
Nous allons donc utiliser la communication en wifi comme dans le tutoriel.
Vue que nous allons connecter les deux ESP en mode LAN donc un des deux va servir de routeur, nous n'avons pas besoin de se connecter à internet.





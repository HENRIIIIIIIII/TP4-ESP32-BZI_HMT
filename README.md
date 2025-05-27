# TP4-ESP32-BZI_HMT
TP4 – ESP32 - Découverte
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

Tout ces étape nous ont permis de pouvoir flashé notre programme (l'envoyer à notre ESP) une fois celuit-ci écrit. Nous pouvons enfin crée un fichier main.py et commencer à coder.
### Explication et stratégie du code en phyton
Pour commencé nous avons verifier le fonctionement de l'appareil grace à un code exemple sur le site : https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/

```
from machine import Pin
from time import sleep
led = Pin(2, Pin.OUT)
while True:
  led.value(not led.value())
  sleep(0.5)

```
  
Ce dernier sert à alimenter la PIN n°2 de notre ESP32 et en branchant une LED de allons de la PIN n°2 au GND la PIN nommé G, la LED s'allume. Ce qui veut dire que notre code a été flashé correctement sur l'appareil.


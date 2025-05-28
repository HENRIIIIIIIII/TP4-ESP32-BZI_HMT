from machine import Pin
from neopixel import NeoPixel
import network
import socket
import time

# --- LED setup ---
pin = Pin(48, Pin.OUT)
neo = NeoPixel(pin, 1)
colors = [(10,0,0), (0,10,0), (0,0,10)]
color_index = 0

# --- Bouton local ---
button = Pin(0, Pin.IN, Pin.PULL_UP)

# --- WiFi point d'accès ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP_serveur', password='12345678', authmode=3)  # AP sécurisé

print("AP démarré avec IP :", ap.ifconfig()[0])

# --- TCP server setup ---
addr = socket.getaddrinfo('0.0.0.0', 1234)[0][-1]
server_socket = socket.socket()
server_socket.bind(addr)
server_socket.listen(1)
server_socket.setblocking(False)
print("Serveur TCP lancé sur port 1234")

# --- Applique couleur initiale ---
neo[0] = colors[color_index]
neo.write()

def change_color():
    global color_index
    color_index = (color_index + 1) % len(colors)
    neo[0] = colors[color_index]
    neo.write()
    print("Couleur changée:", colors[color_index])

while True:
    # Bouton local
    if button.value() == 0:
        change_color()
        while button.value() == 0:
            time.sleep(0.01)
        time.sleep(0.2)

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

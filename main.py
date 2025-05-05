from machine import Pin	#code trouvé sur le site https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/
from time import sleep

led = Pin(2, Pin.OUT)

while True:
  led.value(not led.value())
  sleep(0.5)
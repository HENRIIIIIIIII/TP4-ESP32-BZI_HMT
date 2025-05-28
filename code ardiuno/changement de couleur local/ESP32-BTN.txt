#include <Arduino.h>
#include <Adafruit_NeoPixel.h>  //lib for LED_RGB fonction
 
Adafruit_NeoPixel LED_RGB(1,48,NEO_GRBW + NEO_KHZ800);
const int BOOT_BUTTON = 0;  // GPIO0 is the boot button
 
uint8_t rgbColor[] = {0, 0, 0};  // Start with all colors off
uint8_t counter = 0;  // Conteur
 
void setup()
{
  LED_RGB.begin();  // Start function
  LED_RGB.setBrightness(45);  // To not hurt eyes
  pinMode(BOOT_BUTTON, INPUT);  // Configure boot button as input
  Serial.begin(115200);  // Initialize serial for debugging
}
 
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
 
  // Set the LED color
  LED_RGB.setPixelColor(0, uint32_t(LED_RGB.Color(rgbColor[0], rgbColor[1], rgbColor[2])));
  LED_RGB.show();
   
  delay(100);  // Small delay to prevent too rapid reading
}
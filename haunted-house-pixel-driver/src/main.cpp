#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_PIXELS 60

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);
unsigned long lastCommandTime = 0;
const unsigned long commandTimeout = 10000;

void propagate()
{
    for (int i = 0; i < NUM_PIXELS; i++)
    {
        int pixel_index = random(0, NUM_PIXELS);
        strip.setPixelColor(pixel_index, strip.Color(255, 255, 255));
        strip.show();
        delay(5);
    }
}

void flash()
{
    strip.fill(strip.Color(255, 255, 255), 0, NUM_PIXELS);
    strip.show();
    delay(1000);
}

void strobe()
{
    for (int brightness = 0; brightness <= 255; brightness += 5)
    {
        strip.fill(strip.Color(brightness, 0, 0), 0, NUM_PIXELS);
        strip.show();
        delay(30);
    }
    for (int brightness = 255; brightness >= 0; brightness -= 5)
    {
        strip.fill(strip.Color(brightness, 0, 0), 0, NUM_PIXELS);
        strip.show();
        delay(30);
    }
}

void setup()
{
    Serial.begin(9600);
    strip.begin();
    strip.show();
}

void loop()
{
    if (Serial.available() > 0)
    {
        char command = Serial.read();
        if (command == '1')
        {
            lastCommandTime = millis();
            propagate();
            flash();
            delay(500);
            strip.clear();
            strip.show();
        }
        else if (command == '2')
        {
            lastCommandTime = millis();
            strip.clear();
            strip.show();
        }
    }

    if (millis() - lastCommandTime > commandTimeout)
    {
        strobe();
    }
}
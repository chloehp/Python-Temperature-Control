# Python-Temperature-Control

### What does it do?

This Python app is for use with a DHT11 or DHT22 temperature and humidity sensor connected to a Raspberry Pi. PTC will record the temperature and humidity throughout the day, then (optionally) generate an SVG line graph and automatically send an email report at the end of every day, or when prompted. I made this app to monitor and get a daily report of the temperature and humidity from inside my tortoise's vivarium. In the future I want to add a switch so that it cant automatically turn the heater off and on.

### Set up the Pi

First you will need to install Raspberry Pi OS from the Raspberry Pi Imager, you will want the full desktop version as this will actually simplify letting the app run without being connected to a screen or keyboard (and later make it easier to set up to fully restart in case of a power cut). Set up the Pi to connect to Wi-Fi, or plug it into your LAN via Ethernet. You may want to be able to interact and **set up your Pi remotely**, say if it's set up by your reptile enclosure and not next to a monitor and keyboard - if this is you, jump to [Headless set up and start](#Headless set up and start).

Update your Pi, make sure you have python3 and pip installed, then install and activate a virtual environment:
```
sudo apt update
python3 -m venv env1
. env1/bin/activate
```
Then you can install the adafruit library PTC will use to drive the sensor
```
python3 -m pip install adafruit-circuitpython-dht
```

##### Turn off the Pi and connect the sensor.
Regardless of whether you're connecting the DHT11 or DHT22 module, they both connect to the Pi the same way, the main differences being the resolution and range. There are three pins that can connect directly to the GPIO, depending on the module they can be labelled something like "DAT, VCC, GND", or "+, out, -". 
- Use jumper wires to connect "VCC"/"+" to a 5v pin (like 2 or 4)
- "GND"/"-", to a ground pin (6 or 9)
- "DAT"/"out" to GPIO 4 - This is the data line!

Now you can test the setup!
From the Pi:
```
cd ptc
python testDHT.py
```
This should start spitting out the temperature, humidity and datetime in three columns. Breathe on the sensors for the numbers to go up, leave it and they go back down. It's ok if it occasionally gives you bad data, DHT sensors aren't very reliable, but this is handled in the app proper.

Here's a more in-depth tutorial for connecting the sensor
https://randomnerdtutorials.com/raspberry-pi-dht11-dht22-python/

### Headless set up and start

**NOTE: Please replace 'user' in the following instructions with YOUR username.**
Turn on you Pi, you should have already set it up so that it connects to your local area network automatically. For a connection that works every time, you'll need your Pi's IP address, the easiest way to find this is by from your router's admin page, there should be a page with all the connected devices, and you can find your IP address under 'raspberrypi' (or whatever you named your device).
Log in to your Pi remotely via SSH, then go into your Pi's settings. 
```
ssh user@your IP address here
sudo raspi-config
```
- Go into Interface Options > VNC
  and enable VNC
- Go into System Options > Boot / Auto Login
  and turn on "Desktop Autologin"
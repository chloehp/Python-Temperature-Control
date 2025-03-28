# Python-Temperature-Control

### What does it do?

This Python app is for use with a DHT11 or DHT22 temperature and humidity sensor connected to a Raspberry Pi. PTC will record the temperature and humidity throughout the day, then (optionally) generate an SVG line graph and automatically send an email report at the end of every day, or when prompted. I made this app to monitor and get a daily report of the temperature and humidity from inside my tortoise's vivarium. In the future I want to add a switch so that it cant automatically turn the heater off and on.

### Set up the Pi

First you will need to install Raspberry Pi OS from the Raspberry Pi Imager, you will want the full desktop version as this will actually simplify letting the app run without being connected to a screen or keyboard (and later make it easier to set up to fully restart in case of a power cut). Set up the Pi to connect to Wi-Fi, or plug it into your LAN via Ethernet. You may want to be able to interact and **set up your Pi remotely**, say if it's set up at your reptile enclosure and not next to a monitor and keyboard - if this is you, jump ahead to [Headless set up](#Headless set up).

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
This library is installed within the virtual environment, so you must activate it every boot before running PTC, this can be automated as shown in the [Auto start](#Auto Start) section.

##### Turn off the Pi and connect the sensor.
Regardless of whether you're connecting the DHT11 or DHT22 module, they both connect to the Pi the same way, the main differences being the resolution and range. There are three pins that can connect directly to the GPIO, depending on the module they can be labelled something like "DAT, VCC, GND", or "+, out, -". 
- Use jumper wires to connect "VCC"/"+" to a 5v pin (like 2 or 4)
- "GND"/"-", to a ground pin (6 or 9)
- "DAT"/"out" to GPIO 4 - This is the data line!

Now you can test the setup!
From the Pi (making sure you activate the virtual environment):
```
. env1/bin/activate
cd Python-Temperature-Control
python testDHT.py
```
This should start spitting out the temperature, humidity and datetime in three columns. Breath on the sensors for the numbers to go up, leave it and they go back down. It's ok if it occasionally gives you bad data, DHT sensors aren't very reliable, but this is handled in the app proper.

Here's a more in-depth tutorial for connecting the sensor
https://randomnerdtutorials.com/raspberry-pi-dht11-dht22-python/

If everything's working fine, you're ready to run the app on your Pi!
```
python main.py
```
Like in the test program, you will get the temperature, humidity and datetime in three columns, this will update about every 5 minutes. At the end of each day, PTC will generate a new SVG line graph of the temperature and humidity from the last 24 hours, which is saved in '/graphs'.

### Set up the email service

**NOTE: To complete this section you must enter details into config.json in PTC's files.**
Create a new account you want to use to send and receive emails with your Pi, the rest of this tutorial assumes you are using Gmail, otherwise some details may be different. Enter your new email address into "emailAddress" in config. 
You must **create an App Password** so that PTC can connect to the email service, with Gmail, you must first set up "2-Step Verification" in account settings >Security > Signing in to Google. The app password settings may be hidden away, but searching for "gmail app password" should get you to a google support page that leads to [this link](https://myaccount.google.com/apppasswords). Follow the steps and save the password in "emailPass" in config.

Gmail's POP and SMPT details have been entered by default, if you're using a different service, you must look up their POP domain (to retrieve emails), SMPT domain (for sending, usually the same but beginning with "smpt."), and the SMPT port number. Add these details to "popDomain", "smtpDomain" and "smtpPort" in config.

**PTC is an email bot!** If you send an email to the address you just set up with the subject "r", or "report", your Raspberry Pi running PTC will email you back with today's temperature and humidity data so far (with a line graph). You can add to these keywords in the "reportCodes" array in config.

At the end of each day, after generating a new line graph, PTC can send that days report and SVG graph to **the email address in "sendTo"** in config.
You can change PTC's default subject in "title", and add a message into the email body in "message".

Lastly, **change "sendEmail" to true!** Save config.json and run PTC.

### Headless set up

**NOTE: Please replace 'user' in the following instructions with YOUR username.**
Download and install [TigerVNC viewer](https://tigervnc.org/) on your main computer.
Turn on you Pi, you should have already set it up so that it connects to your local area network automatically. For a connection that works every time, you'll need your Pi's IP address, the easiest way to find this is by from your router's admin page, there should be a page with all the connected devices, and you can find your IP address under 'raspberrypi' (or whatever you named your device).
Log in to your Pi remotely via SSH, then go into your Pi's settings:
```
ssh user@your IP address here
sudo raspi-config
```
- Go into Interface Options > VNC
  and enable VNC
- Go into System Options > Boot / Auto Login
  and turn on "Desktop Autologin"

You can copy across the files via SSH from their source folder on your computer:
```
scp -r Python-Temperature-Control user@your IP address here:/home/user
```
From here you can follow the rest of [Set up the Pi](#Set up the Pi) via SSH - set up a virtual environment, install the adafruit library and connect the sensors.

Turn on the Pi, and **connect to it via TigerVNC**, use the same IP address, username and password as when connecting via SSH. You should now be connected to your Pi via a remote desktop, open up a new terminal, activate the virtual environment, then and PTC.
```
. env1/bin/activate
cd Python-Temperature-Control
python main.py
```
This way, you can disconnect and close the connection (TigerVNC), and PTC will keep running.
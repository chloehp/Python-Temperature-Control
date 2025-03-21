from datetime import datetime
from time import sleep
import json

import temphumid
import sendmail
import utility

appVersion = "v.0.0.0.0.0.0.0.0000003"
currentDay = datetime.now().day                     # current day of the month
try: defaultConfig = utility.importConfig()         # load config. If this fails, then one or more essential variable is missing
except: raise Exception("The following variables are required in config.json: tooHighTemp, tooLowTemp, location, generateGraph, sendEmail, reportNow, emailAddress, emailPass, sendTo, title")

temphumid.startup()
print("Running Python Temperature Control", appVersion)
try: print("""
                    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                        
                 ▒▒▒                    ▒▒▒▒                 ██████             
              ▒▒▒▒                          ▒▒              ██   ██             
             ▒           ▄▄▄████████▄         ▒    ▄▄       █████               
            ▒          ██         ▄▄▀█▄         ▄▄█▀▀▀█▄    █        ███        
   ▄████▄▄           ▄█▀▄▄        ██ ██      ▄█▓▀      ▓    █   █████           
  ▓▀     ▀▓▓█▄▄      ██ ██         ▒ ██    █▀▀        ▄█          █             
  ▓           ▀      ██ ▒   ▄▄ ▄█▀  ██               ▄▓           █     ████    
   ▓▄               ▄ ██▄    ▀█▀  ▄██              ▄▓            █     █        
    ▓▓▄          ▄▄▓    ███▄▄▄▄▄█▀▀  █▄▄         ▄▄▓                   █        
       ▓▓▄     ▄▓▓                      ▓█▄▄▄▄▄█▓                      ████     
         ▀▀███▀▀                           ▀▀▀                                  
""")
except: pass
sleep(1.5)
print(f"{"Temperature":15}{"Humidity":15}Time")                             # formatted 3 columns, width 15
while True:                                                                 # loop forever (about every 5 mins)
    tHour = datetime.now().hour + (datetime.now().minute / 60)              # time of day (decimal)
    #tHour = 24
    try: config = utility.importConfig()                                    # update config
    except:
        config = defaultConfig                                              # if error in config file, use default config
        utility.logError("Config could not be updated. Using default config instead.")
    
    highTemp = config["tooHighTemp"]                                        # what temperature is too high
    lowTemp = config["tooLowTemp"]                                          # what temperature is too low
    svg = ""
    stringDate = str(datetime.now())                                        # date as string

    if datetime.now().day != currentDay:                                    # if it's a different day than it was 5 minutes ago 
        print("New day: Sending report")
        if config["generateGraph"]:                                         # if generateGraph is True
            svg = sendmail.generateSVG(stringDate, highTemp, lowTemp)       # generate new temp and humidity graph
                                                                            # else svg can stay blank
        if config["sendEmail"]:                                             # if sendEmail is True
            sendmail.sendMail(config["sendTo"], config, stringDate, svg)    # send email

        temphumid.logList.clear()                                           # reset todays list (and log.json)
        currentDay = datetime.now().day                                     # set currentday
        print(f"{"Temperature":15}{"Humidity":15}Time")
        
    try: 
        receivedEmails = utility.getMail(config)                                # check emails
        if len(receivedEmails) > 0:                                             # if theres something in the mail queue
            if config["generateGraph"]:                                         # if generateGraph is True
                svg = sendmail.generateSVG(stringDate, config["tooHighTemp"], config["tooLowTemp"])       # generate new temp and humidity graph
                                                                                # else svg can stay blank
            if config["sendEmail"]:                                             # if sendEmail is True
                for returnAddress in receivedEmails:
                    sendmail.sendMail(returnAddress, config, stringDate, svg)   # send email back with tuple from the mail queue and generated
            print(f"{"Temperature":15}{"Humidity":15}Time")

    except: utility.logError("Pop Mail error. Could not get emails for " + config["emailAddress"])        
    
    temperature, humidity = temphumid.readTempAndHumid()                    # read temperature and humidity
    temphumid.recordTempAndHumid(tHour, temperature, humidity)              # record temperature and humidity
    print(f"{str(temperature) + "°C":15}{str(humidity) + "%":15}{datetime.now()}") # print formatted 3 columns, width 15
    
    sleep(300)
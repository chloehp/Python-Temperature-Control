from datetime import datetime
from time import sleep
import json

import temphumid
import sendmail
import utility

appVersion = "v.0.0.0.0.0.0.0.0000002"
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
print("Temperature      Humidity      Time")
while True:                                                                 # loop forever (about every 5 mins)
    tHour = datetime.now().hour + (datetime.now().minute / 60)              # time of day (decimal)
    #tHour = 24
    try: config = utility.importConfig()                                    # update config
    except:
        config = defaultConfig                                              # if error in config file, use default config
        utility.logError("Config could not be updated. Using default config instead.")
    
    highTemp = config["tooHighTemp"]                                        # what temperature is too high
    lowTemp = config["tooLowTemp"]                                          # what temperature is too low

    if datetime.now().day != currentDay:                                    # if it's a different day than it was 10 minutes ago 
        print("New day: Sending report")
        stringDate = str(datetime.now())                                    # date as string
        svg = ""
        if config["generateGraph"]:                                         # if generateGraph is True
            svg = sendmail.generateSVG(stringDate, highTemp, lowTemp)       # generate new temp and humidity graph
                                                                            # else svg can stay blank
        if config["sendEmail"]:                                             # if sendEmail is True
            sendmail.sendMail(config["sendTo"], config, stringDate, svg)    # send email

        temphumid.logList.clear()                                           # reset todays list (and log.json)
        currentDay = datetime.now().day                                     # set currentday
    else:
        try: utility.getMail(config)                                        # check emails
        except: utility.logError("Could not get emails.")
    
    temperature, humidity = temphumid.readTempAndHumid()                    # read temperature and humidity
    temphumid.recordTempAndHumid(tHour, temperature, humidity)              # record temperature and humidity
    print(temperature, "°C           ", humidity, "%         ", datetime.now())
    
    sleep(300)
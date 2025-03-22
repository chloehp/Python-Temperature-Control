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
print(f"{"Temperature":15}{"Humidity":15}Time")                             # print 3 column headers, width 15
while True:                                                                 # loop forever (about every 5 mins)
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
                                                                            # else dont
        temphumid.logList.clear()                                           # reset todays list (and log.json)
        currentDay = datetime.now().day                                     # set currentday
        print(f"{"Temperature":15}{"Humidity":15}Time")                     # reprint 3 column headers, width 15
        
    try: 
        receivedEmails = utility.getMail(config)                                # check emails
        if len(receivedEmails) > 0:                                             # if theres something in the mail queue
            if config["generateGraph"]:                                         # if generateGraph is True
                svg = sendmail.generateSVG(stringDate, highTemp, lowTemp)       # generate new temp and humidity graph
                                                                                # else svg can stay blank
            if config["sendEmail"]:                                             # if sendEmail is True
                for returnAddress in receivedEmails:                            # for every valid email recieved
                    sendmail.sendMail(returnAddress, config, stringDate, svg)   # send email back
            print(f"{"Temperature":15}{"Humidity":15}Time")                     # reprint 3 column headers, width 15

    except: utility.logError("Pop Mail error. Could not get emails for " + config["emailAddress"])        
    
    temperature, humidity = temphumid.readTempAndHumid()                                            # read temperature and humidity
    temphumid.recordTempAndHumid(datetime.now().hour, datetime.now().minute, temperature, humidity) # record time, temperature and humidity
    print(f"{str(temperature) + "°C":15}{str(humidity) + "%":15}{datetime.now()}")                  # print formatted 3 columns, width 15
    # sleep about 5 mins
    sleep(300)
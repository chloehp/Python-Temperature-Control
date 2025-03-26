from datetime import datetime
from time import sleep
import json

import temphumid
import sendmail
import utility

appVersion = "v.0.0.0.0.0.0.0.0000003"
currentDay = datetime.now().day                     # current day of the month
timeToReset = False
try: defaultConfig = utility.importConfig()         # load config. If this fails, then one or more essential variable is missing
except: raise Exception("The following variables are required in config.json (even if left blank): tooHighTemp, tooLowTemp, generateGraph, sendEmail, emailAddress, emailPass, popDomain, smtpDomain, smtpPort, reportCodes, sendTo, title and message")

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
print(f"""{"Temperature":15}{"Humidity":15}Time""")                         # print 3 column headers, width 15
while True:                                                                 # loop forever (about every 5 mins)
    try: config = utility.importConfig()                                    # update config
    except:
        config = defaultConfig                                              # if error in config file, use default config
        utility.logError("Config could not be updated. Using default config instead.")
    
    highTemp = config["tooHighTemp"]                                        # what temperature is too high
    lowTemp = config["tooLowTemp"]                                          # what temperature is too low
    svg = ""
    stringDate = str(datetime.now())                                        # date as string

    try:
        rHour = int(config["resetTime"][0])                                     # get Hour for PTC to reset from config
        rMin = round(int(config["resetTime"][1]), -1)                           # get Minute and round to 10
        if rHour > 23 or rHour < 0: rHour = 0                                   # if rHour is outside accepted range, set as zero
        if rMin > 50 or rMin < 0: rMin = 0                                      # if rMin is outside accepted range, set as zero
        if datetime.now().hour == rHour and datetime.now().minute >= rMin:      # if at the designated reset hour AND at or past the reset minute
            timeToReset = True                                                  # allow reset
        else:
            timeToReset = False
    except: 
        utility.logError("resetTime set incorrectly in config.json")
        timeToReset = True

    if timeToReset and datetime.now().day != currentDay:                    # if timeToReset is True and it's a different day than when last checked
        print("New day: Sending report")
        if config["generateGraph"]:                                         # if generateGraph is True
            svg = sendmail.generateSVG(stringDate, highTemp, lowTemp)       # generate new temp and humidity graph
                                                                            # else svg can stay blank
        if config["sendEmail"]:                                             # if sendEmail is True
            sendmail.sendMail(config["sendTo"], config, stringDate, svg)    # send email
                                                                            # else dont
        temphumid.logList.clear()                                           # reset todays list (and log.json)
        currentDay = datetime.now().day                                     # set currentday
        print(f"""{"Temperature":15}{"Humidity":15}Time""")                 # reprint 3 column headers, width 15
        
    try: 
        receivedEmails = utility.getMail(config)                                # check for emails, load as list of addresses "receivedEmails"
        if len(receivedEmails) > 0:                                             # if theres something in the mail queue
            if config["generateGraph"]:                                         # if generateGraph is True
                svg = sendmail.generateSVG(stringDate, highTemp, lowTemp)       # generate new temp and humidity graph
                                                                                # else svg can stay blank
            if config["sendEmail"]:                                             # if sendEmail is True
                for returnAddress in receivedEmails:                            # for every valid email recieved
                    sendmail.sendMail(returnAddress, config, stringDate, svg)   # send email back
            print(f"""{"Temperature":15}{"Humidity":15}Time""")                 # reprint 3 column headers, width 15

    except: utility.logError("Pop Mail error. Could not get emails for " + config["emailAddress"])        
    
    temperature, humidity = temphumid.readTempAndHumid()                                            # read temperature and humidity
    temphumid.recordTempAndHumid(datetime.now().hour, datetime.now().minute, temperature, humidity) # record time, temperature and humidity
    print(f"""{str(temperature) + "°C":15}{str(humidity) + "%":15}{datetime.now()}""")              # print formatted 3 columns, width 15
    sleep(300)                                                                                      # sleep about 5 mins
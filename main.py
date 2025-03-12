from datetime import datetime
from time import sleep
import json

import temphumid
import sendmail
import utility

appVersion = "v.0.0.0.0.0.0.0.0000001"
currentDay = datetime.now().day             # current day of the month
defaultConfig = utility.importConfig()      # load config

temphumid.startup()
print("Running Python Temperature Control", appVersion)
print("Temperature      Humidity      Time")
while True:                                                                 # loop forever (every 10 mins)
    tHour = datetime.now().hour + (datetime.now().minute / 60)              # time of day (decimal)
    tHour = 24
    try: config = utility.importConfig()                                    # update config
    except:
        config = defaultConfig                                              # if error in config file, use default config
        utility.logError("Config could not be updated. Using default config instead")
    
    highTemp = config["tooHighTemp"]                                        # what temperature is too high
    lowTemp = config["tooLowTemp"]                                          # what temperature is too low
    temperature, humidity = temphumid.readTempAndHumid()                    # read temperature and humidity
    temphumid.recordTempAndHumid(tHour, temperature, humidity)              # record temperature and humidity
    print(temperature, "°C           ", humidity, "%         ", datetime.now())

    reportNow = False
    if datetime.now().day != currentDay or reportNow == True:               # if it's a different day than it was 10 minutes ago
        print("New day")
        stringDate = str(datetime.now())                                    # date as string
        svg = ""
        if config["generateGraph"] == True:                                 # if generateGraph is True
            svg = sendmail.generateSVG(stringDate, highTemp, lowTemp)       # generate new temp and humidity graphs
                                                                            # else svg can stay blank
        #sendmail.sendMail(config, stringDate, svg)                          # send email
        temphumid.logList.clear()                                           # reset todays list (and log.json)
        currentDay = datetime.now().day                                     # set currentday

    sleep(600)
from datetime import datetime
from time import sleep
import json
import temphumid
import sendmail

cDay = datetime.now().day                           # current day of the month

hasBeenSentToday = False

temphumid.startup()
while True:                                                                 # loop forever (every 10 mins)
    tHour = datetime.now().hour + (datetime.now().minute / 60)              # time of day (decimal)    
    configOpen = open("config.json", "r")
    config = json.loads(configOpen.read())                                  # get config as dictionary
    tempAndHumid = temphumid.readTempAndHumid()                             # read temperature and humidity
    temphumid.recordTempAndHumid(tHour, tempAndHumid[0], tempAndHumid[1])   # record temperature and humidity
    #print(str(tempAndHumid[0]) + "°C", str(tempAndHumid[1]) + "%")
    
    rTime = config["resetTime"]                                     # time of day for hasBeenSentToday
    if hasBeenSentToday != True and tHour >= rTime:                 # if at or past reset-time and data has not been sent today 
        strDate = str(datetime.now())                               # date as string
        sendmail.genTempSVG()                                 # generate new temp and humidity graphs

        #sendmail.sendMail(config, strDate, svg)                    # send email
        temphumid.tempHumidList.clear()                             # clear days list (and log.json)
        hasBeenSentToday = True

    if datetime.now().day != cDay:                  # new day
        cDay = datetime.now().day                   # set currentday
        hasBeenSentToday = False

    sleep(600)
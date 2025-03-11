from datetime import datetime
from time import sleep
import temphumid
import sendmail

cDay = datetime.now().day                           # current day of the month

tooHighTemp = 42
tooLowTemp = 21
resetTime = 9           # time of the day that the app makes/sends graphs and, time in decimal

hasBeenSentToday = False

temphumid.startup()
while True:                                                                 # loop forever (every 10 mins)
    tHour = datetime.now().hour + (datetime.now().minute / 60)              # time of day (decimal)    
    tempAndHumid = temphumid.readTempAndHumid()                             # read temperature and humidity
    temphumid.recordTempAndHumid(tHour, tempAndHumid[0], tempAndHumid[1])   # record temperature and humidity
    print(str(tempAndHumid[0]) + "°C", str(tempAndHumid[1]) + "%")
    
    if hasBeenSentToday != True and tHour >= resetTime:     # if at or past reset-time and data has not been sent today 
        #sendmail.genSVG()                                   # generate new temp and humidity graphs
        #sendmail.sendMail()                                 # send email with the svgs
        cDay = datetime.now().day                           # set currentday
        hasBeenSentToday = True

    if datetime.now().day != cDay:                  # new day
        hasBeenSentToday = False

    sleep(3)
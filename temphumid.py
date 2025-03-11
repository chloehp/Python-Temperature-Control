import json
import random

tempHumidList = []

def startup():
    log = open("log.json", "r")
    logRead = log.read()
    if len(logRead) > 0:                                    # if log.json has data
        global tempHumidList
        tempHumidList = json.loads(logRead)                 # load that data into tempHumidList and keep going

def readTempAndHumid():
    # for now, setting fake numbers
    tem = random.randrange(12, 48)
    hum = random.randrange(0, 100)

    return tem, hum

def recordTempAndHumid(time, temp, humidity):
    tAndH = {                                               # create dictionary
        "time": time,
        "temp": temp,
        "humid": humidity
    }
    tempHumidList.append(tAndH)                             # record dictionary into tempHumidList
    log = open("log.json", "w")
    log.write(json.dumps(tempHumidList))                    # record to log.json, in case of power loss, will be restored in startup()
    log.close()
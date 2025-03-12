import json
import random

logList = []

def startup():
    log = open("log.json", "r")
    logRead = log.read()
    if len(logRead) > 0:                                    # if log.json has data
        global logList
        logList = json.loads(logRead)                 # load that data into logList and keep going

def readTempAndHumid():
    # for now, setting fake numbers
    t = random.randrange(12, 48)
    h = random.randrange(0, 100)

    return t, h

def recordTempAndHumid(time, temp, humidity):
    th = {                                               # create dictionary
        "time": time,
        "temp": temp,
        "humid": humidity
    }
    logList.append(th)                             # record dictionary into logList
    log = open("log.json", "w")
    log.write(json.dumps(logList))                    # record to log.json, in case of power loss, will be restored in startup()
    log.close()
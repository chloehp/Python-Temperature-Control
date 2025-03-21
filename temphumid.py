simulated = True

import json
from time import sleep

if simulated:
    import random
else:
    import board
    import adafruit_dht
    sensor = adafruit_dht.DHT11(board.D4)

import utility

logList = []

def startup():
    global logList
    try:
        log = open("log.json", "r")
        logRead = log.read()
        if len(logRead) > 0:                    # if log.json has data
            logList = json.loads(logRead)       # load that data into logList and keep going
    except:
        logList.clear()
        utility.logError("Bad data from log.json, clear list. Start from scratch.")

readAttempts = 0
def readTempAndHumid():
    global readAttempts
    readAttempts += 1
    try:
        if simulated:                       # fake numbers (random)
            t = random.randrange(12, 48)
            h = random.randrange(0, 100)
        else:                               # real numbers (from sensor)
            t = sensor.temperature          # attempt temperature read
            h = sensor.humidity             # attempt humidity read
            t, h = float(t), float(h)       # force int so that it will throw error if not a number
        readAttempts = 0                # reset read attempts

    except:
        utility.logError(f"""Bad sensor data. Attempt {str(readAttempts)}""")
        if readAttempts < 3:            # will try again 3 times
            print("Trying again in 10 seconds")
            sleep(10)
            t, h = readTempAndHumid()   # try again
        else:
            utility.logError("Failed to get sensor data, giving up")
            t, h = -999, -999           # return obviously spoiled data
            readAttempts = 0            # reset read attempts
    
    return t, h                         # return temperature and humidity


def recordTempAndHumid(time, temp, humidity):
    th = {                              # create dictionary
        "c": time,
        "t": temp,
        "h": humidity
    }
    logList.append(th)                  # record dictionary into logList
    log = open("log.json", "w")
    log.write(json.dumps(logList))      # record to log.json, in case of power loss, will be restored in startup()
    log.close()
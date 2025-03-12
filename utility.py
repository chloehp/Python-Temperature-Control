from datetime import datetime
import json

def importConfig():    
    configOpen = open("config.json", "r")
    config = json.loads(configOpen.read())  # get config as dictionary
    configOpen.close()
    return config

def logError(e):
    e = str(datetime.now()) + ": " +  e     # format error with date and time
    print(e)
    errorLog = open("errorlog.txt", "a")
    errorLog.write(e + "\n")                # write to error log, plus new line
    errorLog.close()
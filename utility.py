from datetime import datetime
import json

def importConfig():    
    configOpen = open("config.json", "r")
    config = json.loads(configOpen.read())  # get config as dictionary
    configOpen.close()
    # check all required variables are there, else will error
    tooHighTemp, tooLowTemp, generateGraph, sendEmail, reportNow, emailAddress, emailPass, sendTo, title, message = config["tooHighTemp"], config["tooLowTemp"], config["generateGraph"], config["sendEmail"], config["reportNow"], config["emailAddress"], config["emailPass"], config["sendTo"], config["title"], config["message"]
    return config

def logError(e):
    e = str(datetime.now()) + ": " +  e     # format error with date and time
    print(e)
    errorLog = open("error.log", "a")
    errorLog.write(e + "\n")                # write to error log, plus new line
    errorLog.close()

def replaceInFile(file, x, y):
    r = open(file, "r")
    read = r.read()
    r.close()
    rep = read.replace(x, y)
    w = open(file, "w")
    w.write(rep)

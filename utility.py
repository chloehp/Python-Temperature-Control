from datetime import datetime
import json
#import getpass
import poplib

import sendmail

def importConfig():    
    configOpen = open("config.json", "r")
    config = json.loads(configOpen.read())  # get config as dictionary
    configOpen.close()
    # check all required variables are there, else will error
    tooHighTemp, tooLowTemp, generateGraph, sendEmail, reportCodes, emailAddress, emailPass, sendTo, title, message = config["tooHighTemp"], config["tooLowTemp"], config["generateGraph"], config["sendEmail"], config["reportCodes"], config["emailAddress"], config["emailPass"], config["sendTo"], config["title"], config["message"]
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

def getMail(config):
    stringDate = str(datetime.now())                # date as string
    popMail = poplib.POP3_SSL('pop.googlemail.com', '995') 
    popMail.user(config["emailAddress"]) 
    popMail.pass_(config["emailPass"]) 
    numMessages = len(popMail.list()[1])

    for i in range(numMessages):                    # in new messages
        returnAddress = ""
        subject = ""

        for msg in popMail.retr(i+1)[1]:            # in each POP line
            m = str(msg)
            if m.startswith("b'Return-Path: <"):    # if there is a return address
                returnAddress = m[16:-2]            # get returnAddress
            if m.startswith("b'Subject:"):          # if there is a subject
                subject = m[11:-1]                  # get subject
        
        if subject in config["reportCodes"]:                                    # if a report code has been sent in an email subject
            svg = ""
            if config["generateGraph"]:                                         # if generateGraph is True
                svg = sendmail.generateSVG(stringDate, config["tooHighTemp"], config["tooLowTemp"])       # generate new temp and humidity graph
                                                                                # else svg can stay blank
            if config["sendEmail"]:                                             # if sendEmail is True
                sendmail.sendMail(returnAddress, config, stringDate, svg)       # send email back

    popMail.quit()
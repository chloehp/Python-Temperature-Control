from datetime import datetime
import json
import poplib

def importConfig():    
    configOpen = open("config.json", "r")
    config = json.loads(configOpen.read())  # get config as dictionary
    configOpen.close()
    # check all required variables are there, will error if any are missing that prevents startup or prevents updating of bad config
    tooHighTemp, tooLowTemp, generateGraph, sendEmail, reportCodes, emailAddress, emailPass, sendTo, title, message = config["tooHighTemp"], config["tooLowTemp"], config["generateGraph"], config["sendEmail"], config["reportCodes"], config["emailAddress"], config["emailPass"], config["sendTo"], config["title"], config["message"]
    return config

def logError(e):
    e = str(datetime.now()) + ": " +  e     # format error with date and time
    print(e)
    errorLog = open("error.log", "a")
    errorLog.write(e + "\n")                # write to error log, plus new line
    errorLog.close()

#def replaceInFile(file, x, y):
#    r = open(file, "r")
#    read = r.read()
#    r.close()
#    rep = read.replace(x, y)
#    w = open(file, "w")
#    w.write(rep)

def getAttachment(fileName):
    try:
        fileOpen = open(fileName, "rb")
        file = fileOpen.read()
        fileOpen.close()
        return file                                         # return the file as bytes
    except: 
        utility.logError(f"""Could not get '{fileName}'""")
        return ""                                           # return blank string (falsey)


def getMail(config):
    stringDate = str(datetime.now())                # date as string
    popMail = poplib.POP3_SSL('pop.googlemail.com', '995') 
    popMail.user(config["emailAddress"]) 
    popMail.pass_(config["emailPass"]) 
    numMessages = len(popMail.list()[1])
    emailsFound = []

    for i in range(numMessages):                    # in new messages
        returnAddress = ""
        subject = ""

        try:
            for msg in popMail.retr(i+1)[1]:            # in each POP line
                m = str(msg)
                if m.startswith("b'Return-Path: <"):    # if there is a return address
                    returnAddress = m[16:-2]            # get returnAddress
                if m.startswith("b'Subject:"):          # if there is a subject
                    subject = m[11:-1]                  # get subject
            
            print("Found email from:", returnAddress, "With the subject:", subject)
            if subject in config["reportCodes"]:        # if a report code has been sent as email subject, it's a valid email
                emailsFound.append(returnAddress)       # add to list of addresses to email back
        
        except: logError("Logged in okay but could not get emails in" + str(popMail.list()[1]))

    popMail.quit()
    return emailsFound
    

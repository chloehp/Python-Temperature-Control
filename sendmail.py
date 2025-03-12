import smtplib
from email.message import EmailMessage
from time import sleep
import temphumid

#Set the sender email and password and recipient email

def generateSVG(stringDate):
    print("generate SVG graphs of temperature and humidity from the last 24 hours")
    openTempGraphSVG = open("temperature-graph.svg", "r")       # open the template for temperature graph
    tempGraph = openTempGraphSVG.read()                         # 
    openTempGraphSVG.close()                                    #
    
    # new path for humidity
    hPath = "<path style='fill:none;stroke:#5cbed0;stroke-width:0.79375;stroke-linecap:square;paint-order:stroke fill markers' d='M "
    for item in temphumid.logList:                              # for each dict in the list
                                                                # get x plot (time) and y plot (temperature)
        xPlot = str((item["time"] * 10) + 15)                   # 00:00 is at x="15", 24:00 is at x="255"
        yPlot = str(204 - (item["humid"] * 1.8))                # 0% is at y="204", 100% is at y="24", 1% = 1.8
        hPath += xPlot + "," + yPlot + " "                      # add cordinates        
    hPath += "' id='path3'/>"                                   # close new path
    
    # new path for temperature
    tPath = "<path style='fill:none;stroke:#ff0000;stroke-width:0.79375;stroke-linecap:square;paint-order:stroke fill markers' d='M "
    for item in temphumid.logList:                              # for each dict in the list
                                                                # get x plot (time) and y plot (temperature)
        xPlot = str((item["time"] * 10) + 15)                   # 00:00 is at x="15", 24:00 is at x="255"
        yPlot = str(204 - (item["temp"] * 3.6))                 # 0°C is at y="204", 50°C is at y="24", 1°C = 3.6
        tPath += xPlot + "," + yPlot + " "                      # add cordinates        
    tPath += "' id='path4'/>"                                   # close new path

    newTempGraph = tempGraph[:-6] + hPath + tPath + tempGraph[-6:]    # slice the new path into the SVG template
    stringDate = stringDate.replace(":", "-")
    stringDate = stringDate.replace(" ", "_")
    newTempGraphSVG = open("graphs/temperature" + stringDate + ".svg", "x")
    newTempGraphSVG.write(newTempGraph)                         # create new SVG graph
    newTempGraphSVG.close()                                     #
    return newTempGraph                                         # return the graph

emailAttempts = 1
def sendMail(config, stringDate, svg):
    global emailAttempts
    print("Send email. Attempt:", emailAttempts, "/ 3")
    
    emailBody = f"""
    Sent from {config["location"]} on {stringDate}
    {svg}
    Rawdata:
    {str(temphumid.logList)}"""

    try:
        # Code from: https://RandomNerdTutorials.com/raspberry-pi-send-email-python-smtp-server/
        # Create a message object
        msg = EmailMessage()
        # Set the email body
        msg.set_content(emailBody)
        # Set sender and recipient
        msg['From'] = config["emailAddress"]
        msg['To'] = config["sendTo"]
        # Set your email subject
        msg['Subject'] = config["title"]

        # Connecting to server and sending email
        # Edit the following line with your provider's SMTP server details
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Comment out the next line if your email provider doesn't use TLS
        server.starttls()
        # Login to the SMTP server
        server.login(config["emailAddress"], config["emailPass"])

        # Send the message
        server.send_message(msg)
        print('Email sent')
        #Disconnect from the Server
        server.quit()
        emailAttempts = 1
    
    except:
        print('Could not send email')
        errorLog = open("errorlog.txt", "a")
        errorLog.write("Could not send email. Attempt " + str(emailAttempts) + ". :" + stringDate + "\n")
        errorLog.close()

        if emailAttempts < 3:
            print("Trying again in 1 minute")
            emailAttempts += 1
            sleep(60)
            sendMail(config, stringDate, svg)
        else:
            print("Failed to send email, giving up")
            emailAttempts = 1
import smtplib
from email.message import EmailMessage
from time import sleep
from email.mime.text import MIMEText

import temphumid
import utility

# start of svg path string
def pathStart(colour, width = "0.79375"): return f"""<path style='fill:none;stroke:{colour};stroke-width:{width};stroke-linecap:none;paint-order:stroke fill markers' d='M """
    
def generateSVG(stringDate, highTemp, lowTemp):
    print("generate SVG graphs of temperature and humidity from the last 24 hours")
    openGraphSVG = open("graph-template.svg", "r")              # get the template for the graph
    graph = openGraphSVG.read()                         
    openGraphSVG.close()                                    

    highTempPath = ""
    lowTempPath = ""
    if isinstance(highTemp, (int, float)) and isinstance(lowTemp, (int, float)):                                    # if highTemp and lowTemp exist and are numbers
        highTempYPlot = str(204 - (highTemp * 3.6))                                                                 # 0°C is at y="204", 50°C is at y="24", 1°C = 3.6
        lowTempYPlot = str(204 - (lowTemp * 3.6))                                                                   # 0°C is at y="204", 50°C is at y="24", 1°C = 3.6
        highTempPath = f"""{pathStart("#4d4d4d", "0.265")}15,{highTempYPlot} 255,{highTempYPlot}' id='path3'/>"""   # draw line for high temperature
        lowTempPath = f"""{pathStart("#4d4d4d", "0.265")}15,{lowTempYPlot} 255,{lowTempYPlot}' id='path4'/>"""      # draw line for low temperature
    
    previousTime = 0
    hPath = pathStart("#5cbed0")                # new path for humidity, give line colour
    for item in temphumid.logList:              # for each dict in the list
        if item["h%"] == -999: continue         # if bad data, skip in graph
        dTime = item["H"] + (item["M"] / 60)    # get time as decimal (hour + min/60)
        if dTime < previousTime: continue       # if time is less than previous loop, skip in graph
        else: previousTime = dTime              # set 'previous time' for next loop
        xPlot = str((dTime * 10) + 15)          # get x plot (time): 00:00 is at x="15", 24:00 is at x="255"
        yPlot = str(204 - (item["h%"] * 1.8))   # and y plot (humidity): 0% is at y="204", 100% is at y="24", 1% = 1.8
        hPath += xPlot + "," + yPlot + " "      # add cordinates        
    hPath += "' id='path5'/>"                   # close new path
    
    previousTime = 0
    tPath = pathStart("#ff0000")                # new path for temperature, give line colour
    for item in temphumid.logList:              # for each dict in the list
        if item["tC"] == -999: continue         # if bad data, skip in graph
        dTime = item["H"] + (item["M"] / 60)    # get time as decimal
        if dTime < previousTime: continue       # if time is less than previous loop, skip in graph
        else: previousTime = dTime              # set 'previous time' for next loop
        xPlot = str((dTime * 10) + 15)          # get x plot (time)
        yPlot = str(204 - (item["tC"] * 3.6))   # and y plot (temperature): 0°C is at y="204", 50°C is at y="24", 1°C = 3.6
        tPath += xPlot + "," + yPlot + " "      # add cordinates        
    tPath += "' id='path6'/>"                   # close new path

    newGraph = graph[:-6] + highTempPath + lowTempPath + hPath + tPath + graph[-6:]     # slice the new path into the SVG template
    stringDate = stringDate.replace(":", "-")                                           # make filename friendly
    stringDate = stringDate.replace(" ", "_")                                           # make filename friendly
    fileName = stringDate + ".svg"                                                      # make filename
    newGraphSVG = open("graphs/" + fileName, "x")
    newGraphSVG.write(newGraph)                                                         # create new SVG graph
    newGraphSVG.close()                                     
    print("New graph at: graphs/" + fileName)
    return fileName                                                                     # return the graph


emailAttempts = 0
def sendMail(to, config, stringDate, svg):
    global emailAttempts
    emailAttempts += 1
    print("Send email to:", to, " Attempt:", emailAttempts, "/ 3")
    
    stringLogList = str(temphumid.logList)
    htmlLogList = "<tr><th>Time</th><th>Temperature</th><th>Humidity</th></tr>"     # format string into html table
    for log in temphumid.logList:                                                   # from each log in list
        logTemp = "<td>" + str(log["tC"]) + "°C</td>"                               # get temperature
        logHum = "<td>" + str(log["h%"]) + "%</td>"                                 # get humidity
        logClock = f"""<td>{log["H"]:02d}:{log["M"]:02d}</td>"""                    # get time - format: HOURS:MINUTES (with leading zero)
        htmlLogList += f"""<tr>{logClock}{logTemp}{logHum}</tr>"""                  # format string into html table

    # text email body
    emailBody = f"""
        {config["message"]}

        Data:
        {stringLogList}
    """
    # html email body
    htmlBody = MIMEText(f"""
    <html>
        <head><style> td, th {"{ border: 1px solid black; padding: 8px; }"} </style></head>
        <body>
            <div style="width: 90%; max-width: 600px; margin: auto;">
                <p>{config["message"]}</p><br>
                <p style="text-align: center;font-weight: bold;">Temperature and humidity table:</p>
                <table style="border-collapse: collapse;width: 100%;">{htmlLogList}</table><br>
            </div>
        </body>
    </html>
    """, "html")

    svgFile = utility.getAttachment("graphs/" + svg)
    logFile = utility.getAttachment("log.json")

    try:
        msg = EmailMessage()                                        # Create a message object
        msg.set_content(emailBody)                                  # Set the email body
        msg.add_alternative(htmlBody)                               # Set the HTML email body
        if svgFile:                                                 # If there is a graph to send
            msg.add_attachment(svgFile, maintype = "text", subtype = "plain", filename = "graph-" + svg + ".html")  # Attach graph as html file
        if logFile:                                                 # If there is a log to send
            msg.add_attachment(logFile, maintype = "text", subtype = "plain", filename = "Rawdata.json")            # Attach log.json
        msg['From'] = config["emailAddress"]                        # set email sender
        msg['To'] = to                                              # set email recipient
        msg['Subject'] = config["title"] + " : " + stringDate       # set email title

        # Connecting to server and sending email
        server = smtplib.SMTP(config["smtpDomain"], config["smtpPort"]) # emailprovider's SMTP server details        
        server.starttls()                                               # Comment out if email provider doesn't use TLS
        server.login(config["emailAddress"], config["emailPass"])       # Login to the SMTP server

        server.send_message(msg)        # Send the message
        server.quit()                   # Disconnect from the Server
        emailAttempts = 0               # reset email attempts
        print('Email sent')
    
    except:
        print('Could not send email')
        utility.logError("Could not send email. Attempt " + str(emailAttempts))

        if emailAttempts < 3:
            print("Trying again in 1 minute")
            sleep(60)
            sendMail(config, stringDate, svg)       # try again
        else:
            print("Failed to send email, giving up")
            emailAttempts = 0                       # reset email attempts
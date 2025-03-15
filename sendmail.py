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
    if isinstance(highTemp, (int, float)) and isinstance(lowTemp, (int, float)):                                    # if highTemp and lowTemp are numbers
        highTempYPlot = str(204 - (highTemp * 3.6))
        lowTempYPlot = str(204 - (lowTemp * 3.6))
        highTempPath = f"""{pathStart("#4d4d4d", "0.265")}15,{highTempYPlot} 255,{highTempYPlot}' id='path3'/>"""   # draw line for high temperature
        lowTempPath = f"""{pathStart("#4d4d4d", "0.265")}15,{lowTempYPlot} 255,{lowTempYPlot}' id='path4'/>"""      # draw line for low temperature
    
    hPath = pathStart("#5cbed0")                                # new path for humidity
    for item in temphumid.logList:                              # for each dict in the list
                                                                # get x plot (time) and y plot (humidity)
        xPlot = str((item["time"] * 10) + 15)                   # 00:00 is at x="15", 24:00 is at x="255"
        yPlot = str(204 - (item["humid"] * 1.8))                # 0% is at y="204", 100% is at y="24", 1% = 1.8
        hPath += xPlot + "," + yPlot + " "                      # add cordinates        
    hPath += "' id='path5'/>"                                   # close new path
    
    tPath = pathStart("#ff0000")                                # new path for temperature
    for item in temphumid.logList:                              # for each dict in the list
                                                                # get x plot (time) and y plot (temperature)
        xPlot = str((item["time"] * 10) + 15)                   # 00:00 is at x="15", 24:00 is at x="255"
        yPlot = str(204 - (item["temp"] * 3.6))                 # 0°C is at y="204", 50°C is at y="24", 1°C = 3.6
        tPath += xPlot + "," + yPlot + " "                      # add cordinates        
    tPath += "' id='path6'/>"                                   # close new path

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
def sendMail(config, stringDate, svg):
    global emailAttempts
    emailAttempts += 1
    print("Send email. Attempt:", emailAttempts, "/ 3")
    
    stringLogList = "[<br>\n"
    for item in temphumid.logList:
        stringLogList += str(item) + "<br>\n"
    stringLogList += "]"

    emailBody = f"""
        {config["message"]}

        Rawdata:
        {stringLogList}
    """
    htmlBody = MIMEText(f"""
    <html>
        <head></head>
        <body>
            <div style="width: 90%; max-width: 600px; margin: auto;">
                <p>{config["message"]}</p><br>
                <p>Rawdata:</p><br>
                <code>{stringLogList}</code><br>
            </div>
        </body>
    </html>
    """, "html")

    svgFile = ""
    if len(svg) > 0: 
        try:
            svfFileOpen = open("graphs/" + svg, "rb")
            svgFile = svfFileOpen.read()
            svfFileOpen.close()
        except: 
            svgFile = ""
            utility.logError("Could not get graph.")


    try:
        msg = EmailMessage()                                        # Create a message object
        msg.set_content(emailBody)                                  # Set the email body
        msg.add_alternative(htmlBody)                               # Set the HTML email body
        if len(svgFile) > 0:                                        # If there is a graph to send
            msg.add_attachment(svgFile, maintype = "text", subtype = "plain", filename = "graph-" + svg + ".html")    # Attach graph as html file
        msg['From'] = config["emailAddress"]                        # set email sender
        msg['To'] = config["sendTo"]                                # set email recipient
        msg['Subject'] = config["title"] + " : " + stringDate       # set email title

        # Connecting to server and sending email
        server = smtplib.SMTP('smtp.gmail.com', 587)                # emailprovider's SMTP server details        
        server.starttls()                                           # Comment out if email provider doesn't use TLS
        server.login(config["emailAddress"], config["emailPass"])   # Login to the SMTP server

        server.send_message(msg)        # Send the message
        print('Email sent')
        server.quit()                   # Disconnect from the Server
        emailAttempts = 0               # reset email attempts
    
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
import smtplib
from email.message import EmailMessage
import temphumid

#Set the sender email and password and recipient email

def genTempSVG():
    print("generate SVG graphs of temperature and humidity from the last 24 hours")
    newPath = "<path style='fill:none;stroke:#ff0000;stroke-width:0.79375;stroke-linecap:square;paint-order:stroke fill markers' d='M "
    
    for item in temphumid.tempHumidList:
        xPlot = str((item["time"] * 10) + 15)                                   # 00:00 is at x="15", 24:00 is at x="255"
        yPlot = str(204 - (item["temp"] * 3.6))                                 # 0°C is at y="204" , 50°C is at y="24", 1°C = 3.6
        newPath += xPlot + "," + yPlot + " "
        
    newPath += "' id='path3'/>"                                             # close new path
    print(newPath)


def sendMail(config, stringDate, svgData):
    print("Send eMail")
    
    emailBody = f"""
    Sent from pi on {stringDate}
    Rawdata:
    {str(temphumid.tempHumidList)}"""

    # Code from: https://RandomNerdTutorials.com/raspberry-pi-send-email-python-smtp-server/

    # Create a message object
    msg = EmailMessage()

    # Set the email body
    msg.set_content(emailBody)
    #msg.add_attachment(svgData, maintype='image', subtype='svg')

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
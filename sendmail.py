import smtplib
from email.message import EmailMessage
from datetime import datetime
import json
from temphumid import tempHumidList

#Set the sender email and password and recipient email
from_email_addr ="REPLACE_WITH_THE_SENDER_EMAIL"
from_email_pass ="REPLACE_WITH_THE_SENDER_EMAIL_APP_PASSWORD"
to_email_addr ="REPLACE_WITH_THE_RECIPIENT_EMAIL"
emailBody = f"""
Sent from pi on {str(datetime.now())}
Rawdata:
{json.dumps(tempHumidList)}"""

def genSVG():
    print("generate SVG graphs of temperature and humidity from the last 24 hours")
    tempHumidList.clear()                                   # clear days list (and log.json)

def sendMail():
    print("Send eMail")

    # Code from: https://RandomNerdTutorials.com/raspberry-pi-send-email-python-smtp-server/

    # Create a message object
    msg = EmailMessage()

    # Set the email body
    msg.set_content(emailBody)
    #msg.add_attachment(svgDat, maintype='image', subtype='svg')

    # Set sender and recipient
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    # Set your email subject
    msg['Subject'] = 'TEST EMAIL'

    # Connecting to server and sending email
    # Edit the following line with your provider's SMTP server details
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Comment out the next line if your email provider doesn't use TLS
    server.starttls()
    # Login to the SMTP server
    server.login(from_email_addr, from_email_pass)

    # Send the message
    server.send_message(msg)

    print('Email sent')
    #Disconnect from the Server
    server.quit()
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

load_dotenv()

TO_MAIL = os.getenv("TO_MAIL")
FROM_MAIL = os.getenv("FROM_MAIL")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


def send_email(subject,content,to_email,from_email,password):
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(from_email, password)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    # Send the email
    server.send_message(msg)
    server.quit()

def send(subject,content):
    send_email(subject, content, to_email=TO_MAIL, from_email=FROM_MAIL, password=MAIL_PASSWORD)


def send_image_mail(msg,to_email, from_email, password):
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(from_email, password)

    msg['From'] = from_email
    msg['To'] = to_email


    # Send the email
    server.send_message(msg)
    server.quit()

def sendImageMail(msg):
   send_image_mail(msg,to_email=TO_MAIL, from_email=FROM_MAIL, password=MAIL_PASSWORD)





def check():
    send("Testing Mail Functionality","This is a testing mail to check wheather the mail functionality is working perfectly or not")



#check()
import paramiko
import logging
import csv
from datetime import datetime
from mail import sendImageMail
from mail_composer import MailComposer
from image import getImageFromText
from tableBuilder  import TableBuilder
from extractor import extractActiveStatus
today = datetime.now()
date_str = today.strftime('%Y-%m-%d')



# Create a custom logger
logger = logging.getLogger('Health Checker')
logger.setLevel(logging.DEBUG)

# Create a file handler for logging to a file
file_handler = logging.FileHandler('my_log.log')
file_handler.setLevel(logging.INFO)  # Set file handler to log only INFO and higher

# Create a console handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set console handler to log all messages

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

file = csv.reader(open("servers.csv","r"))
logger.info("opened servers.csv file")

outputfile = open(date_str+"_health_check.txt","w",encoding='utf-8')
logger.info("created an output file")
next(file)

mail_composer = MailComposer()
table_builder = TableBuilder()
mail_composer = mail_composer.addSubject(date_str+"_health_check")

for server in file:
    server_name = server[0]
    server_ip = server[1]
    user_name = server[2]
    password = server[3]
    services = server[4].split(",")

    ssh.connect(server_ip,22,user_name,password)
    logger.info("connected to the" + server_name)

    for service in services:
        logger.info("checking the status of " + service)
        stdin,stdout,stderr = ssh.exec_command("sudo systemctl status "+service)
        #print("SERVER: ",server_name)
        service_status = stdout.read().decode()
        #print(type(service_status))

        

        new_line = "\n"

        outputfile.write("SERVER_NAME: " + server_name)
        outputfile.write("\n")
        outputfile.write("SERVER_IP: " + server_ip)
        outputfile.write("\n")
        outputfile.write("SERVICE: " + service)
        outputfile.write("\n")
        outputfile.write("\n")

        outputfile.write(service_status)
        outputfile.write("\n")
        outputfile.write("\n")

        logger.info("written the status info into the output file")

        server_details = ""

        server_details += "SERVER_NAME: " + server_name + new_line
        server_details += "SERVER_IP: " + server_ip + new_line
        server_details += "SERVICE: " + service + new_line


        active_status = extractActiveStatus(service_status)
        table_builder.addRow(server_ip,service,active_status)

        image = getImageFromText(service_status,service+".png")
        logger.info("Got image of service status")

        mail_composer = mail_composer.addImage(image,service+"image",server_details)
        logger.info("Added image to the mail")
        

    ssh.close()

    logger.info("Disconnected form "+ server_name)



outputfile.close()
logger.info("closed the output file")
table = table_builder.build()
mail_composer = mail_composer.addTable(table)
msg = mail_composer.build()
sendImageMail(msg)
logger.info("Sent the email")

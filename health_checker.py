import paramiko
import logging
import csv
import os
from datetime import datetime
from mail.mail import sendImageMail
from mail.mail_composer import MailComposer
from utils.image import getImageFromText
from mail.tableBuilder  import TableBuilder
from utils.extractor import extractActiveStatus


kill = False
today = datetime.now()
date_str = today.strftime('%Y-%m-%d')

log_folder_name = 'logs'
log_file_path = os.path.join(log_folder_name, f'{date_str}.log')

if not os.path.exists(log_folder_name):
    os.makedirs(log_folder_name)

# Create a custom logger
logger = logging.getLogger('Health Checker')
logger.setLevel(logging.DEBUG)

# Create a file handler for logging to a file
file_handler = logging.FileHandler(log_file_path)
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

screen_shot_folder_name = 'screenshots'

if not os.path.exists(screen_shot_folder_name):
    os.makedirs(screen_shot_folder_name)

report_folder_name = 'reports'
if not os.path.exists(report_folder_name):
    os.makedirs(report_folder_name)

report_file = os.path.join(report_folder_name,f'{date_str}_health_check.txt')


config_folder = 'config'
servers_list_filename = 'servers.csv'
servers_list_file = os.path.join(config_folder,servers_list_filename)

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

file = csv.reader(open(servers_list_file,"r"))
logger.info("opened servers.csv file")

outputfile = open(report_file,"w",encoding='utf-8')
logger.info("created an output file")
next(file)

mail_composer = MailComposer()
table_builder = TableBuilder()
mail_composer = mail_composer.addSubject(date_str+"_health_check")

for server in file:
    try:
        server_name = server[0]
        server_ip = server[1]
        user_name = server[2]
        password = server[3]
        services = server[4].split(",")
        type = server[5]
    except IndexError:
        logger.error("There is some issues with the structurs of servers.csv file(please refer to the servers_dummy.csv for clarity)")
        logger.warning("Stopping the health check")
        kill = True
        break    

    try:
        ssh.connect(server_ip,22,user_name,password)
        logger.info("connected to the " + server_name)
    except TimeoutError:
        logger.error(server_ip + " is Not reachable(please check wheather the server is online or not)")
        continue
    except paramiko.AuthenticationException:
        logger.error("Authentication failed for " + server_ip + " (please check wheather the login credentials are correct or not)")
        continue


    if type == "status":
        for service in services:
            logger.info("checking the status of " + service)
            stdin,stdout,stderr = ssh.exec_command("sudo systemctl status "+service)
          
            service_status = stdout.read().decode()
            err_response = stderr.read().decode()

            #print("STDOUT" + service_status)
            #print("STDERR" + err_response)
            if(len(service_status)==0):
                logger.error(err_response + f" (Please check whether there is a service with the name {service} in {server_ip} )")
                continue


            new_line = "\n"

            server_details = new_line

            server_details += "SERVER_NAME: " + server_name + new_line
            server_details += "SERVER_IP: " + server_ip + new_line
            server_details += "SERVICE: " + service + new_line

            outputfile.write(server_details)
            outputfile.write(new_line)

            outputfile.write(service_status)
            outputfile.write(new_line)

            logger.info("written the status to the output file")

            active_status = extractActiveStatus(service_status)
            table_builder.addRow(server_ip,service,active_status)

            image = getImageFromText(service_status,server_ip + service+".png")
            logger.info("Got image of service status")

            mail_composer = mail_composer.addImage(image,service+"image",server_details)
            logger.info("Added image to the mail")

        ssh.close()
        logger.info("Disconnected form "+ server_name)

    elif type == "space":
        logger.info("checking filesystem utilization of " + server_ip)
        stdin,stdout,stderr = ssh.exec_command("df -h")
        
        response = stdout.read().decode()
        err_response = stderr.read().decode()

        image = getImageFromText(response,server_ip+".png")
        logger.info("Got image of filesystem utilization")

        server_details = "SERVER_NAME: " + server_name + new_line
        server_details += "SERVER_IP: " + server_ip + new_line
        server_details += "Type: File System Utilization" + new_line 

        outputfile.write(server_details)
        outputfile.write(new_line)
        outputfile.write(response)
        outputfile.write(new_line)

        mail_composer = mail_composer.addImage(image,server_ip+"image",server_details)
        logger.info("Added image to the mail")

    else:
        logger.error(f"Type of check is unrecognized (please check for spelling mistakes for {server_ip})")

outputfile.close()
logger.info("closed the output file")

if not kill:
    table = table_builder.build()
    mail_composer = mail_composer.addTable(table)
    msg = mail_composer.build()
    sendImageMail(msg)
    logger.info("Sent the email")

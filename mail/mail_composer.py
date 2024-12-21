from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import uuid

from .mail import sendImageMail


class MailComposer:
    
    def __init__(self):
        self.msg = MIMEMultipart()
        self.servers = []
        self.images = []
        self.table = None

    def addTable(self,table):
        #self.msg.attach(MIMEText(table, 'html'))
        self.table = MIMEText(table, 'html')
        return self

    def addSubject(self,subject):
        self.msg['Subject'] = subject
        return self 
    
    def addFromMailId(self,from_email_id):
        self.msg['From'] = from_email_id
        return self

    def addToMailId(self,to_email_id):
        self.msg['To'] = to_email_id
        return self


    def addImage(self, image_data, image_name, matter):
        # Generate a unique Content-ID
        unique_id = str(uuid.uuid4())
        content_id = f"image_{unique_id}"

        html = f"""
        <html>
            <body>
                <p>{matter}</p>
                <img src="cid:{content_id}">
            </body>
        </html>"""

        # Attach the HTML content
        #self.msg.attach(MIMEText(html, 'html'))

        self.servers.append(MIMEText(html, 'html'))

        # Embed the image with the unique Content-ID
        image = MIMEImage(image_data, name=image_name)
        image.add_header('Content-ID', f'<{content_id}>')  # Unique Content-ID
        image.add_header('Content-Disposition', 'inline')
        self.images.append(image)
        #self.msg.attach(image)
        return self

    def build(self):
        self.msg.attach(self.table)

        for i in range(len(self.servers)):
            self.msg.attach(self.servers[i])
            self.msg.attach(self.images[i])
            
        return self.msg
    

def check():
    mailcomposer = MailComposer()
    image  = open("image.png","rb").read()
    msg = mailcomposer.addImage(image,"sample image","status of the production server1").addSubject("Testing  Mail(Multimedia)").build()
    sendImageMail(msg)


#check()



    
           
            

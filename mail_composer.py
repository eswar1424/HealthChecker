from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from mail import sendImageMail


class MailComposer:
    msg = MIMEMultipart()
    def __init__(self):
        #print("intiating the mail composer")
        pass


    def addTable(self,table):
        self.msg.attach(MIMEText(table, 'html'))
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

    
    def addImage(self,image_data,image_name,matter):
        html = """
            <html>
                <body>
                    <p>"""+matter+"""</p>
                <img src="cid:image1">
                </body>
            </html>"""

        self.msg.attach(MIMEText(html, 'html'))

        image = MIMEImage(image_data, name=image_name)
        image.add_header('Content-ID', '<image1>')
        image.add_header('Content-Disposition', 'inline')
        self.msg.attach(image)
        return self
    
    def build(self):
        return self.msg
    

def check():
    mailcomposer = MailComposer()
    image  = open("image.png","rb").read()
    msg = mailcomposer.addImage(image,"sample image","status of the production server1").addSubject("Testing  Mail(Multimedia)").build()
    sendImageMail(msg)


#check()



    
           
            

import collections
import smtplib, ssl
from email.message import EmailMessage

# subtypes can be found here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types

class Secrets:
    outputFilePath = ''
    senderEmail=''
    senderEmailPassword=''
    receiverEmails=[]
    EmailCredentials = collections.namedtuple("EmailCredentials", ['password', 'sender', 'recipients'])

    @staticmethod
    def sendEmail(filePathComplete: str, fileName: str, email, subject:str, msg:str, subtype=''):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            try:
                server.login(email.sender, email.password)
                for recipient in email.recipients:
                    # must create a new EmailMessage object for every recipient
                    message = EmailMessage()
                    message['From'] = email.sender
                    message['To'] = recipient
                    message['Subject'] = subject
                    message.set_content(msg)
                    if filePathComplete and fileName:
                        with open(filePathComplete, 'rb') as f:
                            fileData = f.read()
                        message.add_attachment(fileData, maintype="application", subtype=subtype, filename=fileName)
                    server.send_message(message)
                print('email sent!')
            except Exception as e:
                print(e)
                print("could not login or send the mail.")



import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import date
from configparser import ConfigParser
import sys



def setup():
    setup_file = Path("config.ini")
    if not setup_file.is_file():
        parser = ConfigParser()
        parser.read("config.ini")
        emailto =  parser.get("settings", "mail")
        filename = "data.csv"
        username = parser.get("settings", "mail")
        password = parser.get("settings", "password")
        if username and password:
                    print('Please provide email and password, run setup.py')
                    sys.exit(0)


def sendemail():

    today = date.today()

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = emailto
    msg["Subject"] = f'vinted bot {today}'

    # motified
    # https://stackoverflow.com/questions/23171140/how-do-i-send-an-email-with-a-csv-attachment-using-python
    
    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(filename)
        
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(filename, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(filename, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(filename, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(username, emailto, msg.as_string())
    server.quit()




def main():
    sende_mail()

if __name__ == '__main__':
    main()
import json
import smtplib
import uuid
import os
import glob

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


class TempImage:
	def __init__(self, basePath="./", ext=".jpg"):
		self.path = "{base_path}/{rand}{ext}".format(base_path=basePath,
			rand=str(uuid.uuid4()), ext=ext)

	def cleanup(self):
		os.remove(self.path)


def send_email():
    fromaddr = "ballanarehell@gmail.com"
    toaddrs = "g.karaboychev@gmail.com"
    print("[INFO] Emailing to {}".format(fromaddr))
    text = 'Intruder'
    subject = 'Security Alert!!'
    message = 'Subject: {}\n\n{}'.format(subject, text)

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    files = glob.glob("/tmp/talkingraspi*")
    for f in files:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    username = "ballanarehell@gmail.com"
    password = "123456"

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()



def send_mail(files=None,
              ):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))



    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

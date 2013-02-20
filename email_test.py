import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os


def get_info():
    with open(os.environ["HOME"] + '.google_file') as f:
        for line in f:
            k, v = line.split(':')
            if k == 'google_pw':
                gmail_pwd = v
            else:
                gmail_user = v
    return gmail_user, gmail_pwd


def mail(to, subject, text, attach):
    gmail_user, gmail_pwd = get_info()
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

mail("some.person@some.address.com",
   "Hello from python!",
   "This is a email sent with python",
   "my_picture.jpg")

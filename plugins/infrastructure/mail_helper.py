from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import smtplib
import os
import logging
logger = logging.getLogger(__name__)

def send_email(sender, recipient, subject, content, ishtml = False, attachment=None):

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] =  recipient
    msg['Subject'] = subject

    if ishtml:
        msg.attach(MIMEText((content), ('html')))
    else:
        msg.attach(MIMEText((content), ('plain')))

    if attachment is not None:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
        msg.attach(part)


    server = smtplib.SMTP('smtp.1and1.pl', 587)
    text = msg.as_string()
    # identify ourselves, prompting server for supported features
    server.ehlo()
    # If we can encrypt this session, do it
    if server.has_extn('STARTTLS'):
        server.starttls()
        server.ehlo() # re-identify ourselves over TLS connection

    server.login('robot@sigma-solutions.eu', 'robot@sigma2016')
    server.sendmail(sender, recipient, text)
    server.quit()

# send email to notify failures
def send_notify_email(subject, content):
    # recipients = ["mobience@spicymobile.pl", "it@spicymobile.pl", "kszczuka@sigma-solutions.eu", "tuyenlq@sigma-solutions.eu", "cuongnv@sigma-solutions.eu", "cuongbn@sigma-solutions.eu"]
    recipients = ["thuongln@sigma-solutions.eu", "tuyenlq@sigma-solutions.eu", "tung@sigma-solutions.eu", "cuongbn@sigma-solutions.eu", "it@spicymobile.pl"]
    try:
        for r in recipients:
            send_email("importer@sigma-solutions.eu", r, subject, content)
    except Exception as e:
        logger.error("send email to notify ERROR")


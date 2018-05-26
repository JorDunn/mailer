import smtplib
from email.headerregistry import Address
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from mailer.config import Config
from mailer.models import Queue


class EmailManager(object):

    receiver: str = None
    sender: str = None
    body: MIMEMultipart = None

    def __init__(self) -> None:
        self.sender = str(Address(
            Config.EMAIL['display'], Config.EMAIL['username'], Config.EMAIL['domain']))
        print("Hello, I'm ", self.sender)

    def construct_email(self, queue_id: int) -> None:
        customer, template = QueueManager.get_queue_item(queue_id)
        msg = MIMEMultipart()
        with open(str(Path.cwd()) + '/mailer/mjml/base.html', 'r') as f:
            html = f.read()
        html = html.replace('{template_content}', template.body)
        html = html.replace('{0}', customer.first_name)
        msg.attach(MIMEText(html, 'html'))
        self.receiver = customer.email
        msg['Subject'] = template.name.replace('{0}', customer.first_name)
        msg['From'] = self.sender
        msg['To'] = self.receiver
        self.body = msg

    def send(self, debuglevel: int=0) -> None:
        try:
            print("Trying to send an email to {}...".format(self.receiver), end='')
            server = smtplib.SMTP_SSL(host=Config.EMAIL['host'], port=Config.EMAIL['port'])
            server.set_debuglevel(debuglevel)
            # If you are using gmail, this requires an app specific passwords
            server.login('{0}@{1}'.format(
                Config.EMAIL['username'], Config.EMAIL['domain']), Config.EMAIL['password'])
            server.sendmail(from_addr=self.sender, to_addrs=self.receiver, msg=self.body.as_string())
            print("complete!")
        except Exception as err:
            print(err)

import smtplib
from pprint import pprint
from email.message import EmailMessage
from email.headerregistry import Address

from pony.orm import db_session

from mailer.models.queue import QueueManager
from mailer.models.templates import TemplateManager
from mailer.models.customers import CustomerManager
from mailer.config import Config


class EmailManager(object):

    sender: str = None
    email = None

    def __init__(self):
        self.sender = Address(
            Config.EMAIL['display'], Config.EMAIL['username'], Config.EMAIL['domain'])

    def construct_email(self, queue_id: int):
        email = EmailMessage()
        email['From'] = self.sender
        html = """
        <html>
            <head></head>
            <body>
            {template_content}
            </body>
        </html>"""
        customer, template = QueueManager.get_queue_item(queue_id)
        html = html.replace("{template_content}", template.body)
        email['Subject'] = template.name.replace("{0}", customer.first_name)
        html = html.replace("{0}", customer.first_name)
        email['To'] = customer.email
        self.email = email
        pprint(email)

    def send(self):
        pass

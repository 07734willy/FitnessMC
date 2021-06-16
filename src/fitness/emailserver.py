from email.parser import BytesParser
from smtpd import SMTPServer
from base64 import b64decode

import asyncio
import asyncore
import os

from .csvhandler import handle_csv

IP_ADDRESS = os.getenv("FITNESSMC_MAIL_IP_ADDRESS")

TARGET_SUBJECT = ""
TARGET_SENDER = ""
TARGET_RCPT_NAME = "fitnessmc"

class EmailServer(SMTPServer):
	def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
		parser = BytesParser()
		message = parser.parsebytes(data)
		
		subject = message.get("Subject")

		if len(rcpttos) != 1:
			return

		rcpt_name = rcpttos[0].split("@", 1)[0]
		if rcpt_name != TARGET_RCPT_NAME:
			return
		
		"""
		if subject != TARGET_SUBJECT or mailfrom != TARGET_SENDER:
			return
		"""

		for part in message.walk():
			if part.get_content_disposition() == 'attachment':
				attachment_data = b64decode(part.get_payload())
				attachment_text = attachment_data.decode('utf-8')

				handle_csv(attachment_text)

	def bind(self, *args, **kwargs):
		print("Email server started")
		super().bind(*args, **kwargs)

SERVER = EmailServer((IP_ADDRESS, 25), None)

def start_email_server():
	asyncore.loop()

def stop_email_server():
	SERVER.close()

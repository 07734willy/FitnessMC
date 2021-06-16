from email.parser import BytesParser
from smtpd import SMTPServer
from base64 import b64decode

import asyncio
import asyncore

from .csvhandler import handle_csv

TARGET_SUBJECT = ""
TARGET_SENDER = ""

class EmailServer(SMTPServer):
	def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
		parser = BytesParser()
		message = parser.parsebytes(data)
		
		subject = message.get("Subject")
		if subject != TARGET_SUBJECT or mailfrom != TARGET_SENDER:
			return

		#print(peer, mailfrom, rcpttos)

		for part in message.walk():
			if part.get_content_disposition() == 'attachment':
				attachment_data = b64decode(part.get_payload())
				attachment_text = attachment_data.decode('utf-8')

				asyncio.run(handle_csv(attachment_text))

			# print(part.get_content_disposition())

	def bind(self, *args, **kwargs):
		print("Email server started")
		super().bind(*args, **kwargs)

SERVER = EmailServer(('localhost', 1025), None)

def start_email_server():
	asyncore.loop()

def stop_email_server():
	SERVER.close()

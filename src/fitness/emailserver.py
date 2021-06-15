from email.parser import BytesParser
from smtpd import SMTPServer
from base64 import b64decode

class EmailServer(SMTPServer):
	def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
		parser = BytesParser()
		message = parser.parsebytes(data)

		print(message.get("From"))
		print(message.get("To"))
		print(message.get("Subject"))
		print(message.get("Date"))

		print(peer, mailfrom, rcpttos)

		print(list(message.items()))
		
		for part in message.walk():
			if part.get_content_disposition() == 'attachment':
				attachment_data = b64decode(part.get_payload())
				attachment_text = attachment_data.decode('utf-8')
				print(attachment_text)

			print(part.get_content_disposition())

def main():
	EmailServer(('localhost', 1025), None)
	import asyncore

	try:
		asyncore.loop()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()

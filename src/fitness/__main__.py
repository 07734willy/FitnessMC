from .discordlink import start_discord_client, stop_discord_client
from .emailserver import start_email_server, stop_email_server
import asyncio

def main():
	try:
		start_discord_client()
		start_email_server()
	except KeyboardInterrupt:
		stop_discord_client()
		stop_email_server()

if __name__ == "__main__":
	main()

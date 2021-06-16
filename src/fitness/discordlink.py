from discord import Client, Intents
from threading import Thread
import asyncio
import os

TOKEN = os.getenv("FITNESSMC_DISCORD_TOKEN")

UPDATES_CHANNEL_ID = 854509811584598067

class CustomClient(Client):
	async def on_ready(self):
		print("Discord Client Connected")
	
CLIENT = CustomClient(intents=Intents.default())

def start_discord_client():
	loop = asyncio.get_event_loop()
	loop.create_task(CLIENT.start(TOKEN))
	Thread(target=loop.run_forever).start()
	
def stop_discord_client():
	asyncio.run(CLIENT.close())

async def send_msg(text):
	while not CLIENT.is_ready():
		await asyncio.sleep(1)

	channel = CLIENT.get_channel(UPDATES_CHANNEL_ID)
	await channel.send(text)

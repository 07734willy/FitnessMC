from discord import Client, Intents
import asyncio
import os

TOKEN = os.getenv("FITNESSMC_DISCORD_TOKEN")

UPDATES_CHANNEL_ID = 854509811584598067

class CustomClient(Client):
	async def on_ready(self):
		print("Discord Connected")
	
CLIENT = CustomClient(intents=Intents.default())

async def start_client():
	await CLIENT.start(TOKEN)

async def stop_client():
	await CLIENT.close()

async def send_msg(text):
	while not CLIENT.is_ready():
		await asyncio.sleep(1)

	channel = CLIENT.get_channel(UPDATES_CHANNEL_ID)
	await channel.send(text)

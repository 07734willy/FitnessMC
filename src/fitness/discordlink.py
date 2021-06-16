from discord import Client, Intents
from threading import Thread
from time import sleep
import asyncio
import os

TOKEN = os.getenv("FITNESSMC_DISCORD_TOKEN")

UPDATES_CHANNEL_ID = 854509811584598067
GUILD_ID = 854509742696300544

class CustomClient(Client):
	async def on_ready(self):
		print("Discord Client Connected")
	
INTENTS = Intents.default()
INTENTS.members = True

CLIENT = CustomClient(intents=INTENTS)
DISCORD_LOOP = asyncio.get_event_loop()

def start_discord_client():
	DISCORD_LOOP.create_task(CLIENT.start(TOKEN))
	Thread(target=DISCORD_LOOP.run_forever).start()
	
def stop_discord_client():
	asyncio.run(CLIENT.close())

def send_msg(text):
	asyncio.run_coroutine_threadsafe(_send_msg(text), DISCORD_LOOP)

async def _send_msg(text):
	while not CLIENT.is_ready():
		await asyncio.sleep(1)

	channel = CLIENT.get_channel(UPDATES_CHANNEL_ID)
	await channel.send(text)

def get_discord_member(member_id):
	while not CLIENT.is_ready():
		sleep(0.5)

	guild = CLIENT.get_guild(GUILD_ID)
	return guild.get_member(member_id)

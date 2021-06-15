import os

from mcrcon import MCRcon

MCRCON_IP_ADDRESS = os.getenv("MCRCON_IP_ADDRESS")
MCRCON_IP_ADDRESS = os.getenv("MCRCON_PASSWORD")

def set_mcmmo_skill(player, skill_name, xp):
	with MCRcon(MCRCON_IP_ADDRESS, MCRCON_PASSWORD):
		mcr.command(f"/skillreset {player.minecraft_id} {skill_name}")
		mcr.command(f"/addxp {player.minecraft_id} {skill_name} {xp}")

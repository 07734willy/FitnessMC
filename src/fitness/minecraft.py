import os

from mcrcon import MCRcon

MCRCON_IP_ADDRESS = os.getenv("FITNESSMC_MCRCON_IP_ADDRESS")
MCRCON_PASSWORD = os.getenv("FITNESSMC_MCRCON_PASSWORD")
MCRCON_PORT = int(os.getenv("FITNESSMC_MCRCON_PORT"))

def update_player_skills(player, skills_xp):
	if not skills_xp:
		return

	with MCRcon(MCRCON_IP_ADDRESS, MCRCON_PASSWORD, port=MCRCON_PORT) as mcr:
		for skill_name, xp in skills_xp.items():
			set_mcmmo_skill(mcr, player, skill_name, xp)

def set_mcmmo_skill(mcr, player, skill_name, xp):
	mcr.command(f"/skillreset {player.minecraft_id} {skill_name}")
	mcr.command(f"/addxp {player.minecraft_id} {skill_name} {xp}")

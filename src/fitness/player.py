from collections import namedtuple
import shelve

LAST_WORKOUT = shelve.open("player.db")

Player = namedtuple("Player", ["minecraft_id", "discord_id", "gym_id"])

PLAYER_BY_GYM_ID = {
	"willyGYM": Player("willyMC", "willyDISCORD", "willyGYM"),
	"peterGYM": Player("peterMC", "peterDISCORD", "peterGYM"),
}

for gym_id, player in PLAYER_BY_GYM_ID.items():
	assert gym_id == player.gym_id

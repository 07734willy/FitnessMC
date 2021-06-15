from collections import namedtuple

Player = namedtuple("Player", ["minecraft_id", "discord_id"])

PLAYER_BY_GYM_ID = {
	"willyGYM": Player("willyMC", "willyDISCORD"),
	"peterGYM": Player("peterMC", "peterDISCORD"),
}

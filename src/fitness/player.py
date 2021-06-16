from collections import namedtuple
from .filehelper import get_data_file_path, read_csv_data
import shelve

Player = namedtuple("Player", ["minecraft_id", "discord_id", "gym_id"])

PLAYER_BY_GYM_ID = {data['gym_id']: Player(**data) for data in read_csv_data("players.csv")}
LAST_WORKOUT = shelve.open(get_data_file_path("workouts.dat"))

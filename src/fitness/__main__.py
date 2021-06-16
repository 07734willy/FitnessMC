from .parser import standardize_workout_log, parse_gym_username
from .compute import calculate_activity_xp, calculate_skills_xp
from .player import PLAYER_BY_GYM_ID, LAST_WORKOUT
from .summary import print_summary

from .discordlink import start_client, stop_client
import asyncio

def clean_df_columns(df):
	subset_df = df[['Date', 'Workout #', 'Exercise', 'Set #', 'Reps', 'Weight']]
	renamed_df = subset_df.rename(columns={'Workout #': 'Workout', 'Set #': 'Set'})
	
	renamed_df['Workout'] = renamed_df['Workout'].astype(int)
	renamed_df['Set']     = renamed_df['Set'].astype(int)
	renamed_df['Reps']    = renamed_df['Reps'].astype(int)

	renamed_df['Date'] = renamed_df['Date'].dt.strftime('%b %d')
	return renamed_df

async def handle_csv(csv_data):
	full_workout_log = standardize_workout_log(csv_data)
	print(full_workout_log)

	gym_id = parse_gym_username(full_workout_log)
	print(gym_id)

	workout_log = clean_df_columns(full_workout_log)

	print(workout_log)

	player = PLAYER_BY_GYM_ID[gym_id]
	activity_xp = calculate_activity_xp(workout_log)

	skills_xp = calculate_skills_xp(activity_xp, player)
	#update_skills_xp(activity_xp, player)
	
	await print_summary(workout_log, activity_xp, skills_xp, player)
	LAST_WORKOUT[gym_id] = workout_log
	# LAST_SEEN[gym_id] = workout_log['Workout #'].max()

async def test_incoming_csv():
	with open("data.csv") as f:
		text = f.read()

	await handle_csv(text)
	print("done")

def main():
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(asyncio.wait([
			start_client(),
			test_incoming_csv(),
		]))
	except KeyboardInterrupt:
		loop.run_until_complete(stop_client())
	finally:
		loop.close()


if __name__ == "__main__":
	main()

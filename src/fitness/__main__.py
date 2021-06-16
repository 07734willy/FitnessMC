from .parser import standardize_workout_log, parse_gym_username
from .compute import calculate_activity_xp, calculate_skills_xp
from .player import PLAYER_BY_GYM_ID, LAST_WORKOUT
from .summary import print_summary


def main():

	with open("data.csv") as f:
		text = f.read()
	
	workout_log = standardize_workout_log(text)
	print(workout_log)

	gym_id = parse_gym_username(workout_log)
	print(gym_id)

	player = PLAYER_BY_GYM_ID[gym_id]
	activity_xp = calculate_activity_xp(workout_log)

	skills_xp = calculate_skills_xp(activity_xp, player)
	#update_skills_xp(activity_xp, player)
	
	print_summary(workout_log, activity_xp, skills_xp, player)
	LAST_WORKOUT[gym_id] = workout_log
	# LAST_SEEN[gym_id] = workout_log['Workout #'].max()

if __name__ == "__main__":
	main()

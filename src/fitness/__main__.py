from .parser import get_full_log, get_log_username
from .compute import update_skills_xp, calculate_activity_xp, CALCULATOR_TABLE
from .player import PLAYER_BY_GYM_ID

import shelve
LAST_SEEN = shelve.open("player.db")

workout_log = get_full_log("data.csv")
print(workout_log)

gym_id = get_log_username(workout_log)
print(gym_id)

player = PLAYER_BY_GYM_ID[gym_id]
activity_xp = calculate_activity_xp(workout_log)
update_skills_xp(activity_xp, player)

def calculate_xp_increase(workout_log, activity_xp):
	if gym_id not in LAST_SEEN:
		return activity_xp

	last_workout = LAST_SEEN[gym_id]
	old_workout_log = workout_log[workout_log['Workout #'] <= last_workout]
	old_activity_xp = calculate_activity_xp(old_workout_log)

	diff = {activity_name: new_val - old_activity_xp.get(activity_name, 0)
			for activity_name, new_val in activity_xp.items()}
	nonzero_diff = {k: v for k, v in diff.items() if v}
	return nonzero_diff

def print_summary(workout_log, activity_xp):
	if gym_id in LAST_SEEN:
		last_workout = LAST_SEEN[gym_id]
		new_workout_log = workout_log[workout_log['Workout #'] > last_workout]
	else:
		new_workout_log = workout_log

	if new_workout_log.empty:
		return

	print(new_workout_log)

	xp_diff = calculate_xp_increase(workout_log, activity_xp)
	if xp_diff:
		print("XP Gains:")
		for activity_name, diff_val in sorted(xp_diff.items()):
			print(f"  {activity_name} xp: +{diff_val}")
	
	unsupported_exercises = set(new_workout_log['Exercise'].unique()) - set(CALCULATOR_TABLE)
	if unsupported_exercises:
		formatted_exercises = ", ".join(sorted(unsupported_exercises))
		print(f"The following exercises were not accounted for: {formatted_exercises}")

print_summary(workout_log, activity_xp)
LAST_SEEN[gym_id] = workout_log['Workout #'].max()

import pandas as pd

from .compute import calculate_activity_xp, calculate_skills_xp, CALCULATOR_TABLE
from .player import LAST_WORKOUT

def print_summary(new_workout_log, new_activity_xp, new_skills_xp, player):
	empty_df = pd.DataFrame(columns=new_workout_log.columns)
	old_workout_log = LAST_WORKOUT.get(player.gym_id, empty_df)
	
	print_workout_diff(old_workout_log, new_workout_log)

	old_activity_xp = calculate_activity_xp(old_workout_log)
	print_activity_xp_diff(old_activity_xp, new_activity_xp)

	old_skills_xp = calculate_skills_xp(old_activity_xp, player)
	print_skills_xp_diff(old_skills_xp, new_skills_xp)

	unsupported_exercises = set(new_workout_log['Exercise'].unique()) - set(CALCULATOR_TABLE)
	if unsupported_exercises:
		formatted_exercises = ", ".join(sorted(unsupported_exercises))
		print(f"The following exercises were not accounted for: {formatted_exercises}")

def diff_xp(old_xp, new_xp):
	raw_xp_diff = {name: new_val - old_xp.get(name, 0)
			for name, new_val in new_xp.items()}
	xp_diff = {k: v for k, v in raw_xp_diff.items() if v}
	return xp_diff

def print_skills_xp_diff(old_skills_xp, new_skills_xp):
	xp_diff = diff_xp(old_skills_xp, new_skills_xp)
	
	if not xp_diff:
		return
	
	print("Activity XP Gains:")
	for skill_name, val in sorted(xp_diff.items()):
		print(f"  {skill_name} xp: {val:+}")

def print_activity_xp_diff(old_activity_xp, new_activity_xp):
	xp_diff = diff_xp(old_activity_xp, new_activity_xp)
	
	if not xp_diff:
		return

	print("Skill XP Gains:")
	for activity_name, val in sorted(xp_diff.items()):
		print(f"  {activity_name} xp: {val:+.2f}")


def print_df_changes(df, comment):
	print(comment)
	print(df)

def diff_df(df1, df2):
	return df1.merge(df2.drop_duplicates(), how="left", indicator=True)

def print_workout_diff(old_workout_log, new_workout_log):
	diff1 = diff_df(new_workout_log, old_workout_log)
	diff2 = diff_df(old_workout_log, new_workout_log)

	gained_rows = diff1[diff1['_merge'] == 'left_only']
	lost_rows   = diff2[diff2['_merge'] == 'left_only']
	kept_rows   = diff1[diff1['_merge'] == 'both']

	if not gained_rows.empty:
		print_df_changes(gained_rows, "The following activities were added since the last sync:")
	if not lost_rows.empty:
		print_df_changes(lost_rows, "The following activities were removed from the last sync:")

from textwrap import indent
import pandas as pd

from .compute import calculate_activity_xp, calculate_skills_xp, CALCULATOR_TABLE
from .player import LAST_WORKOUT
from .discordlink import send_msg

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
		formatted_exercises = ", ".join(map(enclose_in_monospace, sorted(unsupported_exercises)))
		send_msg(f"The following exercises were not accounted for: {formatted_exercises}")

def diff_xp(old_xp, new_xp):
	raw_xp_diff = {name: new_val - old_xp.get(name, 0)
			for name, new_val in new_xp.items()}
	xp_diff = {k: v for k, v in raw_xp_diff.items() if v}
	return xp_diff

def xp_diff_to_df(columns, value_format, xp_diff):
	lines = [[name.capitalize(), value_format.format(val)] for name, val in sorted(xp_diff.items())]
	df = pd.DataFrame(lines, columns=columns)
	return df

def print_xp_diff(header, columns, value_format, old_xp, new_xp):
	xp_diff = diff_xp(old_xp, new_xp)
	
	if not xp_diff:
		return

	df = xp_diff_to_df(columns, value_format, xp_diff)
	print_df(df, header=header)

def print_skills_xp_diff(old_skills_xp, new_skills_xp):
	header = "Activity XP Gains:"
	columns = ['Skill', 'XP']
	value_format = "{:+}"

	print_xp_diff(header, columns, value_format, old_skills_xp, new_skills_xp)

def print_activity_xp_diff(old_activity_xp, new_activity_xp):
	header = "Activity XP Gains:"
	columns = ['Activity', 'XP']
	value_format = "{:+.2f}"

	print_xp_diff(header, columns, value_format, old_activity_xp, new_activity_xp)

def enclose_in_codeblock(data):
	return f"```\n{data}\n```"

def enclose_in_monospace(data):
	return f"`{data}`"

def df_to_string(df):
	return df.to_string(index=False, justify='start', float_format=lambda x: f"{x:.2f}")

def format_df(df, header=None):
	body = enclose_in_codeblock(df_to_string(df))

	if not header:
		return body

	return f"{header}\n{body}"

def get_row_split(df, limit):
	text = df_to_string(df)
	line_size = len(text.split("\n", 1)[0]) + 1
	print('line size', line_size)
	return limit // line_size

def print_df(df, header=None):
	size_limit = 1980
	text = format_df(df, header=header)

	if len(text) <= size_limit:
		send_msg(text)
		return

	limit = size_limit - len(header or "") - 1 - (len(text) - len(df_to_string(df)))
	row_count = get_row_split(df, limit)
	print('row count', row_count)

	subset_df = df.head(row_count)
	send_msg(format_df(subset_df, header=header))
	print_df(df.tail(-row_count)) # BUG: row_count CAN be 0, if header is large enough


def print_df_changes(df, comment):
	print_df(df, header=comment)

def diff_df(df1, df2):
	return df1.merge(df2.drop_duplicates(), how="left", indicator=True)

def print_workout_diff(old_workout_log, new_workout_log):
	diff1 = diff_df(new_workout_log, old_workout_log)
	diff2 = diff_df(old_workout_log, new_workout_log)

	gained_rows = diff1[diff1['_merge'] == 'left_only'].drop('_merge', 1)
	lost_rows   = diff2[diff2['_merge'] == 'left_only'].drop('_merge', 1)
	kept_rows   = diff1[diff1['_merge'] == 'both'].drop('_merge', 1)

	if not gained_rows.empty:
		print_df_changes(gained_rows, "The following activities were added since the last sync:")
	if not lost_rows.empty:
		print_df_changes(lost_rows, "The following activities were removed from the last sync:")

	if gained_rows.empty and lost_rows.empty:
		send_msg("No new changes in uploaded workout log")

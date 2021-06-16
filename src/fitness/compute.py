from .minecraft import set_mcmmo_skill
from .filehelper import read_json_config

ACTIVITY_TABLE = read_json_config("activities.json")
SKILL_TABLE   = read_json_config("skills.json")

def decay_by_x_agg(x):
	def agg(values):
		values = sorted(values, reverse=True)
		# print(sum(x**i * v for i, v in enumerate(values)))
		return sum(x**i * v for i, v in enumerate(values))
	return agg

def apply_x_rate_decay(df, x):
	new_df = df.groupby(['Date']).agg(decay_by_x_agg(x))
	return new_df

def apply_x_day_y_bonus(df, x, y):
	sel = df['score'] > 0
	nz_df = df[sel]

	score_csum = nz_df['score'].cumsum()
	nz_df.loc[:, 'score_avg'] = (score_csum - score_csum.shift(x, fill_value=0)) / x
	df.loc[sel, 'score'] *= (nz_df['score'] / nz_df['score_avg']).clip(1.0, 1.0 + y)

def calculator_wrapper(func):
	def wrapper(name, df):
		df = func(df.copy())
		df = df[['Date', 'score']]
		
		activity_data = ACTIVITY_TABLE[name]

		decay_rate = activity_data['decay_rate']
		df = apply_x_rate_decay(df, decay_rate)
		apply_x_day_y_bonus(df, 7, 0.15)

		multiplier = activity_data['multiplier']
		return df['score'].sum() * multiplier
	return wrapper

@calculator_wrapper
def calculate_reps_only(df):
	df.loc[:, 'score'] = df['Reps']
	return df

@calculator_wrapper
def calculate_reps_times_weight(df):
	df.loc[:, 'score'] = df['Reps'] * df['Weight']
	return df

CALCULATOR_TABLE = {
	"Pushup": calculate_reps_only,
}

def calculate_activity_xp(workout_log):
	activity_xp = {}
	for activity_name, func in CALCULATOR_TABLE.items():
		df = workout_log[workout_log['Exercise'] == activity_name]
		activity_xp[activity_name] = func(activity_name, df)
	return activity_xp

def calculate_skills_xp(activity_xp, player):
	return {skill_data['name']: int(sum(activity_xp[activity_name] * skill_data['multiplier'] * rate / sum(skill_data['distribution'].values())
			for activity_name, rate in skill_data['distribution'].items()
		) + skill_data['bonuses'].get(player.minecraft_id, 0))
		for skill_data in SKILL_TABLE}


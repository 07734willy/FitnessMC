from .minecraft import set_mcmmo_skill
import json

def decay_by_x_agg(x):
	def agg(values):
		values = sorted(values, reverse=True)
		# print(sum(x**i * v for i, v in enumerate(values)))
		return sum(x**i * v for i, v in enumerate(values))
	return agg

def apply_x_rate_decay(df, x):
	new_df = df.groupby(['Date']).agg(decay_by_x_agg(x))
	return new_df

def apply_x_day_bonus(df, x):
	sel = df['score'] > 0
	nz_df = df[sel]

	score_csum = nz_df['score'].cumsum()
	nz_df.loc[:, 'score_avg'] = (score_csum - score_csum.shift(x, fill_value=0)) / x
	df.loc[sel, 'score'] *= (nz_df['score'] / nz_df['score_avg']).clip(1.0, 1.1)

def calculate_pushup(df):
	df = df.copy()
	df.loc[:, 'score'] = df['Reps']
	df = df[['Date', 'score']]

	df = apply_x_rate_decay(df, 0.7)
	apply_x_day_bonus(df, 3)

	return df['score'].sum()

CALCULATOR_TABLE = {
	"Pushup": calculate_pushup,
}

with open("skills.json", "r") as f:
	SKILL_TABLE = json.load(f)

def calculate_activity_xp(workout_log):
	activity_xp = {}
	for activity_name, func in CALCULATOR_TABLE.items():
		df = workout_log[workout_log['Exercise'] == activity_name]
		activity_xp[activity_name] = func(df)
	return activity_xp

def calculate_skills_xp(activity_xp, player):
	return {skill_data['name']: int(sum(activity_xp[activity_name] * rate 
			for activity_name, rate in skill_data['rates'].items()
		) + skill_data['bonuses'].get(player.minecraft_id, 0))
		for skill_data in SKILL_TABLE}
		# set_mcmmo_skill(player, skill_data['name'], xp)


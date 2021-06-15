import pandas as pd

import re

KG_TO_LB = 2.20462

def get_headers(df):
	gym_hero_headers = df[pd.notnull(df['Workout duration'])]
	gym_hero_headers = gym_hero_headers.drop(
		columns=[
			'Exercise',
			'Set #',
			'Reps',
			'Weight',
			'Unit',
			'Muscle group',
			'Workout'
			]
		)

	gym_hero_headers['Date'] = pd.to_datetime(df['Date'])
	return gym_hero_headers

def get_content(df):
	gym_hero_content = df[pd.notnull(df['Reps'])]
	gym_hero_content = gym_hero_content.drop(
		columns=[
			'Date',
			'Workout duration',
			'Link',
			'Workout note'
			]
		)
	return gym_hero_content

def get_full_log(filepath):
	df = pd.read_csv(filepath)

	gym_hero_headers = get_headers(df)
	gym_hero_content = get_content(df)

	gym_hero_merged = pd.merge(
		gym_hero_content,
		gym_hero_headers,
		how='left',
		left_on='Workout #',
		right_on='Workout #'
	)

	rows_to_convert = gym_hero_merged['Unit'] == "kg"
	gym_hero_merged.loc[rows_to_convert, 'Weight'] *= KG_TO_LB
	gym_hero_merged['Unit'] = "lb"

	return gym_hero_merged

def get_log_username(df):
	link = df.iloc[0]['Link']
	return re.search(r"@([^/]+)/", link).group(1)


"""
def read_csv_data(data):
	stream = StringIO(data)
	reader = csv.DictReader(stream)

	gym_name = parse_gym_username(next(iter(reader))['link'])

	session = Session()

	for row in reader:
		if row['Date']:
			workout_date = datetime.strptime(row['Date'], "%a %b %d %Y").date()

		session.add(Activity(
			int(row['Workout #']),
			workout_date,
			row['Excercise'],
			int(row['Set #']),
			int(row['Reps']),
			float(row['Weight']),
		))

	return session

"""

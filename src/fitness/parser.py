from io import StringIO
import pandas as pd

import re

KG_TO_LB = 2.20462

def extract_headers(df):
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

def extract_content(df):
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

def standardize_workout_log(data):
	df = pd.read_csv(StringIO(data))

	gym_hero_headers = extract_headers(df)
	gym_hero_content = extract_content(df)

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

def parse_gym_username(df):
	link = df.iloc[0]['Link']
	return re.search(r"@([^/]+)/", link).group(1)


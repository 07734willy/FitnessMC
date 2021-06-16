from csv import DictReader
import json
import os

PROJ_ROOT_DIR = os.path.abspath(
		os.path.dirname(
			os.path.dirname(
				os.path.dirname(__file__))))

def get_data_file_path(filename):
	return os.path.join(PROJ_ROOT_DIR, 'data', filename)

def get_config_file_path(filename):
	return os.path.join(PROJ_ROOT_DIR, 'config', filename)

def read_json_config(filename):
	filepath = get_config_file_path(filename)
	with open(filepath, "r") as f:
		return json.load(f)

def read_csv_data(filename):
	filepath = get_data_file_path(filename)
	with open(filepath, "r") as f:
		return list(DictReader(f))


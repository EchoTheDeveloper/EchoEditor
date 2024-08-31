import json
from app import CURR_LANG

with open(f'resources/langs/{CURR_LANG}.json', 'r') as file:
    translation = json.load(file)

root_title = translation['root']['title']
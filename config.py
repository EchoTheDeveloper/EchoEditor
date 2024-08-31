import json

#########################
CURR_LANG = 'en_us'
#########################

with open(f'resources/langs/{CURR_LANG}.json', 'r') as file:
    translation = json.load(file)

root_title = translation['root']['title']

fm_title = translation['menus']['file']['title']
fm_new = translation['menus']['file']['new']
fm_open = translation['menus']['file']['open']
fm_save = translation['menus']['file']['save']
fm_exit = translation['menus']['file']['exit']

em_title = translation['menus']['edit']['title']
em_preferences = translation['menus']['edit']['preferences']

#########################
# Preferences
#########################

preferences_title = translation['preferences']['root']['title']
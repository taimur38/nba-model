import csv
import json

stats = open('data/combined-stats.csv')
with open('data/headers') as f:
	fieldnames = [line.strip() for line in f]
reader = list(csv.DictReader(stats, fieldnames=fieldnames))
shots = list(filter(lambda r: r['event_type'] == 'shot' or r['event_type'] == 'miss', reader))

granularity = 5

teams_in_game = {}
for row in reader:
	game = teams_in_game.get(row['game_id'], set())
	if row['team'] is not '':
		game.add(row['team'])
		teams_in_game[row['game_id']] = game

teams = {} # key is teams, value is 2D dictionary of shot locations and amount of attempts
for row in shots:

	team_key = (teams_in_game[row['game_id']] - {row['team']}).pop()
	profile = teams.get(team_key, {str((0, 0)): {'made': 0, 'attempt': 0}})
	try:
		x = float(row['converted_x'])
		y = float(row['converted_y'])
		if y > 47:
			y = 94 - y
	except:
		if row['converted_x'] != 'unknown':
			print('exception on row ' + str(row))

	coords = str((int(x / granularity), int(y / granularity)))

	made = 0 if int(row['points']) == 0 else 1
	profile[coords] = {
		'attempt': profile.get(coords, {'attempt': 0, 'made': 0})['attempt'] + 1,
		'made':    profile.get(coords, {'attempt': 0, 'made': 0})['made'] + made
	}

	teams[team_key] = profile

with open('generated/defense-profile.json', 'w') as f:
	json.dump(teams, f)

stats.close()

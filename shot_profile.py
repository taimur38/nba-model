import csv
import json

stats = open('data/combined-stats.csv')
with open('data/headers') as f:
	fieldnames = [line.strip() for line in f]

reader = csv.DictReader(stats, fieldnames=fieldnames)

granularity = 5

teams = {} # key is teams, value is 2D dictionary of shot locations and amount of attempts
shots = filter(lambda r: r['event_type'] == 'shot' or r['event_type'] == 'miss', reader)
for row in shots:
	profile = teams.get(row['team'], {str((0, 0)): {'made': 0, 'attempt': 0}})
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

	teams[row['team']] = profile

with open('generated/shot-profile.json', 'w') as f:
	json.dump(teams, f)

stats.close()

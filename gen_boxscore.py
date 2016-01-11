import csv
import json
import itertools

fieldnames = []
stats = open('data/combined-stats.csv')

with open('data/headers') as f:
	fieldnames = [line.strip() for line in f]

reader = csv.DictReader(stats, fieldnames=fieldnames)
games = {}

# gen box scores
reader.__next__()
for row in reader:

	if row['event_type'] != 'shot' and row['result'] != 'made':
		continue

	gameid = row['game_id'].replace('"', '').replace('=', '')
	game = games.get(gameid, {})
	game['date'] = row['date']
	game[row['team']] = game.get(row['team'], {})
	team = game[row['team']]

	team[row['period']] = team.get(row['period'], 0) + int(row['points'])

	games[gameid] = game

rows = [["gameid", "date", "team", "q1", "q2", "q3", "q4", "q5", "q6"]]
for gameid in games:
	game = games[gameid]
	for team in game:
		if team == 'date':
			continue
		periods = game[team]
		row = [
			gameid,
			game['date'],
			team,
			periods.get('1', 0),
			periods.get('2', 0),
			periods.get('3', 0),
			periods.get('4', 0),
			periods.get('5', 0),
			periods.get('6', 0)
		]
		rows.append(row)

with open('generated/box_scores.csv', 'w') as f:
	for row in rows:
		f.write(','.join([str(r) for r in row]) + '\n')

stats.close()

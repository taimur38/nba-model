import sys
import json
import operator

with open('generated/defense-profile.json') as f:
	defense_profile = json.load(f)

with open('generated/shot-profile.json') as f:
	shot_profile = json.load(f)


def normalize(team):

	normalized = {}
	total = 0
	maximum = -1
	for coord, stat in team.items():
		combined = stat['made'] + stat['attempt']
		normalized[coord] = combined
		total += combined
		maximum = maximum if combined < maximum else combined

	for coord in normalized:
		normalized[coord] /= total

	return normalized


def compute_diff(shot_profile, defense_profile):
	diffs = {}
	diff = 0
	for coord in shot_profile:
		diffs[coord] = shot_profile[coord] + defense_profile.get(coord, 0)
		diff += diffs[coord]

	return diff, diffs


team1_offense = normalize(shot_profile[sys.argv[1]])
team2_offense = normalize(shot_profile[sys.argv[2]])

team1_defense = normalize(defense_profile[sys.argv[1]])
team2_defense = normalize(defense_profile[sys.argv[2]])

diff1, _ = compute_diff(team1_offense, team2_defense)
diff2, _ = compute_diff(team2_offense, team1_defense)

winner = sys.argv[1] if diff1 > diff2 else sys.argv[2]
print("predicted winner: {winner}".format(winner=winner))

print(sys.argv[1] + " score: " + str(diff1))
print(sys.argv[2] + " score: " + str(diff2))

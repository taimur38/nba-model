import sys
import json
import operator

with open('generated/defense-profile.json') as f:
	defense_profile = json.load(f)

with open('generated/shot-profile.json') as f:
	shot_profile = json.load(f)

print(sys.argv)
knicks = shot_profile[sys.argv[1]]

ranking = {}
for coord in knicks:
	stat = knicks[coord]
	ranking[coord] = stat['made'] + stat['attempt']

sorted_coords = sorted(ranking.items(), key=operator.itemgetter(1))

print(json.dumps(sorted_coords, indent=4, separators=(',', ': ')))

import json
import os

with open('../HackaTAL2016/team_composition.txt') as f:
	data = {}
	team = ""
	player = {}
	players = []
	i = 0
	for line in f:
		if "TEAM" in line:
			data = {}
			players = []
			team = line.split("TEAM")[1].split("#")[0].strip()
			data['team'] = team
			#print(team)
		elif "--" in line:
			i = 0
			player['number'] = line.split("--")[1].strip()
			i += 1
		elif i == 1:
			player['role'] = line.strip()
			i += 1
		elif i == 2:
			player['name'] = line.strip()
			i += 1
		elif i == 3:
			player['age'] = line.split("-")[1].strip()
			i += 1
		elif i == 7:
			player['club'] = line.split("-")[1].strip()
			players.append(player)
			data['players'] = players
			#print(player)
			player = {}
			i += 1
			with open(os.getcwd() + '/data/'+team+'.json', 'w+') as out:
				json.dump(data, out, indent = 4)
		else:
			i += 1
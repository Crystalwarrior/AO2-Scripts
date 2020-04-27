from itertools import combinations

def digit_root(n): 
	return (n - 1) % 9 + 1 if n else 0


players = input('Please input the total players in a single string, e.g. 123456789. ')
player_combinations = [''.join(l) for i in range(len(players)) for l in combinations(players, i+1)]
minplayers = int(input("Please input lowest amount of players per door. "))
maxplayers = int(input("Please input highest amount of players per door. "))
while True:
	doortotal = int(input("Please input amount of doors. "))

	doors = []
	for i in range(doortotal):
		doors.append({"num": int(input("Please input number for door {}. ".format(i))), "combos": []})

		for combo in player_combinations:
			if len(combo) >= minplayers and len(combo) <= maxplayers and digit_root(int(combo)) == doors[i]["num"]:
				doors[i]["combos"].append(combo)
		
	for door in doors:
		print('Door #{} combos:'.format(door["num"]))
		print('\n'.join(door["combos"]))

	input("Displaying all possible combos.")
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
        doors.append({"num": int(input("Please input number for door {}. ".format(i+1))), "combos": []})

        for combo in player_combinations:
            if len(combo) >= minplayers and len(combo) <= maxplayers and digit_root(int(combo)) == doors[i]["num"]:
                doors[i]["combos"].append(combo)

    door_root = digit_root(sum([door["num"] for door in doors]))
    print("The digital root of the doors is {}.".format(door_root))

    # for door in doors:
    #   print('Door #{} individual combos:'.format(door["num"]))
    #   print('\n'.join(door["combos"]))

    def get_combo(comboA, comboB):
        if any(a for a in comboA if a in comboB) == True: #We can't have the same player entering one or several doors at once
            return None
        combo = comboA + comboB
        dif = ''.join([a for a in players if not (a in combo)])
        print("{}: {}, {}: {} \tleft behind: {}".format(doors[0]["num"], comboA, doors[1]["num"], comboB, dif))
        return combo

    for comboA in doors[0]["combos"]:
        for comboB in doors[1]["combos"]:
            get_combo(comboA, comboB)

    input("Displaying all possible combos.")
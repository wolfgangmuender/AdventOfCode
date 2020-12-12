with open("input/input12.txt") as f:
    content = f.read().splitlines()

actions = []
for line in content:
    actions.append({
        "action": line[0],
        "value": int(line[1:]),
    })
directions = ["E", "S", "W", "N"]


def update_position(orientation, value):
    if orientation == "N":
        position[1] += value
    elif orientation == "S":
        position[1] -= value
    elif orientation == "E":
        position[0] += value
    elif orientation == "W":
        position[0] -= value
    else:
        raise Exception


direction = 0
position = [0, 0]
for action in actions:
    if action["action"] in ["N", "S", "E", "W"]:
        update_position(action["action"], action["value"])
    elif action["action"] == "L":
        direction = int((direction - action["value"] / 90) % 4)
    elif action["action"] == "R":
        direction = int((direction + action["value"] / 90) % 4)
    elif action["action"] == "F":
        update_position(directions[direction], action["value"])
    else:
        raise Exception

print("Solution 1: the ship's Manhattan distance is {}".format(abs(position[0]) + abs(position[1])))

position = [0, 0]
waypoint = [10, 1]
for action in actions:
    if action["action"] == "N":
        waypoint[1] += action["value"]
    elif action["action"] == "S":
        waypoint[1] -= action["value"]
    elif action["action"] == "E":
        waypoint[0] += action["value"]
    elif action["action"] == "W":
        waypoint[0] -= action["value"]
    elif action["action"] == "L":
        for i in range(0, int(action["value"] / 90)):
            waypoint = [-waypoint[1], waypoint[0]]
    elif action["action"] == "R":
        for i in range(0, int(action["value"] / 90)):
            waypoint = [waypoint[1], -waypoint[0]]
    elif action["action"] == "F":
        position[0] += action["value"] * waypoint[0]
        position[1] += action["value"] * waypoint[1]
    else:
        raise Exception

print("Solution 2: the ship's Manhattan distance is {}".format(abs(position[0]) + abs(position[1])))

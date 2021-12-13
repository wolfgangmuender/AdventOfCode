with open("input/input13.txt") as f:
    content = f.read().splitlines()

positions = []
instructions = []

positions_part = True
for line in content:
    if not line:
        positions_part = False
    elif positions_part:
        x, y = [int(n) for n in line.split(",")]
        positions.append([x, y])
    else:
        direction, line_number = line.replace("fold along ", "").split("=")
        instructions.append([direction, int(line_number)])


def map_point(the_position, the_command):
    if the_command[0] == "x":
        if the_position[0] <= the_command[1]:
            return the_position.copy()
        else:
            return [2 * the_command[1] - the_position[0], the_position[1]]
    elif the_command[0] == "y":
        if the_position[1] <= the_command[1]:
            return the_position.copy()
        else:
            return [the_position[0], 2 * the_command[1] - the_position[1]]
    else:
        raise Exception("You cannot be serious!")


fold1 = []
for position in positions:
    new_position = map_point(position, instructions[0])
    if new_position not in fold1:
        fold1.append(new_position)

print("Solution 1: {} dots are visible after completing just the first fold instruction on the transparent paper"
      .format(len(fold1)))

fold = positions
for instruction in instructions:
    old_fold = fold
    fold = []
    for position in old_fold:
        new_position = map_point(position, instruction)
        if new_position not in fold:
            fold.append(new_position)

max_x = max([pos[0] for pos in fold])
max_y = max([pos[1] for pos in fold])
for y in range(0, max_y + 1):
    row = []
    for x in range(0, max_x + 1):
        if [x, y] in fold:
            row.append("#")
        else:
            row.append(".")
    print(row)

the_code_from_the_image = "CAFJHZCK"

print("Solution 2: the code to use to activate the infrared thermal imaging camera system is {}"
      .format(the_code_from_the_image))

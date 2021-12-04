with open("input/input04.txt") as f:
    content = f.read().splitlines()


def str_to_int_list(the_string, the_separator):
    print(the_string)
    return [int(n) for n in the_string.split(the_separator) if n]


def transpose(the_matrix):
    return list(map(list, zip(*the_matrix)))


class Board:

    def __init__(self):
        self.rows = []
        self.marked_rows = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.winner_number = None

    def mark(self, the_number):
        i = 0
        for row in self.rows:
            j = 0
            for cell in row:
                if cell == the_number:
                    self.marked_rows[i][j] = 1
                j += 1
            i += 1

        if not self.winner_number and self.is_winner():
            self.winner_number = number

    def is_winner(self):
        for row in self.marked_rows:
            if all(row):
                return True
        for row in transpose(self.marked_rows):
            if all(row):
                return True
        return False

    def get_score(self):
        the_sum = 0
        i = 0
        for marked_row in self.marked_rows:
            j = 0
            for marked_cell in marked_row:
                if marked_cell == 0:
                    the_sum += self.rows[i][j]
                j += 1
            i += 1

        return the_sum * self.winner_number


numbers = []
boards = []
for line in content:
    if ',' in line:
        numbers = str_to_int_list(line, ',')
    elif len(line) == 0:
        boards.append(Board())
    else:
        boards[-1].rows.append(str_to_int_list(line, ' '))

winners = []
for number in numbers:
    for board in boards:
        if not board.is_winner():
            board.mark(number)
            if board.is_winner():
                winners.append(board)

print("Solution 1: the first winner board has a final score of {}".format(winners[0].get_score()))
print("Solution 2: the last winner board has a final score of {}".format(winners[-1].get_score()))

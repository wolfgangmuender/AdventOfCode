import os
import time
from collections import defaultdict


class DeterministicDie:

    def __init__(self):
        self.curr = 0
        self.rolls = 0

    def roll(self):
        if self.curr == 100:
            self.curr = 1
        else:
            self.curr += 1
        self.rolls += 1
        return self.curr


class Game:

    def __init__(self, pos1, score1, pos2, score2):
        self.pos1 = pos1
        self.score1 = score1
        self.pos2 = pos2
        self.score2 = score2

    def is_finished(self):
        return self.score1 >= 21 or self.score2 >= 21

    def process_move(self, player1_turn, pos_diff):
        if player1_turn:
            pos1 = (self.pos1 + pos_diff - 1) % 10 + 1
            score1 = self.score1 + pos1
            return Game(pos1, score1, self.pos2, self.score2)
        else:
            pos2 = (self.pos2 + pos_diff - 1) % 10 + 1
            score2 = self.score2 + pos2
            return Game(self.pos1, self.score1, pos2, score2)

    def serialise(self):
        return "{},{},{},{}".format(self.pos1, self.score1, self.pos2, self.score2)

    @staticmethod
    def deserialise(serialised):
        pos1, score1, pos2, score2 = [int(num) for num in serialised.split(",")]
        return Game(pos1, score1, pos2, score2)


def main(puzzle_input):
    pos1_initial = int(puzzle_input[0][-1])
    pos2_initial = int(puzzle_input[1][-1])

    die = DeterministicDie()

    player1 = {
        "pos": pos1_initial,
        "score": 0,
    }
    player2 = {
        "pos": pos2_initial,
        "score": 0,
    }

    player1["other"] = player2
    player2["other"] = player1
    curr = player1
    while player1["score"] < 1000 and player2["score"] < 1000:
        curr["pos"] = (curr["pos"] + die.roll() + die.roll() + die.roll() - 1) % 10 + 1
        curr["score"] += curr["pos"]
        curr = curr["other"]

    looser = player2 if player1["score"] >= 1000 else player1

    print("Solution 1: the product of the score of the losing player by the number of times the die was rolled is {}"
          .format(looser["score"] * die.rolls))

    initial = Game(pos1_initial, 0, pos2_initial, 0)

    games = defaultdict(lambda: 0)
    games[initial.serialise()] = 1
    continue_games = True
    player1_turn = True
    while continue_games:
        continue_games = False

        games_copy = games.copy()
        for serialised, num in games_copy.items():
            game = Game.deserialise(serialised)
            if num == 0 or game.is_finished():
                continue

            games[serialised] -= num
            moves = {
                3: 1,
                4: 3,
                5: 6,
                6: 7,
                7: 6,
                8: 3,
                9: 1,
            }
            for move, factor in moves.items():
                new_game = game.process_move(player1_turn, move)
                games[new_game.serialise()] += num * factor

            continue_games = True

        player1_turn = not player1_turn

    player1_wins = 0
    player2_wins = 0
    for serialised, num in games.items():
        game = Game.deserialise(serialised)
        if game.score1 > game.score2:
            player1_wins += num
        else:
            player2_wins += num

    player_num = 1 if player1_wins > player2_wins else 2
    player_score = max(player1_wins, player2_wins)

    print("Solution 2: player {} wins in more universes, namely in {}".format(player_num, player_score))


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))

from copy import copy

with open("input/input22.txt") as f:
    content = f.read().splitlines()

initial_player1_cards = []
initial_player2_cards = []
current_cards = initial_player1_cards
for line in content:
    if not line:
        current_cards = initial_player2_cards
    elif line.startswith("Player"):
        continue
    else:
        card = int(line)
        current_cards.append(card)


def play_game(curr_player1_cards, curr_player2_cards):
    while curr_player1_cards and curr_player2_cards:
        card1 = curr_player1_cards.pop(0)
        card2 = curr_player2_cards.pop(0)
        if card1 > card2:
            curr_player1_cards.append(card1)
            curr_player1_cards.append(card2)
        else:
            curr_player2_cards.append(card2)
            curr_player2_cards.append(card1)


player1_cards = copy(initial_player1_cards)
player2_cards = copy(initial_player2_cards)
play_game(player1_cards, player2_cards)
winning_cards = player1_cards if player1_cards else player2_cards


def get_score(the_winning_cards):
    score = 0
    card_score = 0
    while the_winning_cards:
        card_score += 1
        score += the_winning_cards.pop() * card_score
    return score


print("Solution 1: the winning player's score is {}".format(get_score(winning_cards)))


def stringify(curr_player1_cards, curr_player2_cards):
    return "".join([str(x) for x in curr_player1_cards]) + "," + "".join([str(x) for x in curr_player2_cards])


def play_recursive_game(curr_player1_cards, curr_player2_cards):
    already_played = []
    while curr_player1_cards and curr_player2_cards:
        print(curr_player1_cards)
        print(curr_player2_cards)
        print("----------")
        current_turn = stringify(curr_player1_cards, curr_player2_cards)
        if current_turn in already_played:
            return 1
        else:
            already_played.append(current_turn)

        card1 = curr_player1_cards.pop(0)
        card2 = curr_player2_cards.pop(0)

        if len(curr_player1_cards) >= card1 and len(curr_player2_cards) >= card2:
            winner = play_recursive_game(copy(curr_player1_cards[0:card1]), copy(curr_player2_cards[0:card2]))
        elif card1 > card2:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            curr_player1_cards.append(card1)
            curr_player1_cards.append(card2)
        else:
            curr_player2_cards.append(card2)
            curr_player2_cards.append(card1)

    return 1 if curr_player1_cards else 2


player1_cards = copy(initial_player1_cards)
player2_cards = copy(initial_player2_cards)
play_recursive_game(player1_cards, player2_cards)
winning_cards = player1_cards if player1_cards else player2_cards

print("Solution 2: the winning player's score is {}".format(get_score(winning_cards)))

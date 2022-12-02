import enum

class Move(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Outcome(enum.Enum):
    DRAW = 0
    WIN = 1
    LOSE = 2

def score_for_first_player(p1: Move, p2: Move):
    outcome = Outcome((p1.value - p2.value) % 3)
    if outcome == Outcome.WIN:
        return p1.value + 6
    elif outcome == Outcome.DRAW:
        return p1.value + 3
    else:
        return p1.value

def player_move_given_outcome(p1: Move, outcome: Outcome):
    if outcome == Outcome.DRAW:
        return p1
    elif outcome == Outcome.LOSE:
        return Move((p1.value - 2) % 3 + 1)
    else:
        # win
        return Move(p1.value % 3 + 1)

col1_dict = {'A': Move.ROCK, 'B': Move.PAPER, 'C': Move.SCISSORS}
col2_dict = {'X': Outcome.LOSE, 'Y': Outcome.DRAW, 'Z': Outcome.WIN}

with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        line = line.strip()
        p1_move, outcome = line.split(" ")
        p2_move = player_move_given_outcome(col1_dict[p1_move], col2_dict[outcome])
        total += score_for_first_player(p2_move, col1_dict[p1_move])
    print(total)
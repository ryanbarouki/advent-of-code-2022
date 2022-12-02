def score_for_first_player(p1, p2):
    diff = (p1 - p2) % 3
    if diff == 1:
        #win
        return p1 + 6
    elif diff == 0:
        #draw
        return p1 + 3
    else:
        #lose
        return p1

def player_move_given_outcome(p1, outcome):
    if outcome == 2:
        # draw
        return p1
    elif outcome == 1:
        # lose
        return (p1 - 2) % 3 + 1
    else:
        # win
        return p1 % 3 + 1


p1_decode_dict = {'A': 1, 'B': 2, 'C':3}
outcome_decode_dict = {'X': 1, 'Y': 2, 'Z':3}

with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        line = line.strip()
        p1, outcome = line.split(" ")
        p2_move = player_move_given_outcome(p1_decode_dict[p1], outcome_decode_dict[outcome])
        total += score_for_first_player(p2_move, p1_decode_dict[p1])
    print(total)
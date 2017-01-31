# noinspection PyPep8
BOARD_FORMAT = "----------------------------\n| {0} | {1} | {2} |\n|--------------------------|\n| {3} | {4} | {5} |\n|--------------------------|\n| {6} | {7} | {8} |\n----------------------------"
NAMES = [' ', 'X', 'O']

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3


def empty_state():
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def game_over(state):
    # noinspection PyShadowingNames
    for i in range(3):
        if state[i][0] != EMPTY and state[i][0] == state[i][1] and state[i][0] == state[i][2]:
            return state[i][0]
        if state[0][i] != EMPTY and state[0][i] == state[1][i] and state[0][i] == state[2][i]:
            return state[0][i]
    if state[0][0] != EMPTY and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
        return state[0][0]
    if state[0][2] != EMPTY and state[0][2] == state[1][1] and state[0][2] == state[2][0]:
        return state[0][2]
    # noinspection PyShadowingNames
    for i in range(3):
        for j in range(3):
            if state[i][j] == EMPTY:
                return EMPTY
    return DRAW


def print_board(state):
    cells = []
    # noinspection PyShadowingNames
    for i in range(3):
        for j in range(3):
            cells.append(NAMES[state[i][j]].center(6))
    print BOARD_FORMAT.format(*cells)


def play(agent1, agent2):
    current_field_state = empty_state()
    current_player = agent1.player
    game_state = EMPTY
    for i in range(9):
        if current_player == agent1.player:
            agent1.action(current_field_state)
            current_player = agent2.player
        else:
            agent2.action(current_field_state)
            current_player = agent1.player
        game_state = game_over(current_field_state)
        if game_state != EMPTY:
            return game_state
    return game_state

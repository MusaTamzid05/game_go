import random
from dlgo.gotypes import Player
from dlgo.gotypes import Point

def to_python(player_state):

    if player_state is None:
        return "None"

    if player_state == Player.black:
        return Player.black

    return Player.white


def main():

    MAX63 = 0x7fffffffffffffff

    table = {}
    empty_board = 0

    for row in range(1, 20):
        for col in range(1, 20):
            for state in (Player.black, Player.white):
                code = random.randint(0, MAX63)
                table[Point(row, col), state] = code


    print("from .gotypes import Player")
    print("from .gotypes import Point")
    print("")
    print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
    print("")

    print("HASH_CODE = {")
    for (pt, state), hash_code in table.items():
        print("  ({}, {}) : {},".format(pt, to_python(state), hash_code))

    print("}")
    print("")
    print("EMPTY_BOARD = {}".format(empty_board))


main()




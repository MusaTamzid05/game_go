from dlgo import gotypes

COLS = "ABCDEFGHIJKLMOPQRST"
STONE_TO_CHARS = {
        None : " . ",
        gotypes.Player.black : " x ",
        gotypes.Player.white : " o ",
        }


def print_move(player, move):

    if move.is_pass:
        move_str = "passes"

    elif move.is_resign:
        move_str = "resigns"
    else:
        move_str = "{}{}".format(COLS[move.point.col - 1], move.point.row)

    print("{} {}".format(player, move_str))



def print_board(board):

    for row in range(board.num_rows, 0 , -1):
        bump = " " if row <= 9 else ""
        line = []

        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row = row, col = col))
            line.append(STONE_TO_CHARS[stone])


        print("{}{} {}".format(bump, row, "".join(line)))

    print("    " + "  ".join(COLS[:board.num_cols]))


def point_from_coords(coords):

    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])

    return gotypes.Point(row = row, col = col)

def coords_from_point(point):
    return "%s%d" % (COLS[point.col - 1], point.row)

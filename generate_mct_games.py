import argparse
from dlgo.encoders.base import get_encoder_by_name
from dlgo import goboard

def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []
    encoder = get_encoder_by_name("oneplane", board_size)
    game = goboard.GameState.new_game(board_size)
    print(game)

    return 1, 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_size", "-b", type = int, default = 9)
    parser.add_argument("--rounds", "-r", type = int, default = 1000)
    parser.add_argument("--temperature", "-t", type = float, default = 0.8)
    parser.add_argument("--max-moves", "-m", type = float, default = 60,
            help = "Max moves per game")
    parser.add_argument("--num-games", "-n", type = int, default = 10)
    parser.add_argument("--board-out")
    parser.add_argument("--move-out")

    args = parser.parse_args()
    print(args)

    for i in range(args.num_games):
        print(f"Generating game {i + 1}/{args.num_games}")
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)



if __name__:
    main()

import argparse
from dlgo.encoders.base import get_encoder_by_name
from dlgo import goboard
from dlgo import mcts
from dlgo.utils import print_board
from dlgo.utils import print_move

import numpy as np
import os

def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []
    encoder = get_encoder_by_name("oneplane", board_size)
    game = goboard.GameState.new_game(board_size)
    bot = mcts.MCTSAgent(num_rounds = rounds, temperature = temperature)

    num_moves = 0

    while not game.is_over():
        print_board(game.board)
        move = bot.select_move(game)

        if move.is_play:
            boards.append(encoder.encode(game))
            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot)

        print_move(game.next_player, move)
        num_moves += 1
        game = game.apply_move(move)

        if num_moves > max_moves:
            break


    return np.array(boards) , np.array(moves)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_size", "-b", type = int, default = 9)
    parser.add_argument("--rounds", "-r", type = int, default = 1000)
    parser.add_argument("--temperature", "-t", type = float, default = 0.8)
    parser.add_argument("--max-moves", "-m", type = float, default = 60,
            help = "Max moves per game")
    parser.add_argument("--num-games", "-n", type = int, default = 10)

    data_path = os.path.join("generated_data", "mcts")

    parser.add_argument("--board-out", type = str,  default = os.path.join(data_path,"features.npy") , help = "Save path for Features generating using mcts agent")
    parser.add_argument("--move-out", type = str,  default = os.path.join(data_path, "labels.npy") , help = "Save path for labels generating using mcts agent"  )

    args = parser.parse_args()
    print(args)



    xs, ys = [], []

    for i in range(args.num_games):
        print(f"Generating game {i + 1}/{args.num_games}")
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)

    print("total move generation complete")

    x = np.concatenate(xs)
    y = np.concatenate(ys)

    np.save(args.board_out, x)
    np.save(args.move_out, y)

    print("Data generated.")

if __name__:
    main()

from dlgo.encoders.base import get_encoder_by_name
from dlgo.data.index_processor import KGSIndex
from dlgo.data.sampling import Sampler
from dlgo.gosgf import Sgf_game

from dlgo.goboard import GameState
from dlgo.goboard import Board
from dlgo.goboard import Move



from dlgo.gotypes import Player
from dlgo.gotypes import Point


from dlgo.data.generator import DataGenerator

import numpy as np

import os
import multiprocessing
import sys
import gzip
import shutil
import tarfile

def worker(jobinfo):
    try:
        clazz, encoder, zip_file, data_file_name,  game_list = jobinfo
        clazz(encoder = encoder).process_zip(zip_file, data_file_name, game_list)
    except (KeyboardInterrupt, SystemExit):
        raise Exception(">> Exiting child process")


class GoDataProcessor:
    def __init__(
            self,
            encoder = "simple",
            data_directory = "data"
            ):
        self.encoder_string = encoder
        self.encoder = get_encoder_by_name(encoder, 19)
        self.data_dir = data_directory

    def load_go_data(
            self,
            data_type = "train",
            num_samples = 1000
            ):
        index = KGSIndex(data_directory = self.data_dir)
        index.download_files()

        sampler = Sampler(data_dir = self.data_dir)
        data = sampler.draw_data(data_type, num_samples)

        # the unzip part removed, we load data from
        # predefine folder

        generator = DataGenerator(self.data_dir, data)
        return generator




    def map_to_workers(self, data_type, samples):
        zip_names = set()
        indices_by_zip_name = {}

        for filename, index in samples:
            zip_names.add(filename)

            if filename not in indices_by_zip_name:
                indices_by_zip_name[filename] = []

            indices_by_zip_name[filename].append(index)

        zips_to_process = []

        for zip_name in zip_names:
            base_name = zip_name.replace(".tar.gz", "")
            data_file_name = base_name + data_type

            if not os.path.isfile(self.data_dir + "/" + data_file_name):
                zips_to_process.append((
                    self.__class__,
                    self.encoder_string,
                    zip_name,
                    data_file_name,
                    indices_by_zip_name[zip_name]
                    ))


        cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes = cores)
        p = pool.map_async(worker, zips_to_process)

        try:
            p.get()
        except KeyboardInterrupt:
            pool.terminal()
            pool.join()
            sys.exit(-1)

    def unzip_data(self, zip_file_name):
        this_gz = gzip.open(self.data_dir + "/" + zip_file_name)
        tar_file = zip_file_name[0:-3]

        this_tar = open(self.data_dir + "/" + tar_file, "wb")
        shutil.copyfileobj(this_gz, this_tar)
        this_tar.close()

        return tar_file

    def num_total_examples(self, zip_file, game_list, name_list):
        total_examples = 0
        for index in game_list:
            name = name_list[index - 1]
            if name.endswith(".sgf"):
                sgf_content = zip_file.extractfile(name).read()
                sgf = Sgf_game.from_string(sgf_content)
                game_state, first_move_done = self.get_handicap(sgf)

                num_moves = 0

                for item in sgf.main_sequence_iter():
                    color, move = item.get_move()

                    if color is not None:
                        if first_move_done:
                            num_moves += 1
                        first_move_done = True

                    total_examples = total_examples + num_moves

            else:
                #raise ValueError(name + " is not valid sgf")
                continue

        return total_examples


    @staticmethod
    def get_handicap(sgf):
        go_board = Board(19, 19)
        first_move_done = False
        move = None
        game_state = GameState.new_game(19)


        if sgf.get_handicap() is not None and sgf.get_handicap() != 0:
            for setup in sgf.get_root().get_setup_stones():
                for move in setup:
                    row, col = move
                    go_board.place_stone(Player.black, Point(row + 1, col + 1))

            first_move_done = True
            game_state = GameState(go_board, Player.white, None, move)

        return game_state, first_move_done


    def process_zip(self, zip_file_name, data_file_name, game_list):
        tar_file = self.unzip_data(zip_file_name)
        zip_file = tarfile.open(self.data_dir + "/" + tar_file)
        name_list = zip_file.getnames()
        total_examples = self.num_total_examples(zip_file, game_list, name_list)

        shape = self.encoder.shape()
        feature_shapes = np.insert(shape, 0, np.asarray([total_examples]))
        features = np.zeros(feature_shapes)
        labels = np.zeros((total_examples,))

        counter = 0

        for index in game_list:
            name = name_list[index + 1]



            if name.endswith("sgf") == False:
                continue

            sgf_content = zip_file.extractfile(name).read()
            sgf = Sgf_game.from_string(sgf_content)

            game_state, first_move_done = self.get_handicap(sgf)

            for item in sgf.main_sequence_iter():
                color, move_tuple = item.get_move()
                point = None

                print(move_tuple)

                if color is not None:
                    if move_tuple is None:
                        continue

                    row, col = move_tuple


                    point = Point(row + 1, col + 1)
                    move = Move.play(point)
                else:
                    move = Move.pass_turn()

                if first_move_done and point is not None:
                    features[counter] = self.encoder.encode(game_state)
                    labels[counter] = self.encoder.encode_point(point)
                    counter += 1

                game_state = game_state.apply_move(move)
                first_move_done = True


        feature_file_base = os.path.join(self.data_dir, data_file_name, "_features_%d")
        label_file_base = os.path.join(self.data_dir, data_file_name, "_labels__%d")


        chunk = 0
        chunksize = 1024

        while features.shape[0] >= chunksize:
            feature_file = feature_file_base % chunk
            label_file = label_file_base % chunk
            chunk += 1
            current_features, features = features[:chunksize], features[chunksize:]
            current_labels, labels = labels[:chunksize], labels[chunksize:]

            print("saving")
            np.save(feature_file, current_features)
            np.save(label_file , current_labels)

            print(f"Feature file : {current_features}, label File : {current_labels}")


    def consolidate_games(self, data_type, samples):
        files_needed = set(file_name for file_name, index in samples)
        file_names = []

        for zip_file_name in files_needed:
            file_name = zip_file_name.replace(".tar.gz", "") + data_type
            file_names.append(file_name)


        print(file_names)





from dlgo.data.processor import GoDataProcessor
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.network.small import layers


from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint


import tensorflow as tf

def limit_gpu():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)



def main():
    limit_gpu()
    go_board_rows, go_board_cols = 19, 19
    num_classes = go_board_rows * go_board_cols
    num_games = 100

    encoder = OnePlaneEncoder((go_board_rows, go_board_cols))
    processor = GoDataProcessor(encoder = encoder.name(), data_directory = "data_processed_100")
    generator = processor.load_go_data("train", num_games)
    test_generator = processor.load_go_data("test", num_games)

    print(generator.get_num_samples())


    input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
    network_layers = layers(input_shape = input_shape)

    model = Sequential()


    for layer in network_layers:
        model.add(layer)

    model.add(Dense(num_classes, activation = "softmax"))
    model.compile(loss = "categorical_crossentropy", optimizer = "sgd", metrics = ["accuracy"])
    epochs = 3
    batch_size = 128

    model.fit_generator(
            generator.generate(batch_size, num_classes),
            epochs = epochs,
            steps_per_epoch = generator.get_num_samples() / batch_size,
            validation_data = test_generator.generate(batch_size, num_classes),
            validation_steps = test_generator.get_num_samples() / batch_size,
            callbacks = [
                ModelCheckpoint("./checkpoints/small_model_{epoch}.h5")
                ]
            )

    model.evaluate_generator(
            generator = test_generator.generate(batch_size, num_classes),
            steps = test_generator.get_num_samples() / batch_size
            )


if __name__ == "__main__":
    main()

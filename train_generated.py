import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout


from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPooling2D


def limit_gpu(memory = 2048):
    '''
    This is deprecated!!
    '''
    gpus = tf.config.experimental.list_physical_devices('GPU')
    tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory)])


def load_process_data(size):
    '''
    Loads the the process data
    than reshapes it.Than
    the reshape data is devided
    to train to test splot.

    '''

    X = np.load("./generated_data/mcts/features.npy")
    Y = np.load("./generated_data/mcts/labels.npy")

    samples = X.shape[0]


    X = X.reshape(samples, size, size, 1)

    train_samples = int(0.9 * samples)
    X_train, X_test = X[:train_samples], X[train_samples:]
    Y_train , Y_test = Y[:train_samples], Y[train_samples:]

    return X_train, X_test, Y_train, Y_test


def init_model(input_shape, board_size):


    model = Sequential()
    model.add(Conv2D(filters = 48,
        kernel_size = (3, 3),
        activation = "relu",
        padding = "same",
        input_shape = input_shape)
        )

    model.add(Dropout(rate = 0.5))

    model.add(Conv2D(filters = 48,
        kernel_size = (3, 3),
        activation = "relu",
        ))

    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(rate = 0.5))

    model.add(Flatten())
    model.add(Dense(512, activation = "relu"))
    model.add(Dropout(rate = 0.5))
    model.add(Dense(board_size, activation = "softmax"))

    model.summary()
    model.compile(loss = "categorical_crossentropy", optimizer = "sgd", metrics = ["accuracy"])

    return model

def main():
    limit_gpu()
    np.random.seed(123)
    size = 9
    board_size = size * size
    input_shape = (9, 9, 1)

    X_train, X_test, Y_train, Y_test = load_process_data(size = size)

    print(X_train.shape)
    print(Y_train.shape)


    model = init_model(input_shape = input_shape, board_size = board_size)
    model.fit(X_train, Y_train, batch_size = 64, epochs = 10, verbose = 1, validation_data = (X_test, Y_test))
    score = model.evaluate(X_test, Y_test, verbose = 0)

    test_board = np.array([[
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 1, 1, 1, 1, 0, 0, 0, 0,
	0, 1, 1, 1, 1, 0, 0, 0, 0,
	0, 0, 1, 1, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]])

    test_board = test_board.reshape((9, 9, 1))
    test_board = np.expand_dims(X_test[0], axis = 0)



    print(f"Test score : {score[0]}")
    print(f"Test accuracy: {score[1]}")

    move_probs = model.predict(test_board)[0]
    i = 0

    for row in range(9):
        row_formatted = []
        for col in range(9):
            row_formatted.append("{:.3f}".format(move_probs[i]))
            i += 1
        print(" ".join(row_formatted))

if __name__ == "__main__":
    main()

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def load_process_data(board_size):
    '''
    Loads the the process data
    than reshapes it.Than
    the reshape data is devided
    to train to test splot.

    '''

    X = np.load("./generated_data/mcts/features.npy")
    Y = np.load("./generated_data/mcts/labels.npy")

    samples = X.shape[0]

    X = X.reshape(samples, board_size)
    Y = Y.reshape(samples, board_size)

    train_samples = int(0.9 * samples)
    X_train, X_test = X[:train_samples], X[train_samples:]
    Y_train , Y_test = Y[:train_samples], Y[train_samples:]

    return X_train, X_test, Y_train, Y_test


def init_model(board_size):
    model = Sequential()
    model.add(Dense(1000, activation = "sigmoid", input_shape = (board_size,)))
    model.add(Dense(500, activation = "sigmoid"))
    model.add(Dense(board_size, activation = "softmax"))

    model.summary()
    model.compile(loss = "mean_squared_error", optimizer = "sgd", metrics = ["accuracy"])

    return model

def main():
    np.random.seed(123)
    board_size = 9 * 9
    X_train, X_test, Y_train, Y_test = load_process_data(board_size = board_size)

    model = init_model(board_size = board_size)
    model.fit(X_train, Y_train, batch_size = 64, epochs = 100, verbose = 1, validation_data = (X_test, Y_test))
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

__author__ = 'Andrea'
import matplotlib.pyplot as mpl


def main():
    in_train = open("./errors/train_MSE.txt", "r")
    in_test = open("./errors/test_MSE.txt", "r")
    in_valid = open("./errors/valid_MSE.txt", "r")

    test_errors = in_test.readlines()
    test_valid = in_valid.readlines()
    train_errors = in_train.readlines()

    # plot train and test errors
    mpl.plot(range(len(train_errors)), train_errors)
    mpl.plot(range(len(test_errors)), test_errors)
    # mpl.plot(range(len(test_valid)), test_valid)
    mpl.show()

    ptrain = open("./errors/train_progression.txt", "r")
    ptest = open("./errors/test_progression.txt", "r")

    train_errors = ptrain.readlines()
    test_errors = ptest.readlines()

    mpl.close()
    mpl.plot(range(len(train_errors)), train_errors)
    mpl.plot(range(len(test_errors)), test_errors)
    mpl.show()

    in_valid.close()
    in_test.close()
    in_train.close()


if __name__ == "__main__":
    main()

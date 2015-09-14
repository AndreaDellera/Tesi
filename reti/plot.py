__author__ = 'Andrea'
import matplotlib.pyplot as mpl


def main():
    fold = "./FF/train45"
    in_train = open(fold + "/errors/train_MSE.txt", "r")
    in_test = open(fold + "/errors/test_MSE.txt", "r")
    in_valid = open(fold + "/errors/valid_MSE.txt", "r")

    test_errors = in_test.readlines()
    test_valid = in_valid.readlines()
    train_errors = in_train.readlines()

    # plot train and test errors
    mpl.plot(range(len(train_errors)), train_errors)
    mpl.plot(range(len(test_errors)), test_errors)
    # mpl.plot(range(len(test_valid)), test_valid)
    mpl.show()

    ptrain = open(fold + "/errors/train_progression.txt", "r")
    ptest = open(fold + "/errors/test_progression.txt", "r")

    train_errors = ptrain.readlines()
    test_errors = ptest.readlines()
    summ = 0
    for i in train_errors:
        summ += float(i[0:len(i)-1:1])
    print summ / len (train_errors)

    summ = 0
    for i in test_errors:
        summ += float(i[0:len(i)-1:1])
    print summ / len(test_errors)

    mpl.close()
    mpl.plot(range(len(train_errors)), train_errors)
    mpl.plot(range(len(test_errors)), test_errors)
    mpl.show()

    in_valid.close()
    in_test.close()
    in_train.close()
    ptrain.close()
    ptest.close()

if __name__ == "__main__":
    main()

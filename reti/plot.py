__author__ = 'Andrea'
import matplotlib.pyplot as mpl


def main():
    fold = "./FF/train45"
    in_train = open(fold + "/errors/train_MSE.txt", "r")
    in_test = open(fold + "/errors/test_MSE.txt", "r")
    # in_valid = open(fold + "/errors/valid_MSE.txt", "r")

    test_errors = in_test.readlines()
    # test_valid = in_valid.readlines()
    train_errors = in_train.readlines()

    # plot train and test errors
    one, = mpl.plot(range(len(train_errors)), train_errors, label = 'allineamento')
    two, = mpl.plot(range(len(test_errors)), test_errors, label = 'validazione', linestyle='--')
    # three, = mpl.plot(range(len(test_valid)), test_valid)
    mpl.axis([0, 9, 0, 4])
    mpl.legend(handles=[one, two])
    mpl.ylabel('Errore')
    mpl.xlabel('Tempo')
    mpl.show()

    ptrain = open(fold + "/errors/train_progression.txt", "r")
    ptest = open(fold + "/errors/test_progression.txt", "r")

    train_errors = ptrain.readlines()
    test_errors = ptest.readlines()

    mpl.close()
    one, = mpl.plot(range(len(train_errors)), train_errors, label = 'allineamento')
    two, = mpl.plot(range(len(test_errors)), test_errors, label = 'validazione', linestyle='--')
    mpl.axis([0, 10000, 0, 4])
    mpl.legend(handles=[one, two])
    mpl.ylabel('Errore')
    mpl.xlabel('Tempo')
    mpl.show()

    # in_valid.close()
    in_test.close()
    in_train.close()
    ptrain.close()
    ptest.close()

if __name__ == "__main__":
    main()

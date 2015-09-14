__author__ = 'Andrea'
import matplotlib.pyplot as mpl


def main():
    fold = "."
    test_1 = open(fold + "/1_test.txt", "r")
    test_2 = open(fold + "/2_test.txt", "r")
    test_3 = open(fold + "/3_test.txt", "r")
    test_5 = open(fold + "/5_test.txt", "r")
    test_8 = open(fold + "/8_test.txt", "r")


    t1 = test_1.readlines()
    t2 = test_2.readlines()
    t3 = test_3.readlines()
    t5 = test_5.readlines()
    t8 = test_8.readlines()

    # plot train and test errors
    a, = mpl.plot(range(len(t1)), t1, label = '1 input')
    b, = mpl.plot(range(len(t2)), t2, label = '2 input')
    c, = mpl.plot(range(len(t3)), t3, label = '3 input')
    d, = mpl.plot(range(len(t5)), t5, label = '5 input')
    e, = mpl.plot(range(len(t8)), t8, label = '8 input')
    mpl.legend(handles=[a,b,c,d,e])#, ['1 input', '2 input', '3 input', '5 input', '8 input'])
    mpl.show()

    test_1.close()
    test_2.close()
    test_3.close()
    test_5.close()
    test_8.close()
if __name__ == "__main__":
    main()

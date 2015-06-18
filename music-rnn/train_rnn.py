__author__ = 'Andrea'

import xml.etree.ElementTree as ET
import glob
from myBackProp import myBackpropTrainer
from classes import Note
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, LSTMLayer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.validation import Validator

import matplotlib.pyplot as mpl

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

# database for different inputs
def create_db(ds, dstest, n_input, n_output, codecs, tests):
    if n_input == 11:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]),
                    ret_Characters(codecs[j][i + 1])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]),
                    ret_Characters(tests[j][i + 1])
                )
    elif n_input == 22:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]),
                    ret_Characters(codecs[j][i + 2])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]),
                    ret_Characters(tests[j][i + 2])
                )
    elif n_input == 33:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(codecs[j][i + 2]),
                    ret_Characters(codecs[j][i + 3])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(tests[j][i + 2]),
                    ret_Characters(tests[j][i + 3])
                )
    elif n_input == 44:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3]),
                    ret_Characters(codecs[j][i + 4])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3]),
                    ret_Characters(tests[j][i + 4])
                )
    elif n_input == 55:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]),
                    ret_Characters(codecs[j][i + 5])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]),
                    ret_Characters(tests[j][i + 5])
                )
    elif n_input == 66:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]),
                    ret_Characters(codecs[j][i + 6])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]),
                    ret_Characters(tests[j][i + 6])
                )
    elif n_input == 77:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]) + ret_Characters(
                        codecs[j][i + 6]),
                    ret_Characters(codecs[j][i + 7])
                )

        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]) + ret_Characters(
                        tests[j][i + 6]),
                    ret_Characters(tests[j][i + 7])
                )
    elif n_input == 88:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]) + ret_Characters(
                        codecs[j][i + 6]) + ret_Characters(codecs[j][i + 7]),
                    ret_Characters(codecs[j][i + 8])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]) + ret_Characters(
                        tests[j][i + 6]) + ret_Characters(tests[j][i + 7]),
                    ret_Characters(tests[j][i + 8])
                )
    elif n_input == 99:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]) + ret_Characters(
                        codecs[j][i + 6]) + ret_Characters(codecs[j][i + 7]) + ret_Characters(codecs[j][i + 8]),
                    ret_Characters(codecs[j][i + 9])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]) + ret_Characters(
                        tests[j][i + 6]) + ret_Characters(tests[j][i + 7]) + ret_Characters(tests[j][i + 8]),
                    ret_Characters(tests[j][i + 9])
                )

def ret_Characters(string):
    return (
        string[0], string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[8], string[9],
        string[10])

def main():
    # number of pitches in every note normalized by max value
    division = 4096.
    # hash table for encoding the duration
    kv = {'4096': '0000', '3072': '0011', '2048': '0010', '1536': '0101', '1024': '0100',
          '768': '0111', '512': '0110', '384': '1001', '256': '1000', '192': '1011', '128': '1010',
          '64': '1100'}

    # list of all train files
    files = glob.glob("../files/train/*.xml")
    codecs = []
    i = 0
    # extracting all the notes
    for file in files:
        codecs.append([])
        print "\nfile: " + file
        tree = ET.parse(file)
        # notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        notes = [Note(note, division) for note in tree.findall('.//note')]
        for note in notes:
            codecs[i].append(note.encode(kv))
        i += 1

    # list of all test files
    files = glob.glob("../files/test/*.xml")
    tests = []
    i = 0
    # extracting all the notes
    for file in files:
        tests.append([])
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division) for note in tree.findall('.//note')]
        for note in notes:
            tests[i].append(note.encode(kv))
            # print note.encode()
        i += 1

    # creating the datasets
    ds_train = [] # array of train datasets
    ds_test = [] # array of test datasets
    n_input = 88
    n_output = 11

    # creation of the datasets based on the number of input
    create_db(ds_train, ds_test, n_input, n_output, codecs, tests)

    del files, codecs, tests

    # creating the network
    # without hidden layers the network does not works properly
    rnn = buildNetwork(n_input, 8, n_output, recurrent=True, outclass=SigmoidLayer, hiddenclass=LSTMLayer)
    # if verbose == True then print "Total error:", MSE / ponderation
    trainer = myBackpropTrainer(rnn, learningrate=0.01, momentum=0.99, verbose=False, weightdecay=False)


    x = []
    print "start training"
    for i in range(len(ds_train)):
        x += trainer.trainOnDataset(ds_train[i], 70)
    print "finish training"

    NetworkWriter.writeToFile(rnn, 'weights.xml')

    mse = Validator()
    print len(ds_test)
    for i in range(len(ds_test)):
        activations = []
        targets = []
        for inp, out in ds_test[i]:
            activations.append(rnn.activate(inp))
            targets.append(out)
            # print rnn.activate(inp), '\n', out
        targets = [out for inp, out in ds_test[i]]
        print i, "                  ", mse.MSE(activations, targets)

    y = []
    print "start testing"
    for i in range(len(ds_test)):
        y += trainer.testOnData(ds_test[i], verbose=False)
        # print "testing on ", i, "\n"
    print "finish testing"

    # mpl.plot(range(len(x)), x)
    # mpl.show()
    #
    # mpl.plot(range(len(y)), y)
    # mpl.show()

    rnn.reset()


if __name__ == "__main__":
    main()

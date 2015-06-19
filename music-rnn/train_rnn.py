__author__ = 'Andrea'

import xml.etree.ElementTree as ET
import glob
from functions import create_db
from myBackProp import myBackpropTrainer
from classes import Note
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, LSTMLayer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.validation import Validator, CrossValidator

import matplotlib.pyplot as mpl

# database for different inputs

def main():
    # number of pitches in every note normalized by max value
    division = 1024
    # hash table for encoding the duration
    kv = {'4096': '0000', '3072': '0001', '2048': '0010', '1536': '0011', '1024': '0100',
          '768': '0101', '512': '0110', '384': '0111', '256': '1000', '192': '1001', '128': '1010',
          '64': '1011'}

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
    ds_train = []  # array of train datasets
    ds_test = []  # array of test datasets
    n_input = 6 * 11
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
        x += trainer.trainOnDataset(ds_train[i], 50)
    print "finish training"

    # mse = Validator()
    # print len(ds_test)
    # for i in range(len(ds_test)):
    #     activations = []
    #     targets = []
    #     for inp, out in ds_test[i]:
    #         activations.append(rnn.activate(inp))
    #         targets.append(out)
    #         # print rnn.activate(inp), '\n', out
    #     targets = [out for inp, out in ds_test[i]]
    #     # print i, "                  ", mse.MSE(activations, targets)

    y = []
    print "start testing"
    for i in range(len(ds_test)):
        y += trainer.testOnData(ds_test[i], verbose=False)
        # print "testing on ", i, "\n"
    print "finish testing"
    # cval = CrossValidator(trainer, ds_train[0], 10).validate()
    # print cval

    NetworkWriter.writeToFile(rnn, 'weights.xml')


    mpl.plot(range(len(x)), x)
    # mpl.show()
    #
    # mpl.plot(range(len(y)), y)
    mpl.show()

    rnn.reset()


if __name__ == "__main__":
    main()

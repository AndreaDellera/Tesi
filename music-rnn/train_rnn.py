__author__ = 'Andrea'

import xml.etree.ElementTree as ET
import glob
from modules.functions import create_db
from modules.myBackProp import myBackpropTrainer
from modules.classes import Note
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, LSTMLayer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.validation import Validator, CrossValidator, ModuleValidator
from random import shuffle
from pybrain.datasets import SupervisedDataSet

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
    coded_notes = []
    i = 0
    # extracting all the notes
    for file in files:
        print "\nfile: " + file
        tree = ET.parse(file)
        # notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        notes = [Note(note, division) for note in tree.findall('.//note')]
        for note in notes:
            coded_notes.append(note.encode(kv))
        i += 1

    # elimination of duplicates sequences
    coded_set = set(tuple(x) for x in coded_notes)
    coded_notes = [list(x) for x in coded_set]
    # creating the datasets
    n_input = 5 * 11
    n_output = 11

    # creation of the datasets based on the number of input
    dataset_notes = create_db(n_input, n_output, coded_notes)
    del files, coded_notes

    # creating the network
    # without hidden layers the network does not works properly
    rnn = buildNetwork(n_input, 8, n_output, recurrent=True, outclass=SigmoidLayer, hiddenclass=LSTMLayer)
    # if verbose == True then print "Total error:", MSE / ponderation
    trainer = myBackpropTrainer(rnn, learningrate=0.01, momentum=0.9, verbose=False, weightdecay=False, batchlearning=True)

    print "start training"
    # to obtain different dataset for each iteration
    shuffledSequences = []
    for seq in dataset_notes:
        shuffledSequences.append(seq)

    out_train = open("./errors/train_MSE.txt", "w")
    out_test = open("./errors/test_MSE.txt", "w")
    out_valid = open("./errors/valid_MSE.txt", "w")

    rip = 500
    trainer.descent.momentum -= 0.5
    trainer.descent.alpha += 0.5
    for i in range(rip):
        shuffle_ds = SupervisedDataSet(rnn.indim, rnn.outdim)
        shuffle(shuffledSequences)
        for j in range(len(shuffledSequences)):
            shuffle_ds.appendLinked(shuffledSequences[j][0], shuffledSequences[j][1])

        print "train ", i + 1, " su ", rip
        # 0.75 del dataset per il train, il resto per il test
        ds_train, ds_test = shuffle_ds.splitWithProportion(0.75)
        tmp_train = trainer.trainOnDataset(ds_train, 10)
        tmp_test = trainer.testOnData(ds_test)

        validator = Validator()
        activations = []
        targets = []
        for inp, out in ds_test:
            activations.append(rnn.activate(inp))
            targets.append(out)
        val = validator.MSE(activations, targets)
        out_train.write(str(sum(tmp_train) / len(tmp_train)) + '\n')
        out_valid.write(str(val) + '\n')
        out_test.write(str(sum(tmp_test) / len(tmp_test)) + '\n')

        trainer.descent.momentum += 0.5 / rip
        trainer.descent.alpha -= 0.5 / rip
    out_train.close()
    out_test.close()
    out_valid.close()

    print "end training"

    NetworkWriter.writeToFile(rnn, 'weights.xml')
    rnn.reset()


if __name__ == "__main__":
    main()

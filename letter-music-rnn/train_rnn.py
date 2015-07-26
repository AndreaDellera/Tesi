__author__ = 'Andrea'

import xml.etree.ElementTree as ET
import glob
from modules.functions import create_db
from modules.myBackProp import myBackpropTrainer
from modules.classes import Note
from modules.functions import create_network
from modules.functions import evaluate_error
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, LSTMLayer, LinearLayer, MDLSTMLayer, FeedForwardNetwork
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.validation import Validator
from pybrain.datasets import SupervisedDataSet
from random import shuffle
from numpy import unique
import numpy as np
def unique_rows(a):
    return list(set(a))


# database for different inputs

def main():
    # number of pitches in every note normalized by max value
    division = 1024

    # list of all train files
    files = glob.glob("../files/train/*.xml")
    coded_notes = []
    # extracting all the notes
    for file in files:
        print "\nfile: " + file
        tree = ET.parse(file)
        # notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        notes = [Note(note, division) for note in tree.findall('.//note')]
        for note in notes:
            coded_notes.append(note.encode())


    # creating the datasets
    n_input = 5 * 3
    n_output = 3

    rec = True

    # creation of the datasets based on the number of input
    dataset_notes = create_db(n_input, n_output, coded_notes)
    if not rec:
        shuffledSequences = np.array([])
        unique_ds = SupervisedDataSet(n_input, n_output)
        for seq in dataset_notes:
            if not (seq in shuffledSequences):
                np.append(shuffledSequences, seq)
                unique_ds.appendLinked(seq[0], seq[1])
        dataset_notes = unique_ds
        del unique_ds, shuffledSequences

    del files, coded_notes
    # creating the network
    # without hidden layers the network does not works properly
    # rnn = buildNetwork(n_input, 50, n_output, recurrent=rec, outclass=SigmoidLayer, hiddenclass=LSTMLayer, bias=False)

    rnn = create_network(n_input, 100, n_output, recurrent=rec, outclass=LinearLayer, hiddenclass=SigmoidLayer, bias=False)
    # if verbose == True then print "Total error:", MSE / ponderation
    trainer = myBackpropTrainer(rnn, learningrate=0.001, momentum=0.9, verbose=False, weightdecay=False,
                                batchlearning=False, recurrent=rec)

    out_train = open("./errors/train_MSE.txt", "w")
    out_test = open("./errors/test_MSE.txt", "w")
    out_valid = open("./errors/valid_MSE.txt", "w")
    ptrain = open("./errors/train_progression.txt", "w")
    ptest  = open("./errors/test_progression.txt", "w")
    print "start training"
    prev_err = 1000

    # esegue il test su n diverse insiemi di sequenze, in sequenza, ad ogni ciclo;
    # calcola train error e validation error
    # il validation error e' calcolato su n esempi
    dataset_dim = dataset_notes.getLength()
    number_of_division = 20
    if number_of_division > dataset_dim:
        number_of_division = dataset_dim
    n = dataset_notes.getLength() / number_of_division


    # numero di discese lungo il gradiente ad ogni sessione di train
    n_disc_grad = 10
    test_cont = 0
    under = False
    train_progression = []
    test_progression = []
    for i in range(0, dataset_dim - (dataset_dim % number_of_division), n):

        # crea un dataset vuoto per calcolare l'errore di validazione
        ds_test = SupervisedDataSet(rnn.indim, rnn.outdim)
        ds_train = SupervisedDataSet(rnn.indim, rnn.outdim)
        base = test_cont
        print 'train ', (base / n) + 1, ' on ', ((dataset_dim - (dataset_dim % number_of_division)) / n)

        # costruzione dei datasets di train e test per la cross validation
        train_cont = test_cont
        for b in range(dataset_dim - dataset_dim % number_of_division):
            if base <= test_cont < (base + n):
                ds_test.appendLinked(*dataset_notes.getLinked(test_cont))
                test_cont += 1
                train_cont = (train_cont + 1) % number_of_division
            else:
                ds_train.appendLinked(*dataset_notes.getLinked(train_cont))
                train_cont = (train_cont + 1) % number_of_division

        # tmp_train = trainer.trainOnDataset(ds_train, n_disc_grad)
        tmp_train, tmp_test = trainer.trainUntilConvergence(datasetTrain=ds_train, datasetTest=ds_test, verbose=False, maxEpochs=10000)
        train_progression += tmp_train
        test_progression += tmp_test
        # implementa il bold driver, aggiusta il learning rate in base all'evoluzione del train error
        if sum(tmp_train) / len(tmp_train) < prev_err:
            prev_err = sum(tmp_train) / len(tmp_train)
            trainer.descent.alpha += trainer.descent.alpha * 0.1  # alpha = learning rate
        else:
            prev_err = sum(tmp_train) / len(tmp_train)
            trainer.descent.alpha -= trainer.descent.alpha * 0.5  # alpha = learning rate

        # testOnData e Validator calcolano lo stesso errore (MSE) in due modi differenti
        # implementato per vedere se le due funzioni si comportano in maniera coerente

        # tmp_test = trainer.testOnData(ds_test, verbose=True)
        # validator = Validator()
        # activations = []
        # targets = []
        # for inp, out in ds_test:
        #     activations.append(rnn.activate(inp))
        #     targets.append(out)
        # val = validator.MSE(activations, targets)
        val = evaluate_error(rnn, ds_test, verbose=False)

        # scrive gli errori su file per permettere che siano pollati in seguito
        out_train.write(str(sum(tmp_train) / len(tmp_train)) + '\n')
        # out_valid.write(str(val) + '\n')
        out_test.write(str(sum(tmp_test) / len(tmp_test)) + '\n')
        #     under = True
        # if under and (sum(tmp_train) / len(tmp_train) < tmp_test):
        #     break

    for i in range(len(train_progression)):
        ptrain.write(str(train_progression[i]) + '\n')
    for i in range(len(test_progression)):
        ptest.write(str(test_progression[i]) + '\n')


    out_train.close()
    out_test.close()
    out_valid.close()
    ptest.close()
    ptrain.close()

    print "end training"


    # salva lo stato della rete
    NetworkWriter.writeToFile(rnn, 'weights.xml')
    rnn.reset()


if __name__ == "__main__":
    main()

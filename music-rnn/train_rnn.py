__author__ = 'Andrea'

import xml.etree.ElementTree as ET
import glob
from modules.functions import create_binary_dataset, create_int_dataset
from modules.myBackProp import myBackpropTrainer
from modules.classes import Note
from modules.functions import create_network, train_network, binary_to_int_note
from pybrain.structure import SigmoidLayer, LSTMLayer, LinearLayer, GaussianLayer, SoftmaxLayer, TanhLayer
from pybrain.tools.xml.networkwriter import NetworkWriter


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
    # extracting all the notes
    for file in files:
        print "\nfile: " + file
        tree = ET.parse(file)
        # notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        notes = [Note(note, division) for note in tree.findall('.//note')]
        for note in notes:
            coded_notes.append(note.encode(kv))

    binary = True
    input_notes = 8
    if binary:
        # creating the datasets
        n_input = input_notes * 11
        n_output = 11
        dataset_notes = create_binary_dataset(n_input, n_output, coded_notes)
    else:
        n_input = input_notes * 3
        n_output = 3
        coded_notes = binary_to_int_note(coded_notes)
        dataset_notes = create_int_dataset(n_input, n_output, coded_notes)

    rec = True

    # creation of the datasets based on the number of input
    # if not rec:
    #     from modules.functions import unique_dataset
    #     dataset_notes = unique_dataset(dataset_notes)

    del files, coded_notes

    # creating the network
    # without hidden layers the network does not works properly
    # rnn = buildNetwork(n_input, 5, n_output, recurrent=rec, outclass=SigmoidLayer, hiddenclass=LSTMLayer, bias=False)

    if rec:
        hc = LSTMLayer
        oc = SigmoidLayer
    else:
        hc = SigmoidLayer
        oc = SigmoidLayer

    rnn = create_network(n_input, 20, n_output, recurrent=rec, outclass=oc, hiddenclass=hc, bias=False)

    # if verbose == True then print "Total error:", MSE / ponderation
    trainer = myBackpropTrainer(rnn, learningrate=0.3, momentum=0.9, verbose=False,
                                batchlearning=False, recurrent=rec)

    print "start training"
    n = 2
    if n > dataset_notes.getLength():
        n = dataset_notes.getLength()
    train_network(trainer, dataset_notes, k_fold=n, bold_driver=True, maxEpochs=50)

    print "end training"


    # salva lo stato della rete
    NetworkWriter.writeToFile(rnn, 'weights.xml')
    rnn.reset()


if __name__ == "__main__":
    main()

from pybrain import Network, LSTMLayer, LinearLayer, BiasUnit, FullConnection, RecurrentNetwork, SigmoidLayer, \
    FeedForwardNetwork
from pybrain.tools.shortcuts import NetworkError
from modules.myBackProp import myBackpropTrainer
import numpy as np


__author__ = 'Andrea'

from pybrain.datasets import SupervisedDataSet

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

# returns the value (int) of the coded note
def duration_decode(text, dict1):
    return int(dict1[str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]])


# returns the duration's code. If there's an error return 111-1 (not a note)
def code_duration(node, dict1):
    # assert isinstance(node, classes.Note)
    if node.duration.text in dict1:
        return dict1[node.duration.text]
    else:
        return "1111"


# decodes the coded octave
def octave_decode(text):
    note = int((str(text[0])[0] + str(text[1])[0] + str(text[2])[0]), 2)
    # per evitare note altissime o bassissime
    if note > 5:
        return 5
    elif note < 3:
        return 3
    return note


# returns 111 if is a pause, elsewhere the code of the step's octave
def code_octave(node):
    # assert isinstance(node, classes.Pitch)
    if node.is_pause:
        return "111"
    else:
        return "%03d" % int(get_bin(ord(node.octave.text) - 48))


# decodes the coded step
def step_decode(text, dict2):
    tmp = dict2[str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]]
    if tmp is None:
        return 'pause'
    else:
        if len(tmp) > 1:
            return True, tmp[0:1:1]
        else:
            return False, tmp[0:1:1]


# returns 1111 if is a pause, in the other cases return the code of the step
def code_step(node):
    # assert isinstance(node, classes.Pitch)
    if node.is_pause:
        return "1111"
    elif node.not_alter:
        if node.step.text == "A" or node.step.text == "B":
            return "%04d" % int(get_bin((ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7)))
        elif node.step.text == "C" or node.step.text == "D" or node.step.text == "E":
            return "%04d" % int(get_bin((ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7 - 1)))
        else:
            return "%04d" % int(get_bin((ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7 - 2)))
    else:
        if node.step.text == "A" or node.step.text == "B":
            return "%04d" % int(get_bin((ord(node.step.text) - 64 + (ord(node.step.text) - 65) % 7)))
        elif node.step.text == "C" or node.step.text == "D" or node.step.text == "E":
            return "%04d" % int(get_bin((ord(node.step.text) - 64 + (ord(node.step.text) - 65) % 7 - 1)))
        else:
            return "%04d" % int(get_bin((ord(node.step.text) - 64 + (ord(node.step.text) - 65) % 7 - 2)))


# decode the network's output
def decode(note_tuple, dict2, dict1):
    return (octave_decode(note_tuple[0:3:1]),
            step_decode(note_tuple[3:7:1], dict2),
            duration_decode(note_tuple[7:11:1], dict1))


# encode the network's input
def encode(pitch, note, kv):
    return code_octave(pitch) + code_step(pitch) + code_duration(note, kv)


# split a string into 11 characters
def ret_Characters(string):
    return (
        string[0], string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[8], string[9],
        string[10])


# creates a SuperviseDataset based on the number of notes in input
def create_binary_dataset(n_input, n_output, codecs):
    ds = SupervisedDataSet(n_input, n_output)
    if n_input == 11:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]),
                ret_Characters(codecs[i + 1])
            )
    elif n_input == 22:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]),
                            ret_Characters(codecs[i + 2])
                            )

    elif n_input == 33:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(codecs[i + 2]),
                            ret_Characters(codecs[i + 3])
                            )

    elif n_input == 44:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]),
                ret_Characters(codecs[i + 4])
            )
    elif n_input == 55:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]),
                ret_Characters(codecs[i + 5])
            )
    elif n_input == 66:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]),
                ret_Characters(codecs[i + 6])
            )
    elif n_input == 77:
        ds = SupervisedDataSet(n_input, n_output)
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]) + ret_Characters(codecs[i + 6]),
                ret_Characters(codecs[i + 7])
            )

    elif n_input == 88:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]) + ret_Characters(codecs[i + 6]) + ret_Characters(codecs[i + 7]),
                ret_Characters(codecs[i + 8])
            )
    elif n_input == 99:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]) + ret_Characters(codecs[i + 6]) + ret_Characters(codecs[i + 7]) + ret_Characters(
                    codecs[i + 8]),
                ret_Characters(codecs[i + 9])
            )
    return ds

def create_int_dataset(n_input, n_output, codecs):
    ds = SupervisedDataSet(n_input, n_output)
    if n_input == 3 * 1:
        for i in range(0, len(codecs), 1):
            if i + 1 < len(codecs):
                ds.appendLinked(
                    list(codecs[i]),
                    list(codecs[i + 1])
                )
    elif n_input == 3 * 3:
        for i in range(0, len(codecs), 1):
            if i + 3 < len(codecs):
                ds.appendLinked(
                    list(codecs[i] + codecs[i + 1] + codecs[i + 2]),
                    list(codecs[i + 3])
                )
    elif n_input == 3 * 5:
        for i in range(0, len(codecs), 1):
            if i + 6 < len(codecs):
                ds.appendLinked(
                    list(codecs[i] + codecs[i + 1] + codecs[i + 2] + codecs[i + 3] + codecs[i + 4]),
                    list(codecs[i + 5])
                )

    elif n_input == 3 * 8:
        for i in range(0, len(codecs), 1):
            if i + 9 < len(codecs):
                ds.appendLinked(
                    list(codecs[i] + codecs[i + 1] + codecs[i + 2] + codecs[i + 3] + codecs[i + 4] + codecs[i + 5]
                         + codecs[i + 6] + codecs[i + 7]),
                    list(codecs[i + 8])
                )
    else:
        print 'not implemented yet'
        return
    return ds

def create_network(*layers, **options):
    """Build arbitrarily deep networks.

    `layers` should be a list or tuple of integers, that indicate how many
    neurons the layers should have. `bias` and `outputbias` are flags to
    indicate whether the network should have the corresponding biases; both
    default to True.

    To adjust the classes for the layers use the `hiddenclass` and  `outclass`
    parameters, which expect a subclass of :class:`NeuronLayer`.

    If the `recurrent` flag is set, a :class:`RecurrentNetwork` will be created,
    otherwise a :class:`FeedForwardNetwork`.

    If the `fast` flag is set, faster arac networks will be used instead of the
    pybrain implementations."""
    # options
    opt = {'bias': True,
           'hiddenclass': SigmoidLayer,
           'outclass': LinearLayer,
           'outputbias': True,
           'peepholes': False,
           'recurrent': False,
           'fast': False,
           }
    for key in options:
        if key not in opt.keys():
            raise NetworkError('buildNetwork unknown option: %s' % key)
        opt[key] = options[key]

    if len(layers) < 2:
        raise NetworkError('buildNetwork needs 2 arguments for input and output layers at least.')

    # Bind the right class to the Network name
    network_map = {
        (False, False): FeedForwardNetwork,
        (True, False): RecurrentNetwork,
    }

    try:
        network_map[(False, True)] = FeedForwardNetwork
        network_map[(True, True)] = RecurrentNetwork
    except NameError:
        if opt['fast']:
            raise NetworkError("No fast networks available.")
    if opt['hiddenclass'].sequential or opt['outclass'].sequential:
        if not opt['recurrent']:
            # CHECKME: a warning here?
            opt['recurrent'] = True

    Network = network_map[opt['recurrent'], opt['fast']]

    n = Network()
    # linear input layer
    n.addInputModule(LinearLayer(layers[0], name='in'))
    # output layer of type 'outclass'
    n.addOutputModule(opt['outclass'](layers[-1], name='out'))

    if opt['bias']:
        # add bias module and connection to out module, if desired
        n.addModule(BiasUnit(name='bias'))

    # arbitrary number of hidden layers of type 'hiddenclass'
    for i, num in enumerate(layers[1:-1]):
        layername = 'hidden%i' % i
        n.addModule(opt['hiddenclass'](num, name=layername))
        if opt['bias'] and i == 0:
            # also connect all the layers with the bias
            n.addConnection(FullConnection(n['bias'], n[layername]))
            n.addConnection(FullConnection(n['bias'], n['out']))

    # network with hidden layer(s), connections from in to first hidden and last hidden to out
    n.addConnection(FullConnection(n['in'], n['hidden0']))
    n.addConnection(FullConnection(n['hidden%i' % (len(layers) - 3)], n['out']))


    # recurrent connections
    if opt['recurrent']:
        print "Recurrent network"
        n.addRecurrentConnection(FullConnection(n['hidden0'], n['hidden0']))

    n.sortModules()
    return n

def evaluate_int_error(net, ds, verbose=False):
    avg = 0
    for inpt, tar in ds:
        opt = (net.activate(inpt))
        tar = (tar)
        opt_oct = opt[0]
        tar_oct = tar[0]
        opt_step = opt[1]
        tar_step = tar[1]
        opt_dur = opt[2]
        tar_dur = tar[2]

        if verbose:
            print 'octave\n\t output:%f -> target:%f -> diff:%f' % (opt_oct, tar_oct, (opt_oct - tar_oct))
            print 'step\n\t output:%f -> target:%f  -> diff:%f' % (opt_step, tar_step, (opt_step - tar_step))
            print 'duration\n\t output:%f -> target:%f  -> diff:%f' % (opt_dur, tar_dur, (opt_dur - tar_dur))

        e = ((opt_oct + opt_dur + opt_step) - (tar_oct + tar_dur + tar_step)) ** 2
        avg += e
    return avg / len(ds)

def evaluate_binary_error(net, ds, verbose=False):
    avg = 0
    for inpt, tar in ds:
        opt = net.activate(inpt)
        for j in range(len(opt)):
            opt[j] = abs(round(opt[j]))
            if opt[j] > 1:
                opt[j] = 1
            if opt[j] < 1:
                opt[j] = 0
        opt_oct = int((str(opt[0])[0] + str(opt[1])[0] + str(opt[2])[0]), 2)
        tar_oct = int((str(tar[0])[0] + str(tar[1])[0] + str(tar[2])[0]), 2)

        opt_step = int((str(opt[3])[0] + str(opt[4])[0] + str(opt[5])[0] + str(opt[6])[0]), 2)
        tar_step = int((str(tar[3])[0] + str(tar[4])[0] + str(tar[5])[0] + str(tar[6])[0]), 2)

        opt_dur = int((str(opt[7])[0] + str(opt[8])[0] + str(opt[9])[0] + str(opt[10])[0]), 2)
        tar_dur = int((str(tar[7])[0] + str(tar[8])[0] + str(tar[9])[0] + str(tar[10])[0]), 2)

        if verbose:
            print 'octave\n\t output:%f -> target:%f -> diff:%f' % (opt_oct, tar_oct, (opt_oct - tar_oct))
            print 'step\n\t output:%f -> target:%f  -> diff:%f' % (opt_step, tar_step, (opt_step - tar_step))
            print 'duration\n\t output:%f -> target:%f  -> diff:%f' % (opt_dur, tar_dur, (opt_dur - tar_dur))

        e = 0.01 * ((opt_oct + opt_dur + opt_step) - (tar_oct + tar_dur + tar_step)) ** 2
        avg += e
    return avg / len(ds)

def binary_to_int_note(notes):
    int_notes = []
    for note in notes:
        oct = int((str(note[0])[0] + str(note[1])[0] + str(note[2])[0]), 2)
        step = int((str(note[3])[0] + str(note[4])[0] + str(note[5])[0] + str(note[6])[0]), 2)
        dur = int((str(note[7])[0] + str(note[8])[0] + str(note[9])[0] + str(note[10])[0]), 2)
        int_notes.append((oct, step, dur))
    return standardization_int_inputs(int_notes)

def int_to_binary_note(notes):
    bin_notes = []
    i = 0
    while i < len(notes):
        print notes[i], ' ->', int((notes[i]) * 7 + 1)
        print notes[i + 1], ' ->', int(((notes[i + 1]) * 11))
        print notes[i + 2], ' ->', int(((notes[i + 2]) * 15))
        oct = '{0:03b}'.format(int((notes[i]) * 7 + 1))
        step = '{0:04b}'.format(int(((notes[i + 1]) * 11)))
        dur = '{0:04b}'.format(int(((notes[i + 2]) * 15)))
        print len(oct+step+dur)
        bin_notes.append(oct+step+dur)
        i += 3
    return bin_notes

def train_network(trainer, dataset=None, k_fold=1, bold_driver=False, maxEpochs=1000):
    prev_err = 1000
    out_train = open("./errors/train_MSE.txt", "w")
    out_test = open("./errors/test_MSE.txt", "w")
    out_valid = open("./errors/valid_MSE.txt", "w")
    ptrain = open("./errors/train_progression.txt", "w")
    ptest = open("./errors/test_progression.txt", "w")

    # numero di discese lungo il gradiente ad ogni sessione di train
    test_cont = 0
    train_progression = []
    test_progression = []

    assert isinstance(trainer, myBackpropTrainer)
    net = trainer.module
    if dataset is None:
        dataset = trainer.ds

    assert isinstance(dataset, SupervisedDataSet)
    ds_dim = dataset.getLength()

    n = dataset.getLength() / k_fold

    for i in range(0, ds_dim - (ds_dim % k_fold), n):
        # crea un dataset vuoto per calcolare l'errore di validazione
        ds_test = SupervisedDataSet(net.indim, net.outdim)
        ds_train = SupervisedDataSet(net.indim, net.outdim)
        base = test_cont
        print 'train ', (base / n) + 1, ' on ', ((ds_dim - (ds_dim % k_fold)) / n)

        # costruzione dei datasets di train e test per la cross validation
        train_cont = test_cont
        for b in range(ds_dim - ds_dim % k_fold):
            if base <= test_cont < (base + n):
                ds_test.appendLinked(*dataset.getLinked(test_cont))
                test_cont += 1
                train_cont = (train_cont + 1) % k_fold
            else:
                ds_train.appendLinked(*dataset.getLinked(train_cont))
                train_cont = (train_cont + 1) % k_fold
        ds_test = dataset
        ds_train = dataset
        tmp_train, tmp_test = trainer.trainUntilConvergence(datasetTrain=ds_train, datasetTest=ds_test, verbose=False,
                                                            maxEpochs=maxEpochs, continueEpochs=maxEpochs/2)
        # tmp_train, tmp_test = trainer.trainUntilConvergence(maxEpochs=1000, verbose=True,
        #                       continueEpochs=1000, validationProportion=0.30,
        #                       trainingData=ds_train, validationData=ds_test,
        #                       convergence_threshold=10)

        train_progression += tmp_train
        test_progression += tmp_test

        # implementa il bold driver, aggiusta il learning rate in base all'evoluzione del train error
        if bold_driver:
            if tmp_test < prev_err:
                prev_err = tmp_test
                trainer.descent.alpha += trainer.descent.alpha * 0.01  # alpha = learning rate
            else:
                prev_err = tmp_test
                trainer.descent.alpha -= trainer.descent.alpha * 0.01
                trainer.descent.alpha -= trainer.descent.alpha * 0.5  # alpha = learning rate

        # testOnData e Validator calcolano lo stesso errore (MSE) in due modi differenti
        # implementato per vedere se le due funzioni si comportano in maniera coerente
        if net.indim % 11 == 0:
            val = evaluate_binary_error(net, ds_test, verbose=True)
        else:
            val = evaluate_int_error(net, ds_test, verbose=True)

        # scrive gli errori su file per permettere che siano pollati in seguito
        out_train.write(str(sum(tmp_train) / len(tmp_train)) + '\n')
        out_valid.write(str(val) + '\n')
        out_test.write(str(sum(tmp_test) / len(tmp_test)) + '\n')


    for i in range(len(train_progression)):
        ptrain.write(str(train_progression[i]) + '\n')
    for i in range(len(test_progression)):
        ptest.write(str(test_progression[i]) + '\n')

    out_train.close()
    out_test.close()
    out_valid.close()
    ptest.close()
    ptrain.close()

# def unique_dataset(ds):
#     assert isinstance(ds, SupervisedDataSet)
#     inputs = np.array([])
#     targets = np.array([])
#     for i, o in ds:
#         print i, o
#         if not(i in inputs):
#             if not(np.where)
#             print 'aggiungi'
#             inputs = np.concatenate([inputs, i], axis=0)
#             targets = np.concatenate([targets, i], axis=0)
#     print inputs
#
#     un_ds = SupervisedDataSet(ds.indim, ds.outdim)
#     for i in range(inputs.size):
#         un_ds.appendLinked(inputs[i], targets[i])
#     print 'dataset: ', un_ds
#     return un_ds

def standardization_int_inputs(notes):
    std = []
    for note in notes:
        std.append(((float(note[0]) - 1) / (8 - 1), float(note[1]) / 11, (float(note[2])) / 15))
    return std
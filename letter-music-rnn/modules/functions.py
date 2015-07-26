from pybrain import Network, LSTMLayer, LinearLayer, BiasUnit, FullConnection, RecurrentNetwork, SigmoidLayer, \
    FeedForwardNetwork
from pybrain.tools.shortcuts import NetworkError

__author__ = 'Andrea'

from pybrain.datasets import SupervisedDataSet

# returns the value (int) of the coded note
def duration_decode(text):
    return int(text)


# returns the duration's code. If there's an error return 111-1 (not a note)
def code_duration(node):
    return (float(node.duration.text) - 64) / (4096 - 64)


# decodes the coded octave
def octave_decode(text):
    note = int(text)
    # per evitare note altissime o bassissime
    if note > 5:
        return 5
    elif note < 3:
        return 3
    return note


# returns 111 if is a pause, elsewhere the code of the step's octave
def code_octave(node):
    if node.is_pause:
        return -1
    else:
        return (float(node.octave.text) - 1) / (8 - 1)


# decodes the coded step
def step_decode(text):
    if int(text) is -1:
        return 'pause'
    else:
        return int(text)


# returns 1111 if is a pause, in the other cases return the code of the step
def code_step(node):
    # assert isinstance(node, classes.Pitch)
    step = -1
    if node.is_pause:
        return -1
    if node.step.text == "A" or node.step.text == "B":
        step = ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7
    elif node.step.text == "C" or node.step.text == "D" or node.step.text == "E":
        step = ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7 - 1
    else:
        step = ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7 - 2
    if not node.not_alter:
        step -= 1
    return float(step) / 11


# decode the network's output
def decode(note_tuple, dict2, dict1):
    return (octave_decode(note_tuple[0]),
            step_decode(note_tuple[1]),
            duration_decode(note_tuple[2]))


# encode the network's input
def encode(pitch, note):
    return (code_octave(pitch), code_step(pitch), code_duration(note))


# creates a SuperviseDataset based on the number of notes in input
def create_db(n_input, n_output, codecs):
    ds = SupervisedDataSet(n_input, n_output)
    if n_input == 3 * 1:
        for i in range(0, len(codecs), 1):
            if i + 1< len(codecs):
                ds.appendLinked(
                    list(codecs[i]),
                    list(codecs[i + 1])
                )
    elif n_input == 3 * 3:
        for i in range(0, len(codecs), 1):
            if i + 6 < len(codecs):
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


def evaluate_error(net, ds, verbose=False):
    avg = 0
    for inpt, tar in ds:
        opt = net.activate(inpt)
        opt_oct = opt[0]
        tar_oct = tar[0]
        opt_step = opt[1]
        tar_step = tar[1]
        opt_dur = opt[2]
        tar_dur = tar[2]

        if verbose:
            print 'octave: %f -> %f '%(opt_oct, tar_oct)
            print 'step: %f -> %f '%(opt_step, tar_step)
            print 'duration: %f -> %f '%(opt_dur, tar_dur)

        e = ((opt_oct + opt_dur + opt_step) - (tar_oct + tar_dur + tar_step)) ** 2
        avg += e
    return avg / len(ds)

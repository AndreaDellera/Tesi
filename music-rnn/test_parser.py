import xml.etree.ElementTree as ET
import glob
from myBackProp import myBackpropTrainer

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, LinearLayer, LSTMLayer
import matplotlib.pyplot as mpl

from pybrain.tools.validation import Validator


get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]


def ret_Character(string):
    return (string[0], string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[8], string[9], \
           string[10])


class Pitch(object):
    step = None
    alter = None

    def __init__(self, pitch):  # pitch contructor
        if pitch is not None:
            self.step = pitch.find('step')
            self.octave = pitch.find('octave')
            self.alter = pitch.find('alter')


    @property  # return true if is a pause, false elsewhere
    def is_pause(self):
        return self.step is None

    @property  # return true if the pitch is not altered, false elsewhere
    def not_alter(self):
        return self.alter is None

    # return 1111 if is a pause, in the other cases return the code of the step
    def print_step_code(self):
        if self.is_pause:
            return "1111"
        elif self.not_alter:
            if self.step.text == "A" or self.step.text == "B":
                return "%04d" % int(get_bin((ord(self.step.text) - 65 + (ord(self.step.text) - 65) % 7)))
            elif self.step.text == "C" or self.step.text == "D" or self.step.text == "E":
                return "%04d" % int(get_bin((ord(self.step.text) - 65 + (ord(self.step.text) - 65) % 7 - 1)))
            else:
                return "%04d" % int(get_bin((ord(self.step.text) - 65 + (ord(self.step.text) - 65) % 7 - 2)))
        else:
            if self.step.text == "A" or self.step.text == "B":
                return "%04d" % int(get_bin((ord(self.step.text) - 64 + (ord(self.step.text) - 65) % 7)))
            elif self.step.text == "C" or self.step.text == "D" or self.step.text == "E":
                return "%04d" % int(get_bin((ord(self.step.text) - 64 + (ord(self.step.text) - 65) % 7 - 1)))
            else:
                return "%04d" % int(get_bin((ord(self.step.text) - 64 + (ord(self.step.text) - 65) % 7 - 2)))

    # return 111 if is a pause, elsewhere the code of the step's octave
    def print_octave_code(self):
        if self.is_pause:
            return "111"
        else:
            return "%03d" % int(get_bin(ord(self.octave.text) - 48))


class Note(object):
    def __init__(self, note, division, step_time):
        self.pitch = Pitch(note.find('pitch'))
        self.duration = note.find('duration')
        self.type_ = note.find('type')
        self.division = division
        self.st = step_time

    # return true if is a pause, false elsewhere
    @property
    def is_pause(self):
        return self.pitch.is_pause

    # allows to change the division value
    def set_division(self, div):
        self.division = div

    # return the duration's code. If there's an error return 111-1 (not a note)
    def print_duration_code(self):
        for i in self.st:
            if i[0] == self.duration.text:
                return ("%04s" % i[1])
        return "1111"

    @property
    def __str__(self):
        return self.pitch.print_octave_code() + self.pitch.print_step_code() + self.print_duration_code()

    def encode(self):
        return self.__str__


def main():
    # number of pitches in every note normalized by max value
    division = 4096.
    # list with tuple (time, time's code)
    step_time = [("4096", "0000"), ("3072", "0011"), ("2048", "0010"), ("1536", "0101"), ("1024", "0100"),
                 ("768", "0111"), ("512", "0110"), ("384", "1001"), ("256", "1000"), ("192", "1011"), ("128", "1010"),
                 ("64", "1100")]

    # list of all train files
    files = glob.glob("../files/train/*.xml")
    codecs = []
    i = 0
    # extracting all the notes
    for file in files:
        codecs.append([])
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        for note in notes:
            codecs[i].append(note.encode())
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
        notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        for note in notes:
            tests[i].append(note.encode())
            print note.encode()
        i += 1

    # creating the datasets
    ds = []
    dstest = []
    n_input = 22
    n_output = 11

    # adding data to the ds
    for j in range(len(codecs)):
        ds.append(SupervisedDataSet(n_input, n_output))
        for i in range(0, len(codecs[j]) - 2, 1):
            ds[j].appendLinked(ret_Character(codecs[j][i]) + ret_Character(codecs[j][i + 1])
                               ,
                               ret_Character(codecs[j][i + 2])
                               )


    # adding data to the dstest
    for j in range(len(tests)):
        dstest.append(SupervisedDataSet(n_input, n_output))
        for i in range(0, len(tests[j]) - 2, 1):
            dstest[j].appendLinked(ret_Character(tests[j][i]) + ret_Character(tests[j][i + 1])
                                   ,
                                   ret_Character(tests[j][i + 2])
                                   )
    # import pdb; pdb.set_trace()

    # creating the network
    # without hidden layers the network works properly
    rnn = buildNetwork(ds[0].indim, 6, ds[0].outdim, recurrent=True, outclass=SigmoidLayer, hiddenclass=LSTMLayer)
    # if verbose == True then print "Total error:", MSE / ponderation
    trainer = myBackpropTrainer(rnn, learningrate=0.01, momentum=0.99, verbose=True)

    x = []
    print "start training"
    for i in range(len(ds)):
        x += trainer.trainOnDataset(ds[i], 200)
    print "finish training"

    # mse = Validator()
    # print len(dstest)
    # for i in range(len(dstest)):
    # activations = []
    # targets = []
    #     for inp, out in dstest[i]:
    #         activations.append(net.activate(inp))
    #         targets.append(out)
    #         # print net.activate(inp), '\n', out
    #     targets = [out for inp, out in dstest[i]]
    #     print i, "                  ", mse.MSE(activations, targets)

    # output's decode

    # creation of the new music xml
    # noteValue = durationValue = stepValue = alterValue = octaveValue = 0
    # print noteValue, durationValue, stepValue, alterValue, octaveValue

    y = []
    print "start testing"
    for i in range(len(dstest)):
        y += trainer.testOnData(dstest[i], verbose=True)
        print "testing on ", i, "\n"
    print "finish testing"

    # print dstest[0].getSample(0)[0]
    # print rnn.activate(dstest[0].getSample(0)[0]) - rnn.activate(dstest[0].getSample(0)[0])

    mpl.plot(range(len(x)), x)
    mpl.show()

    mpl.plot(range(len(y)), y)
    mpl.show()

    rnn.reset()


if __name__ == "__main__":
    main()
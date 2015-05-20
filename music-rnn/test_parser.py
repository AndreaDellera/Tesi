import xml.etree.ElementTree as ET
import glob
from myBackProp import myBackpropTrainer

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, LinearLayer, RecurrentNetwork
import matplotlib.pyplot as mpl

from pybrain.tools.validation import Validator


get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]


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
            return "%04d" % int(get_bin((ord(self.step.text) - 65)))
        else:
            return "%04d" % int(get_bin((ord(self.step.text) - 65) + (ord(self.alter.text) - 48)))

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
    files = [glob.glob("../files/train/*.xml")]
    codecs = []
    i = 0
    # extracting all the notes
    for file in files[0]:
        codecs.append([])
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        for note in notes:
            codecs[i].append(note.encode())
        i += 1


    # list of all test files
    files = [glob.glob("../files/test/*.xml")]
    tests = []
    i = 0
    # extracting all the notes
    for file in files[0]:
        tests.append([])
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        for note in notes:
            tests[i].append(note.encode())
        i += 1

    # creating the datasets
    ds = []
    dstest = []


    # adding data to the ds
    for j in range(len(codecs)):
        ds.append(SupervisedDataSet(11, 11))
        for i in range(0, len(codecs[j]) - 2, 1):
            ds[j].appendLinked((codecs[j][i][0], codecs[j][i][1], codecs[j][i][2], codecs[j][i][3], codecs[j][i][4],
                             codecs[j][i][5], codecs[j][i][6], codecs[j][i][7], codecs[j][i][8], codecs[j][i][9],
                             codecs[j][i][10])
                            ,
                            (codecs[j][i + 1][0], codecs[j][i + 1][1], codecs[j][i + 1][2], codecs[j][i + 1][3],
                             codecs[j][i + 1][4], codecs[j][i + 1][5], codecs[j][i + 1][6], codecs[j][i + 1][7],
                             codecs[j][i + 1][8], codecs[j][i + 1][9], codecs[j][i + 1][10])
                            )


    # adding data to the dstest
    for j in range(len(tests)):
        dstest.append(SupervisedDataSet(11, 11))
        for i in range(0, len(tests[j]) - 2, 1):
            dstest[j].appendLinked((tests[j][i][0], tests[j][i][1], tests[j][i][2], tests[j][i][3], tests[j][i][4],
                                 tests[j][i][5], tests[j][i][6], tests[j][i][7], tests[j][i][8], tests[j][i][9],
                                 tests[j][i][10]),
                                (tests[j][i + 1][0], tests[j][i + 1][1], tests[j][i + 1][2], tests[j][i + 1][3],
                                 tests[j][i + 1][4], tests[j][i + 1][5], tests[j][i + 1][6], tests[j][i + 1][7],
                                 tests[j][i + 1][8], tests[j][i + 1][9], tests[j][i + 1][10])
                                )
    # import pdb; pdb.set_trace()

    # creating the network
    # without hidden layers the network works properly
    net = buildNetwork(ds[0].indim, 6, ds[0].outdim, recurrent=True, outclass=LinearLayer, hiddenclass=SigmoidLayer)
    # if verbose == True then print "Total error:", MSE / ponderation
    trainer = myBackpropTrainer(net, learningrate=0.01, momentum=0.99)

    x = []
    print "start training"
    for i in range(len(ds)):
        x += trainer.trainOnDataset(ds[i], 200)
    print "finish training"

    # mse = Validator()
    # print len(dstest)
    # for i in range(len(dstest)):
    #     activations = []
    #     targets = []
    #     for inp, out in dstest[i]:
    #         activations.append(net.activate(inp))
    #         targets.append(out)
    #         # print net.activate(inp), '\n', out
    #     targets = [out for inp, out in dstest[i]]
    #     print i, "                  ", mse.MSE(activations, targets)

    # output's decode

    # creation of the new music xml
    noteValue = durationValue = stepValue = alterValue = octaveValue = 0
    print noteValue, durationValue, stepValue, alterValue, octaveValue

    y = []
    print "start testing"
    for i in range(len(dstest)):
        y += trainer.testOnData(dstest[i], verbose=True)
        print "testing on ", i, "\n"
    print "finish testing"
    #
    # mpl.plot(range(len(x)), x)
    # mpl.show()

    mpl.plot(range(len(y)), y)
    mpl.show()
    # print net['in']
    # print net['hidden0']
    # print net['out']

    net.reset()

if __name__ == "__main__":
    main()
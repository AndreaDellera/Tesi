import xml.etree.ElementTree as ET
import glob

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, LinearLayer


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
    # extracting all the notes
    for file in files[0]:
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        for note in notes:
            # print int(note.encode(), 2)
            codecs.append(note.encode())

    # list of all test files
    files = [glob.glob("../files/test/*.xml")]
    tests = []
    # extracting all the notes
    for file in files[0]:
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        for note in notes:
            tests.append(note.encode())

    # creating the datasets
    ds = SupervisedDataSet(11, 11)
    dstest = SupervisedDataSet(11, 11)

    # creating the network
    net = buildNetwork(ds.indim, 6, ds.outdim, recurrent=True, outclass=LinearLayer, hiddenclass=SigmoidLayer)
    trainer = BackpropTrainer(net, dataset=ds, learningrate=0.01, momentum=0.99, verbose=True)

    # adding data to the ds
    for i in range(0, codecs.__len__() - 2, 1):
        ds.addSample((codecs[i][0], codecs[i][1], codecs[i][2], codecs[i][3], codecs[i][4], codecs[i][5], codecs[i][6],
                      codecs[i][7], codecs[i][8], codecs[i][9], codecs[i][10])
                     ,
                     (codecs[i + 1][0], codecs[i + 1][1], codecs[i + 1][2], codecs[i + 1][3], codecs[i + 1][4],
                      codecs[i + 1][5], codecs[i + 1][6], codecs[i + 1][7], codecs[i + 1][8], codecs[i + 1][9],
                      codecs[i + 1][10])
                     )
    print ds

    # adding data to the dstest
    for i in range(0, tests.__len__() - 2, 1):
        dstest.addSample((tests[i][0], tests[i][1], tests[i][2], tests[i][3], tests[i][4], tests[i][5], tests[i][6],
                          tests[i][7], tests[i][8], tests[i][9], tests[i][10]),
                         (tests[i + 1][0], tests[i + 1][1], tests[i + 1][2], tests[i + 1][3], tests[i + 1][4],
                          tests[i + 1][5], tests[i + 1][6], tests[i + 1][7], tests[i + 1][8], tests[i + 1][9],
                          tests[i + 1][10], )
                         )
    print dstest

    print "start training"
    trainer.trainOnDataset(ds, 1000)
    print "finish training"

    # # carry out the training
    # for i in range(1000):
    # trainer.trainEpochs(2)
    #     trnresult = 100. * (1.0-trainer.testOnData(ds))
    #     tstresult = 100. * (1.0-trainer.testOnData(dstest))
    #     print("train error: %5.2f%%" % trnresult, ",  test error: %5.2f%%" % tstresult)

    print "start testing"
    trainer.testOnData(dstest, verbose=True)
    print "finish testing"

    for i in range(2):
        print net.activate((codecs[i][0], codecs[i][1], codecs[i][2], codecs[i][3], codecs[i][4], codecs[i][5],
                           codecs[i][6], codecs[i][7], codecs[i][8], codecs[i][9], codecs[i][10]))


if __name__ == "__main__":
    main()
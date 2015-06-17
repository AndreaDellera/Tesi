import xml.etree.ElementTree as ET
import glob
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.datasets import SupervisedDataSet

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

def create_hash():
    global kv
    kv = {'4096': '0000', '3072': '0011', '2048': '0010', '1536': '0101', '1024': '0100',
          '768': '0111', '512': '0110', '384': '1001', '256': '1000', '192': '1011', '128': '1010',
          '64':  '1100'}


def ret_Characters(string):
    return (
        string[0], string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[8], string[9],
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
    def __init__(self, note, division):
        self.pitch = Pitch(note.find('pitch'))
        self.duration = note.find('duration')
        self.type_ = note.find('type')
        self.division = division
        # self.st = step_time

    # return true if is a pause, false elsewhere
    @property
    def is_pause(self):
        return self.pitch.is_pause

    # allows to change the division value
    def set_division(self, div):
        self.division = div

    # return the duration's code. If there's an error return 111-1 (not a note)
    def print_duration_code(self):
        # for i in self.st:
        #     if i[0] == self.duration.text:
        #         return ("%04s" % i[1])
        if self.duration.text in kv:
            return kv[self.duration.text]
        else:
            return "1111"

    @property
    def __str__(self):
        return self.pitch.print_octave_code() + self.pitch.print_step_code() + self.print_duration_code()

    def encode(self):
        return self.__str__


def main():
    division = 4096.
    # load the network
    rnn = NetworkReader.readFrom('weights.xml')
    files = glob.glob("../files/toGenerate/*.xml")
    input_notes = ()
    create_hash()

    # creating the input for the net
    i = 0
    for file in files:
        print "\nfile: " + file
        tree = ET.parse(file)
        # notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        notes = [Note(note, division) for note in tree.findall('.//note')]
        for note in notes:
            if i < rnn.indim / 11: i += 1
            else: break
            tmp = note.encode()
            for x in range(11):
                input_notes += (tmp[x],)

    # generating new notes! ( :D)
    notes = []
    for i in range(10):
        otp =rnn.activate(input_notes[(i*11):(rnn.indim + 11*i):1])
        notes.append(otp)
        for i in range (len(otp)):
            otp[i] = abs(round(otp[i]))
        # print otp
        input_notes += tuple(otp)

    print notes


if __name__ == "__main__":
    main()

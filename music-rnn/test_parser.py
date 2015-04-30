import xml.etree.ElementTree as ET
import glob
import rnn

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
            return ("%04d" % int(get_bin((ord(self.step.text) - 65))))
        else:
            return ("%04d" % int(get_bin((ord(self.step.text) - 65) + (ord(self.alter.text) - 48))))

    # return 111 if is a pause, elsewhere the code of the step's octave
    def print_octave_code(self):
        if self.is_pause:
            return "111"
        else:
            return ("%03d" % int(get_bin(ord(self.octave.text) - 48)))


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
        for cop in self.st:
            if cop[0] == self.duration.text:
                return ("%04s" % cop[1])
        return "111-1"

    def __str__(self):
        return self.pitch.print_octave_code() + self.pitch.print_step_code() +  self.print_duration_code()

    def encode(self):
        return self.__str__()

def main():
    # number of pitches in every note normalized by max value
    division = 4096.
    # list with tuple (time, time's code)
    step_time = [("4096", "0000"), ("3072", "0011"), ("2048", "0010"), ("1536", "0101"), ("1024", "0100"),
                 ("768", "0111"), ("512", "0110"), ("384", "1001"), ("256", "1000"), ("192", "1011"), ("128", "1010"),
                 ("64", "1100")]
    # list of all test files
    files = [glob.glob("../test/*.xml")]
    codecs = []
    # extracting all the notes
    for file in files[0]:
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
        for note in notes:
            codecs.append(note.encode())

    # creating the recurrent neural network
    network = rnn.MetaRNN()
    network.output_type = "binary"
    network.fit(bin(codecs[0]), bin(codecs[1]))



if __name__ == "__main__":
    main()

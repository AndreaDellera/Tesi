__author__ = 'Andrea'

import xml.etree.ElementTree as ET
get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

class Pitch(object):
    step = None
    alter = None

    def __init__(self, pitch=None):  # pitch contructor
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

    # returns 1111 if is a pause, in the other cases return the code of the step
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

    # decodes the coded step

    # returns 111 if is a pause, elsewhere the code of the step's octave
    def print_octave_code(self):
        if self.is_pause:
            return "111"
        else:
            return "%03d" % int(get_bin(ord(self.octave.text) - 48))




class Note(object):
    def __init__(self, note=None, division=4096):
        self.pitch = Pitch(note.find('pitch'))
        self.duration = note.find('duration')
        self.type_ = note.find('type')
        self.division = division

    # return true if is a pause, false elsewhere
    @property
    def is_pause(self):
        return self.pitch.is_pause

    # allows to change the division value
    def set_division(self, div):
        self.division = div

    # returns the duration's code. If there's an error return 111-1 (not a note)
    def print_duration_code(self, dictionary):
        if self.duration.text in dictionary:
            return dictionary[self.duration.text]
        else:
            return "1111"


    # encode the note
    def encode(self, kv):
        return self.pitch.print_octave_code() + self.pitch.print_step_code() + self.print_duration_code(kv)
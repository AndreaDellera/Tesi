__author__ = 'Andrea'
from functions import code_octave, code_step, code_duration

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]


class Pitch(object):
    step = None
    alter = None

    def __init__(self, pitch):  # pitch contructor
        if pitch is not None:
            self.step = pitch.find('step')
            self.octave = pitch.find('octave')
            self.alter = pitch.find('alter')

    @property # return true if is a pause, false elsewhere
    def is_pause(self):
        return self.step is None

    @property # return true if the pitch is not altered, false elsewhere
    def not_alter(self):
        return self.alter is None

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
        return code_octave(self.pitch) + code_step(self.pitch) + code_duration(self, kv)

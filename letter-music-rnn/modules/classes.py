__author__ = 'Andrea'
from functions import encode

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]


class Pitch(object):
    step = None
    alter = None

    def __init__(self, pitch):  # pitch contructor
        if pitch is not None:
            self.step = pitch.find('step')
            self.octave = pitch.find('octave')
            self.alter = pitch.find('alter')

    # returns true if is a pause, false elsewhere
    @property
    def is_pause(self):
        return self.step is None

    # returns true if the pitch is not altered, false elsewhere
    @property
    def not_alter(self):
        return self.alter is None

class Note(object):
    def __init__(self, note=None, division=4096):
        self.pitch = Pitch(note.find('pitch'))
        self.duration = note.find('duration')
        self.type_ = note.find('type')
        self.division = division

    # returns true if is a pause, false elsewhere
    @property
    def is_pause(self):
        return self.pitch.is_pause

    # allows to change the division value
    def set_division(self, div):
        self.division = div

    # encode the note
    def encode(self):
        return encode(self.pitch, self)

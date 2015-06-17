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

    # decode of the note
    def step_decode(self, text, step_kv):
        if text == "1111":
            self.is_pause = None
        else:
            tmp = step_kv[text]
            if len(tmp) > 1:
                self.alter = True
                self.step.text = tmp[0:1:1]
            else:
                self.alter = None
                self.step.text = tmp

    # return 111 if is a pause, elsewhere the code of the step's octave
    def print_octave_code(self):
        if self.is_pause:
            return "111"
        else:
            return "%03d" % int(get_bin(ord(self.octave.text) - 48))

    # decode of the octave
    def octave_decode(self, text):
        self.octave.text = ''+int(bin(text))


class Note(object):
    def __init__(self, note, division):
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

    # return the duration's code. If there's an error return 111-1 (not a note)
    def print_duration_code(self, dictionary):
        if self.duration.text in dictionary:
            return dictionary[self.duration.text]
        else:
            return "1111"

    def duration_decode(self, text, dur_kv):
        self.duration.text = dur_kv[text]

    def encode(self, kv):
        return self.pitch.print_octave_code() + self.pitch.print_step_code() + self.print_duration_code(kv)

    # TODO: implementing decodification
    def decode(self, note_str, step_kv, dur_kv):
        self.pitch.octave_decode(note_str[0:2:1])
        self.pitch.step_decode(note_str[3:6:1], step_kv)
        self.duration_decode(note_str[7:10:1], dur_kv)

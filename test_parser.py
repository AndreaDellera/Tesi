import xml.etree.ElementTree as ET

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

step_time = [(100,"0000"),(75, "0011"), (50,"0100"),(37,"0101"),(25,"0110"),(19,"0111"),(12,"1000")]



class Pitch(object):
    step = None
    alter = None

    def __init__(self, pitch):

        if pitch is not None:
            self.step = pitch.find('step')
            self.octave = pitch.find('octave')
            self.alter = pitch.find('alter')



    @property
    def is_pause(self):
        return self.step is None

    @property
    def not_alter(self):
        return  self.alter is None

    def print_step_code(self):
        if self.is_pause:
            return "1111"
        elif self.not_alter:
            return ("%04d" % int(get_bin((ord(self.step.text)-65))))
        else:
            return ("%04d" % int(get_bin((ord(self.step.text)-65) + (ord(self.alter.text)-48))))

    def print_octave_code(self):
        if self.is_pause:
            return "111"
        else:
            return ("%03d" % int(get_bin(ord(self.octave.text) - 48)))


class Note(object):
    def __init__(self, note, division):
        self.pitch = Pitch(note.find('pitch'))
        self.duration = note.find('duration')
        self.type_ = note.find('type')
        self.division = division

    @property
    def is_pause(self):
        return self.pitch.is_pause

    def set_division(self, div):
        self.division = div

    def print_duration_code(self):
        numb = int(float(self.duration.text)/self.division*100)
        for cop in step_time
            if cop.first == numb:
                ##return ("%06d"%(int(get_bin(int(float(self.duration.text)/self.division*100.)))))
                return ("%06d"%cop.second)
        return "111-1"

    def __str__(self):
            return self.pitch.print_octave_code() + " " + self.pitch.print_step_code() + " " +  self.print_duration_code() #TODO: duration and value point to implement

def main():
    division = 4096. #number of pitch in every note normalized by max value
    tree = ET.parse('./test/test_2.xml')
    notes = [Note(note, division) for note in tree.findall('//note')]

    for note in notes:
        print note

    print "tutto ok"
    values = []
    for note in notes:
        assert isinstance(note, Note) #Note in range [65 - 71]
        if note.pitch.is_pause:
            values.append(-1)
        else:
            values.append(ord(note.pitch.step.text)-65 + 12*int(note.pitch.octave.text))

    print values

if __name__ == "__main__":
    main()


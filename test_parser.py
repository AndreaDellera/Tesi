import xml.etree.ElementTree as ET

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

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


class Note(object):
    def __init__(self, note):
        self.pitch = Pitch(note.find('pitch'))
        self.duration = note.find('duration')
        self.type_ = note.find('type')

    #def __str__(self):
    #     if self.pitch.is_pause:
    #         return 'e una pausa'
    #     elif self.pitch.not_alter:
    #         return self.pitch.octave.text+self.pitch.step.text
    #     else:
    #         return self.pitch.octave.text+self.pitch.step.text+self.pitch.alter.text

    # def __str__(self):
    #     if self.pitch.is_pause:
    #         return 'e una pausa'
    #     elif self.pitch.not_alter:
    #         return ("%03d" % int(get_bin(ord(self.pitch.octave.text) - 48))) + " " + ("%04d" % int(get_bin((ord(self.pitch.step.text)-65))))
    #     else:
    #         return ("%03d" % int(get_bin(ord(self.pitch.octave.text) - 48))) + " " + ("%04d" % int(get_bin((ord(self.pitch.step.text)-65) + (ord(self.pitch.alter.text)-48))))

    def __str__(self):
        if self.pitch.is_pause:
            return 'e una pausa'
        elif self.pitch.not_alter:
            return ("%03d" % int(get_bin(ord(self.pitch.octave.text) - 48))) + " " + ("%04d" % int(get_bin((ord(self.pitch.step.text)-65))))
        else:
            return ("%03d" % int(get_bin(ord(self.pitch.octave.text) - 48))) + " " + ("%04d" % int(get_bin((ord(self.pitch.step.text)-65) + (ord(self.pitch.alter.text)-48))))

def main():
    tree = ET.parse('/Users/Andrea/Desktop/test_1.xml')
    notes = [Note(note) for note in tree.findall('//note')]

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


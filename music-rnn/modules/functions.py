__author__ = 'Andrea'

from pybrain.datasets import SupervisedDataSet

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

# returns the value (int) of the coded note
def duration_decode(text, dict1):
    return int(dict1[str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]])

# returns the duration's code. If there's an error return 111-1 (not a note)
def code_duration(node, dict1):
    # assert isinstance(node, classes.Note)
    if node.duration.text in dict1:
        return dict1[node.duration.text]
    else:
        return "1111"

# decodes the coded octave
def octave_decode(text):
    note = int((str(text[0])[0] + str(text[1])[0] + str(text[2])[0]), 2)
    # per evitare note altissime o bassissime
    if note > 5:
        return 5
    elif note < 3:
        return 3
    return note

# returns 111 if is a pause, elsewhere the code of the step's octave
def code_octave(node):
    # assert isinstance(node, classes.Pitch)
    if node.is_pause:
        return "111"
    else:
        return "%03d" % int(get_bin(ord(node.octave.text) - 48))

# decodes the coded step
def step_decode(text, dict2):
    tmp = dict2[str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]]
    if tmp is None:
        return 'pause'
    else:
        if len(tmp) > 1:
            return True, tmp[0:1:1]
        else:
            return False, tmp[0:1:1]

# returns 1111 if is a pause, in the other cases return the code of the step
def code_step(node):
    # assert isinstance(node, classes.Pitch)
    if node.is_pause:
        return "1111"
    elif node.not_alter:
        if node.step.text == "A" or node.step.text == "B":
            return "%04d" % int(get_bin((ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7)))
        elif node.step.text == "C" or node.step.text == "D" or node.step.text == "E":
            return "%04d" % int(get_bin((ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7 - 1)))
        else:
            return "%04d" % int(get_bin((ord(node.step.text) - 65 + (ord(node.step.text) - 65) % 7 - 2)))
    else:
        if node.step.text == "A" or node.step.text == "B":
            return "%04d" % int(get_bin((ord(node.step.text) - 64 + (ord(node.step.text) - 65) % 7)))
        elif node.step.text == "C" or node.step.text == "D" or node.step.text == "E":
            return "%04d" % int(get_bin((ord(node.step.text) - 64 + (ord(node.step.text) - 65) % 7 - 1)))
        else:
            return "%04d" % int(get_bin((ord(node.step.text) - 64 + (ord(node.step.text) - 65) % 7 - 2)))

# decode the network's output
def decode(note_tuple, dict2, dict1):
    return (octave_decode(note_tuple[0:3:1]),
            step_decode(note_tuple[3:7:1], dict2),
            duration_decode(note_tuple[7:11:1], dict1))

# encode the network's input
def encode(pitch, note, kv):
    return code_octave(pitch) + code_step(pitch) + code_duration(note, kv)
# split a string into 11 characters
def ret_Characters(string):
    return (
        string[0], string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[8], string[9],
        string[10])

# creates a SuperviseDataset based on the number of notes in input
def create_db(n_input, n_output, codecs):
    ds = SupervisedDataSet(n_input, n_output)
    if n_input == 11:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]),
                ret_Characters(codecs[i + 1])
            )
    elif n_input == 22:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]),
                            ret_Characters(codecs[i + 2])
                            )

    elif n_input == 33:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(codecs[i + 2]),
                            ret_Characters(codecs[i + 3])
                            )

    elif n_input == 44:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]),
                ret_Characters(codecs[i + 4])
            )
    elif n_input == 55:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]),
                ret_Characters(codecs[i + 5])
            )
    elif n_input == 66:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]),
                ret_Characters(codecs[i + 6])
            )
    elif n_input == 77:
        ds = SupervisedDataSet(n_input, n_output)
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]) + ret_Characters(codecs[i + 6]),
                ret_Characters(codecs[i + 7])
            )

    elif n_input == 88:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]) + ret_Characters(codecs[i + 6]) + ret_Characters(codecs[i + 7]),
                ret_Characters(codecs[i + 8])
            )
    elif n_input == 99:
        for i in range(0, len(codecs) - n_input % 10, 1):
            ds.appendLinked(
                ret_Characters(codecs[i]) + ret_Characters(codecs[i + 1]) + ret_Characters(
                    codecs[i + 2]) + ret_Characters(codecs[i + 3]) + ret_Characters(codecs[i + 4]) + ret_Characters(
                    codecs[i + 5]) + ret_Characters(codecs[i + 6]) + ret_Characters(codecs[i + 7]) + ret_Characters(
                    codecs[i + 8]),
                ret_Characters(codecs[i + 9])
            )
    return ds

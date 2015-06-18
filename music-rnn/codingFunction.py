__author__ = 'Andrea'

# returns the value (int) of the coded note
def duration_decode(text, dur_kv):
    return int(dur_kv[str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]])


# decodes the coded octave
def octave_decode(text):
    return int((str(text[0])[0] + str(text[1])[0] + str(text[2])[0]), 2)


def step_decode(text, step_kv):
    if text == "1111":
        return "pause"
    else:
        tmp = step_kv["" + str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]]
        if len(tmp) > 1:
            return True, tmp[0:1:1]
        else:
            return False, tmp[0:1:1]


def decode(note_tuple, step_kv, dur_kv):
    return (octave_decode(note_tuple[0:3:1]),
            step_decode(note_tuple[3:7:1], step_kv),
            duration_decode(note_tuple[7:11:1], dur_kv))

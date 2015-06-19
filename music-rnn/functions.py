__author__ = 'Andrea'
from pybrain.datasets import SupervisedDataSet

# returns the value (int) of the coded note
def duration_decode(text, dur_kv):
    return int(dur_kv[str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]])

# decodes the coded octave
def octave_decode(text):
    return int((str(text[0])[0] + str(text[1])[0] + str(text[2])[0]), 2)

# decodes the coded step
def step_decode(text, step_kv):
    tmp = step_kv[str(text[0])[0] + str(text[1])[0] + str(text[2])[0] + str(text[3])[0]]
    if tmp is None:
        return 'pause'
    else:
        if len(tmp) > 1:
            return True, tmp[0:1:1]
        else:
            return False, tmp[0:1:1]

#decode the network's output
def decode(note_tuple, step_kv, dur_kv):
    return (octave_decode(note_tuple[0:3:1]),
            step_decode(note_tuple[3:7:1], step_kv),
            duration_decode(note_tuple[7:11:1], dur_kv))

#split a string into 11 characters
def ret_Characters(string):
    return (
        string[0], string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[8], string[9],
        string[10])

#creates a SuperviseDataset looking for the number of notes in input
def create_db(ds, dstest, n_input, n_output, codecs, tests):
    if n_input == 11:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]),
                    ret_Characters(codecs[j][i + 1])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]),
                    ret_Characters(tests[j][i + 1])
                )
    elif n_input == 22:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]),
                    ret_Characters(codecs[j][i + 2])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]),
                    ret_Characters(tests[j][i + 2])
                )
    elif n_input == 33:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(codecs[j][i + 2]),
                    ret_Characters(codecs[j][i + 3])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(tests[j][i + 2]),
                    ret_Characters(tests[j][i + 3])
                )
    elif n_input == 44:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3]),
                    ret_Characters(codecs[j][i + 4])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3]),
                    ret_Characters(tests[j][i + 4])
                )
    elif n_input == 55:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]),
                    ret_Characters(codecs[j][i + 5])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]),
                    ret_Characters(tests[j][i + 5])
                )
    elif n_input == 66:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]),
                    ret_Characters(codecs[j][i + 6])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]),
                    ret_Characters(tests[j][i + 6])
                )
    elif n_input == 77:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]) + ret_Characters(
                        codecs[j][i + 6]),
                    ret_Characters(codecs[j][i + 7])
                )

        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]) + ret_Characters(
                        tests[j][i + 6]),
                    ret_Characters(tests[j][i + 7])
                )
    elif n_input == 88:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]) + ret_Characters(
                        codecs[j][i + 6]) + ret_Characters(codecs[j][i + 7]),
                    ret_Characters(codecs[j][i + 8])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]) + ret_Characters(
                        tests[j][i + 6]) + ret_Characters(tests[j][i + 7]),
                    ret_Characters(tests[j][i + 8])
                )
    elif n_input == 99:
        for j in range(len(codecs)):
            ds.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(codecs[j]) - n_input % 10, 1):
                ds[j].appendLinked(
                    ret_Characters(codecs[j][i]) + ret_Characters(codecs[j][i + 1]) + ret_Characters(
                        codecs[j][i + 2]) + ret_Characters(codecs[j][i + 3])
                    + ret_Characters(codecs[j][i + 4]) + ret_Characters(codecs[j][i + 5]) + ret_Characters(
                        codecs[j][i + 6]) + ret_Characters(codecs[j][i + 7]) + ret_Characters(codecs[j][i + 8]),
                    ret_Characters(codecs[j][i + 9])
                )
        for j in range(len(tests)):
            dstest.append(SupervisedDataSet(n_input, n_output))
            for i in range(0, len(tests[j]) - n_input % 10, 1):
                dstest[j].appendLinked(
                    ret_Characters(tests[j][i]) + ret_Characters(tests[j][i + 1]) + ret_Characters(
                        tests[j][i + 2]) + ret_Characters(tests[j][i + 3])
                    + ret_Characters(tests[j][i + 4]) + ret_Characters(tests[j][i + 5]) + ret_Characters(
                        tests[j][i + 6]) + ret_Characters(tests[j][i + 7]) + ret_Characters(tests[j][i + 8]),
                    ret_Characters(tests[j][i + 9])
                )

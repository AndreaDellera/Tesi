__author__ = 'Andrea'

import xml.etree.ElementTree as ET
import glob
from pybrain.tools.xml.networkreader import NetworkReader
from modules.classes import Note
from modules.buildXML import create_music_xml
from modules.functions import decode
import random


def main():
    division = 1024
    # load the network trained in train_rnn
    rnn = NetworkReader.readFrom('weights.xml')
    files = glob.glob("../files/toGenerate/*.xml")
    input_notes = ()
    # hash table for encoding the duration
    dur_en_kv = {'4096': '0000', '3072': '0011', '2048': '0010', '1536': '0101', '1024': '0100',
                 '768': '0111', '512': '0110', '384': '1001', '256': '1000', '192': '1011', '128': '1010',
                 '64': '1100'}

    # hash table for decoding the step value
    step_kv = {1: 'A', 2: 'A#', '0010': 'B', 3: 'C', '0100': 'C#', '0101': 'D', '0110': 'D#',
               '0111': 'E',
               '1000': 'F', '1001': 'F#', '1010': 'G', '1011': 'G#', '1100': 'pausa', '1101': 'pausa', '1110': 'pausa',
               '1111': 'pausa'}

    # hash table for decoding the duration
    dur_dec_kv = {'0000': '4096', '0001': '3072', '0010': '2048', '0011': '1536', '0100': '1024',
                  '0101': '768', '0110': '512', '0111': '384', '1000': '256', '1001': '192', '1010': '128',
                  '1011': '64',
                  '1100': '64', '1101': '64', '1110': '64', '1111': '64'}

    # creating the input for the net
    i = 0
    for file in files:
        print "\nfile: " + file
        tree = ET.parse(file)
        notes = [Note(note, division) for note in tree.findall('.//note')]
        for note in notes:
            if i < rnn.indim / 11:
                i += 1
            else:
                break
            tmp = note.encode(dur_en_kv)
            for x in range(11):
                input_notes += (tmp[x],)

    # generating new notes
    for i in range(150):
        otp = rnn.activate(input_notes[(i * 11):(rnn.indim + 11 * i):1])  # takes the last rnn.indim notes to activate the netwotk
        for x in range(len(otp)):
            otp[x] = abs(round(otp[x]))
        for x in range(11):
            input_notes += (str(otp[x])[0],)

    dec_notes = []
    last = [2,3]
    prec = -1
    # decoding of all the notes in input_notes
    for i in range(0, len(input_notes), 11):
        note = decode(input_notes[i:((i + 1) * 11):1], step_kv, dur_dec_kv)

        # avoid loop
        if note == last[1] and prec == last[0]:
            print "avoided loop ", i / 11
            otp = rnn.activate(random.sample(input_notes, (rnn.indim)))
            for x in range(len(otp)):
                otp[x] = abs(round(otp[x]))
            note = decode(otp, step_kv, dur_dec_kv)

        dec_notes.append(note)
        last.insert(i % (rnn.indim / 11), note)
        prec = note


    # XML
    create_music_xml(dec_notes, division, 'output.xml')


if __name__ == "__main__":
    main()

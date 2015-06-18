import xml.etree.ElementTree as ET
import glob
from pybrain.tools.xml.networkreader import NetworkReader
from classes import Note

get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def ret_Characters(string):
    return (
        string[0], string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[8], string[9],
        string[10])


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


def main():
    division = 4096
    # load the network, trained before
    rnn = NetworkReader.readFrom('weights.xml')
    files = glob.glob("../files/toGenerate/*.xml")
    input_notes = ()
    # hash table for encoding the duration
    dur_en_kv = {'4096': '0000', '3072': '0011', '2048': '0010', '1536': '0101', '1024': '0100',
                 '768': '0111', '512': '0110', '384': '1001', '256': '1000', '192': '1011', '128': '1010',
                 '64': '1100'}

    # hash table for decoding the step value
    step_kv = {'0000': 'A', '0001': 'A#', '0010': 'B', '0011': 'C', '0100': 'C#', '0101': 'D', '0110': 'D#',
               '0111': 'E',
               '1000': 'F', '1001': 'F#', '1010': 'G', '1011': 'G#'}

    # hash table for decoding the duration
    dur_dec_kv = {'0000': '4096', '0011': '3072', '0010': '2048', '0101': '1536', '0100': '1024',
                  '0111': '768', '0110': '512', '1001': '384', '1000': '256', '1011': '192', '1010': '128',
                  '1100': '64'}

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

    # generating new notes! (yeah :D)
    for i in range(3):
        otp = rnn.activate(
            input_notes[(i * 11):(rnn.indim + 11 * i):1])  # takes the last rnn.indim notes to activate the netwotk
        for x in range(len(otp)):
            otp[x] = abs(round(otp[x]))
        for x in range(11):
            input_notes += (str(otp[x])[0],)
    dec_notes = []
    # decoding of all the notes in input_notes
    for i in range(0, len(input_notes), 11):
        dec_notes.append(decode(input_notes[i:((i + 1) * 11):1], step_kv, dur_dec_kv))

    print dec_notes
    #XML
    tree = ET.parse('../files/toGenerate/EmptyXML.xml')
    part = tree.find('.//part')
    del i
    i = 0
    n_measure = 1
    strings = {1: 'E', 2: 'A', 3: 'D', 4: 'G', 5: 'B', 6: 'E'}
    oct = {1: '2', 2: '2', 3: '3', 4: '3', 5: '3', 6: '4'}
    while i < len(dec_notes):
        print i
        # structure of the measure
        measure = ET.SubElement(part, 'measure', {'number': str(n_measure)})
        n_measure += 1
        # <attributes>
        #     <divisions>1024</divisions>
        att = ET.SubElement(measure, 'attributes')
        tmp = ET.SubElement(att, 'division')
        print str(division)
        tmp.text = str(division)
        #     <key>
        #       <fifths>0</fifths>
        #       <mode>major</mode>
        #     </key>
        key = ET.SubElement(att, 'key')
        tmp = ET.SubElement(key, 'fifths')
        tmp.text = str(0)
        tmp = ET.SubElement(key, 'mode')
        tmp.text = "major"
        #     <time>
        #       <beats>4</beats>
        #       <beat-type>4</beat-type>
        #     </time>
        time = ET.SubElement(att, 'time')
        tmp = ET.SubElement(time, 'beats')
        tmp.text = str(4)
        tmp = ET.SubElement(time, 'beat-type')
        tmp.text = str(4)
        #     <staves>1</staves>, numero di alterazioni in chiave
        tmp = ET.SubElement(att, 'staves')
        tmp.text = str(0)
        #     <clef>
        #       <sign>TAB</sign>
        #       <line>6</line>
        #     </clef>
        clef = ET.SubElement(att, 'clef')
        tmp = ET.SubElement(clef, 'sign')
        tmp.text = "TAB"
        tmp = ET.SubElement(clef, 'line')
        tmp.text = str(6)
        #     <staff-details>
        #       <staff-lines>6</staff-lines>
        #       <staff-tuning line="1">
        #         <tuning-step>E</tuning-step>
        #         <tuning-octave>2</tuning-octave>
        #       </staff-tuning>
        # ....
        #       <staff-tuning line="6">
        #         <tuning-step>E</tuning-step>
        #         <tuning-octave>4</tuning-octave>
        #       </staff-tuning>
        #     </staff-details>
        staffD = ET.SubElement(att, 'staff-details')
        tmp = ET.SubElement(staffD, 'staff-lines')
        tmp.text = str(6)
        for j in range(6):
            staffT = ET.SubElement(staffD, 'staff-tuning', {'line': str(j + 1)})
            tmp = ET.SubElement(staffT, 'tuning-step')
            tmp.text = strings[j + 1]
            tmp = ET.SubElement(staffT, 'tuning-octave')
            tmp. text = oct[j + 1]
        # </attributes>
        totDuration = 0

        # putting the notes in the measure
        while totDuration < division and i < len(dec_notes):
            print i
            # <note>

            note = ET.SubElement(measure, 'note')
            #     <pitch>
            #       <step>G</step>
            #       <alter>1</alter>
            #       <octave>5</octave>
            #     </pitch>
            pitch = ET.SubElement(note, 'pitch')
            tmp = ET.SubElement(pitch, 'step')
            tmp.text = dec_notes[i][1][1]
            tmp = ET.SubElement(note, 'alter')
            # print dec_notes[i][1][0], dec_notes[i][1][1]
            if dec_notes[i][1][0]:
                tmp.text = '1'
            tmp = ET.SubElement(pitch, 'octave')
            tmp.text = str(dec_notes[i][0])
            #     <duration>512</duration>
            tmp = ET.SubElement(note, 'duration')
            tmp.text = str(dec_notes[i][2])
            #     <voice>0</voice>
            tmp = ET.SubElement(note, 'voice')
            tmp.text = '0'
            #     <type>eighth</type>
            #       <dynamics>
            #         <f/>
            #       </dynamics>
            dyn = ET.SubElement(note, 'dynamics')
            ET.SubElement(dyn, 'f')
            # </note>

            totDuration += dec_notes[i][2]
            # print(totDuration)
            i += 1

    indent(tree.getroot())
    del strings, oct, i
    tree.write('output.xml', xml_declaration=True, encoding='utf-8', method="xml")

if __name__ == "__main__":
    main()

__author__ = 'Andrea'

import xml.etree.ElementTree as ET


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def create_music_xml(dec_notes, division=1024, name='output.xml'):
    tree = ET.parse('../files/toGenerate/EmptyXML.xml')
    part = tree.find('.//part')
    i = 0
    n_measure = 1
    strings = {1: 'E', 2: 'A', 3: 'D', 4: 'G', 5: 'B', 6: 'E'}
    oct = {1: '2', 2: '2', 3: '3', 4: '3', 5: '3', 6: '4'}
    type = {4096: 'whole', 3072: 'half', 2048: 'half', 1536: 'quarter', 1024: 'quarter', 768: 'eighth', 512: 'eighth',
            384: '16th', 256: '16th', 192: '32th', 128: '32th', 96: '64th', 32: '64th', 48: '64th'}
    while i < len(dec_notes):
        # structure of the measure
        measure = ET.SubElement(part, 'measure', {'number': str(n_measure)})
        n_measure += 1
        # <attributes>
        #     <divisions>1024</divisions>
        att = ET.SubElement(measure, 'attributes')
        if n_measure == 1:
            tmp = ET.SubElement(att, 'division')
            tmp.text = str(division)
        # <key>
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
        tmp.text = str(1)
        #     <clef>
        #       <sign>TAB</sign>
        #       <line>6</line>
        #     </clef>
        clef = ET.SubElement(att, 'clef')
        tmp = ET.SubElement(clef, 'sign')
        tmp.text = "G"
        tmp = ET.SubElement(clef, 'line')
        tmp.text = str(2)
        # </attributes>
        totDuration = 0
        # putting the notes in the measure
        # whole_bar = True
        while totDuration < division * 4 and i < len(dec_notes):
            # <note>

            note = ET.SubElement(measure, 'note')
            #     <pitch>
            #       <step>G</step>
            #       <alter>1</alter>
            #       <octave>5</octave>
            #     </pitch>
            pitch = ET.SubElement(note, 'pitch')

            if dec_notes[i][1] != 'pause':  # nota
                tmp = ET.SubElement(pitch, 'step')
                tmp.text = dec_notes[i][1][1]
                tmp = ET.SubElement(pitch, 'alter')
                if dec_notes[i][1][0]:
                    tmp.text = "1"
                tmp = ET.SubElement(pitch, 'octave')
                tmp.text = str(dec_notes[i][0])
            else:  # pausa
                ET.SubElement(note, 'rest')

            # <duration>512</duration>
            tmp = ET.SubElement(note, 'duration')
            # if (totDuration + dec_notes[i][2]) <= division:
            #     print 'nota ok'
            tmp.text = str(dec_notes[i][2])
            # else:
            #     tmp.text = str(division * 4 - totDuration)
            #     # print dec_notes[i][2], ' ', tmp.text
            #     whole_bar = False

            # <voice>0</voice>
            tmp = ET.SubElement(note, 'voice')
            tmp.text = '1'

            #     <type>eighth</type>
            #     <sharp>1<\sharp>
            tmp = ET.SubElement(note, 'type')
            tmp.text = type[dec_notes[i][2]]
            if dec_notes[i][1][0]:
                tmp = ET.SubElement(note, 'accidental')
                tmp.text = "sharp"
            if dec_notes[i][2] in (3072, 1536, 768, 384, 192):
                ET.SubElement(note, 'dot')

            # if not whole_bar:
            #     tmp = ET.SubElement(note, 'notation')
            #     ET.SubElement((ET.SubElement(tmp, 'accidental')), 'detached-legato',
            #                   {'default-x': "0", 'default-y': "6", 'placement': "above"})
            # # </note>
            #
            # totDuration += dec_notes[i][2]
            # if whole_bar:
            #     i += 1
            # else:
            #     dec_notes[i] = list(dec_notes[i])
            #     dec_notes[i][2] -= division - totDuration
            #     dec_notes[i] = tuple(dec_notes[i])
            #     whole_bar = False

            totDuration += dec_notes[i][2]
            i += 1
    indent(tree.getroot())
    del strings, oct, i

    with open(name, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n'
                '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 2.0 Partwise//EN" "musicxml20/partwise.dtd">\n')
        tree.write(f, encoding='utf-8', method="xml")

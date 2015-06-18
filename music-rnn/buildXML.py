__author__ = 'Andrea'

import xml.etree.ElementTree as ET

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

def create_music_xml(dec_notes, division, name):
    tree = ET.parse('../files/toGenerate/EmptyXML.xml')
    part = tree.find('.//part')
    i = 0
    n_measure = 1
    strings = {1: 'E', 2: 'A', 3: 'D', 4: 'G', 5: 'B', 6: 'E'}
    oct = {1: '2', 2: '2', 3: '3', 4: '3', 5: '3', 6: '4'}
    type = {4096: 'whole', 3072: 'half', 2048: 'half', 1536: 'quarter', 1024: 'quarter', 768: 'eight', 512: 'eight', 256: '16th'}
    while i < len(dec_notes):
        # structure of the measure
        measure = ET.SubElement(part, 'measure', {'number': str(n_measure)})
        n_measure += 1
        # <attributes>
        #     <divisions>1024</divisions>
        att = ET.SubElement(measure, 'attributes')
        tmp = ET.SubElement(att, 'division')
        tmp.text = str(1024)
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
        complete_measure = False
        # putting the notes in the measure
        while totDuration < division and i < len(dec_notes):
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
            tmp = ET.SubElement(pitch, 'octave')
            tmp.text = str(dec_notes[i][0])
            tmp = ET.SubElement(note, 'alter')
            if dec_notes[i][1][0]:
                tmp.text = '1'
            #     <duration>512</duration>
            tmp = ET.SubElement(note, 'duration')
            tmp.text = str(dec_notes[i][2])
            #     <voice>0</voice>
            tmp = ET.SubElement(note, 'voice')
            tmp.text = '0'
            # #     <type>eighth</type>
            # #       <dynamics>
            # #         <f/>
            # #       </dynamics>
            # tmp = ET.SubElement(note, 'type')
            # tmp.text = type[dec_notes[i][2]]
            # if dec_notes[i][2] in (3072, 1536, 768, 384, 192):
            #     ET.SubElement(note, 'dot')
            # dyn = ET.SubElement(note, 'dynamics')
            # ET.SubElement(dyn, 'f')
            # </note>

            totDuration += dec_notes[i][2]
            if i >= len(dec_notes):
                complete_measure = True
            i += 1
        # complete the last measure if it is not full
        # if complete_measure
    indent(tree.getroot())
    del strings, oct, i
    tree.write(name, xml_declaration=True, encoding='utf-8', method="xml")
# -*- coding: utf-8 -*-
"""
Example of use Elman recurrent network
=====================================
Task: Detect the amplitudes
"""
import glob
import neurolab as nl
import numpy as np
import xml.etree.ElementTree as ET

# Create train samples
from modules.classes import Note
division = 1024
files = glob.glob("../files/train/*.xml")
coded_notes = []
# extracting all the notes
for file in files:
    print "\nfile: " + file
    tree = ET.parse(file)
    # notes = [Note(note, division, step_time) for note in tree.findall('.//note')]
    notes = [Note(note, division) for note in tree.findall('.//note')]
    for note in notes:
        coded_notes.append(note.encode())
inpt = []
target = []
# for i in range(0, len(coded_notes), 1):
#     if i + 9 < len(coded_notes):
#             inpt.append(list(coded_notes[i] + coded_notes[i + 1] + coded_notes[i + 2] + coded_notes[i + 3] + coded_notes[i + 4] + coded_notes[i + 5]
#                  + coded_notes[i + 6] + coded_notes[i + 7]))
#             target.append(list(coded_notes[i + 8]))

for i in range(0, len(coded_notes), 1):
    if i + 1 < len(coded_notes):
        inpt += list(coded_notes[i])
        target += list(coded_notes[i + 1])
inpt = np.array(inpt)
target = np.array(target)

# Create network with 3 layers
net = nl.net.newelm([[0, 1], [0, 1], [0, 1]], [10, 3], [nl.trans.TanSig(), nl.trans.PureLin()])
# Set initialized functions and init
net.layers[0].initf = nl.init.InitRand([-0.5, 0.5], 'wb')
net.layers[1].initf = nl.init.InitRand([-0.5, 0.5], 'wb')
net.init()
# Train network
error = net.train(inpt, target, epochs=100, show=1, goal=0.01)
# Simulate network
output = net.sim(inpt)

# Plot result
import pylab as pl
pl.subplot(211)
pl.plot(error)
pl.xlabel('Epoch number')
pl.ylabel('Train error (default MSE)')

pl.subplot(212)
pl.plot(target.reshape(80))
pl.plot(output.reshape(80))
pl.legend(['train target', 'net output'])
pl.show()

#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 13 May, 2019
"""
import sys, io
import wave, struct, datetime
from exe3 import *
from signal_functions import *

## Define Globals
HEADSIZE = 48
BITRATE = 192000


## Open stdin as a file
f = open( sys.stdin.fileno(), "rb", buffering=BITRATE)

## Remove the wav header, and keep it
head = f.read(HEADSIZE)

## Spawn an infinite loop to listen to stdin forever
while True:
    ## Read from stdin file object, prepending the head to it.
    fakeWavData = head + f.read(BITRATE)

    ## Create a file-like object from fakeWavData
    wavFLO = io.BytesIO( fakeWavData ) # FLO (file like object)

    ## Open fakeWavFile with Python Wave Module
    wav = wave.open( wavFLO )

    ## Throw away the head
    wav.readframes(HEADSIZE)

    ## Get all the data
    samples_bytes = wav.readframes(BITRATE)

    samples = struct.unpack("<%ih"%(len(samples_bytes)/2), samples_bytes)
    samples = [int(i / 256) for i in samples]

    ## Convert to numpy array
    samples = np.array(samples)



    ## Smooth samples
    samples = smooth_samples(samples)

    pulses = extract_data_pulses(samples)


    for pulse in pulses:
        pos, neg = split_samples(pulse)

        pos = samples2signal(pos)
        neg = samples2signal(neg)

        pos_msg = process_message(manchester_decode(pos))
        neg_msg = process_message(manchester_decode(neg))

        print(pos_msg)
        print(neg_msg)

        print(hex2data(pos_msg))
        print(hex2data(neg_msg))
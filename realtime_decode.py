#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 13 May, 2019
"""
import sys, io
import wave, struct, datetime
import numpy as np
import signal_functions
import message_functions


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
    samples = signal_functions.smooth_samples(samples)

    pulses = signal_functions.extract_data_pulses(samples)


    for pulse in pulses:
        pos, neg = signal_functions.split_samples(pulse)

        pos = signal_functions.samples2signal(pos)
        neg = signal_functions.samples2signal(neg)

        pos_msg = message_functions.process_message(signal_functions.manchester_decode(pos))
        neg_msg = message_functions.process_message(signal_functions.manchester_decode(neg))

        print(pos_msg)
        print(neg_msg)

        print(message_functions.hex2data(pos_msg))
        print(message_functions.hex2data(neg_msg))
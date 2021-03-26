#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 28 February, 2021
"""
import sys
import struct
import wave
import numpy as np
import signal_functions
import message_functions


def read_wav_file(path):
    """
    Reads a wav file, and returns samples as numpy array of signed integer 
    values.

    Args: 
        path (str): The path of the wave file to read.
    
    Returns:
        samples (np.array): An array of the sample values. -128 to 128 signed 
        integers.
    """
    ## Read in file arg
    wav = wave.open(path)

    ## Throw away the file header
    #wav.readframes(head_size)

    ## Get all the samples in file
    samples_bytes = wav.readframes(wav.getnframes())


    ## Convert bytes to list of signed integers
    samples = struct.unpack("<%ih"%(len(samples_bytes)/2), samples_bytes)
    samples = [int(i / 256) for i in samples]

    ## Convert to numpy array
    samples = np.array(samples)

    ## Return samples array 
    return samples  


def pretty_print_data(data):
    """
    Pretty prints the data tuple returned from message_functions.hex2data 
    function.
    """
    print(f"Sensor {data[0]} on channel {data[1]} reports: {data[3]}°C, and {data[4]}%.")


def main(file_path):
    """
    Takes a file path, decodes and prints any Oregon Scientific RFv2 found 
    within.
    """
    ## Read sample array from file
    samples = read_wav_file(file_path)

    ## Smooth samples
    samples = signal_functions.smooth_samples(samples)

    ## Extract list of only revelvent data
    pulses = signal_functions.extract_data_pulses(samples)

    ## Alert and exit if file has no data
    if len(pulses) == 0:
        print("No data was found in given file.")
        return

    for pulse in pulses:
        ## Split samples into positive and negative channels
        positive_samples, negative_samples = signal_functions.split_samples(pulse)

        ## Convert samples to signal
        positive_signal = signal_functions.samples2signal(positive_samples)
        negative_signal = signal_functions.samples2signal(negative_samples)

        ## manchester_decode signal into a binary string
        positive_manchester = signal_functions.manchester_decode(positive_signal, 40)
        negative_manchester = signal_functions.manchester_decode(negative_signal, 40)

        ## Convert bin string msg to hex message
        positive_message = message_functions.process_message(positive_manchester)
        negative_message = message_functions.process_message(negative_manchester)
        
        ## Extract data from positive hex message
        msg_valid, msg_data = message_functions.hex2data(positive_message)

        ## Print msg_data if message was valid
        if msg_valid:
            pretty_print_data(msg_data)

        ## Extract data from negative hex message
        msg_valid, msg_data = message_functions.hex2data(negative_message)

        ## Print msg_data if message was valid
        if msg_valid:
            pretty_print_data(msg_data)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        main(file_path)    
    else:
        print("Error: Please input a single file.")

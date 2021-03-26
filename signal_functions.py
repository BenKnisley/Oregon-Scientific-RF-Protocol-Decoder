"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 26 March, 2021
"""
import numpy as np
from scipy.signal import filtfilt, butter


def smooth_samples(samples):
    """
    Smooths out any major waves crossing the 0-axis. 
    
    Normalizes values back around 0-axis, by using a Butterworth filter to 
    create a average value index and then subtracting original values from it.

    Args:
        samples (np.array): The array of samples to process.
    
    Returns: 
        smooth_samples (np.array): The smoothed array of samples.
    """
    ## Create a reference array of smoothed data 
    reference = samples.copy()
    b, a = butter(8, 0.01)
    #b, a = butter(8, 0.008)
    reference = filtfilt(b, a, reference)

    ## Subtract samples from smoothed signal to normalize values
    smooth_samples = samples - reference

    ## Return final signal
    return smooth_samples


def extract_data_pulses(samples):
    """
    Finds and returns a list of cropped data pulses.
    """
    ##
    reference = np.abs(samples*1.25)
    b, a = butter(8, 0.008)
    reference = filtfilt(b, a, reference)
    reference = samples2signal(reference, 8)

    pulses = []

    current_bit = int(not reference[0])

    while current_bit in reference:
        clip_point = np.where(reference == current_bit)[0][0]

        if not current_bit:
            pulse = samples[:clip_point]
            if len(pulse) > 100:

                ## Clip to first high 
                one_inx = np.where(pulse > 16)[0][0]
                pulse = pulse[one_inx:]

                pulses.append(pulse)

        reference = reference[clip_point:]
        samples = samples[clip_point:]

        current_bit = int(not current_bit)
    
    return pulses

##
def split_samples(samples):
    """
    Splits a sample array into positive values, and negative values channels.
    """
    positive_samples = samples.copy()
    negative_samples = samples.copy()

    positive_samples[positive_samples < 0] = 0
    negative_samples[negative_samples > 0] = 0
    negative_samples = np.abs(negative_samples)

    return positive_samples, negative_samples


def samples2signal(samples, threshold=16):
    """
    Returns a signal from an sample array.
    """
    samples[samples < threshold] = 0
    samples[samples >= threshold] = 1
    signal = samples.astype(int)
    return signal


def get_cycle_sizes(signal):
    transitions = []

    current_bit = bool(signal[0])

    while int(not current_bit) in signal:
        transition = np.where(signal == int(not current_bit))[0][0]
        transitions.append(transition)
        signal = signal[transition:]
        current_bit = bool(signal[0])
    return transitions


def manchester_decode(signal, break_point=40):
    """
    Decodes a manchester encoded signal to a binary message.
    """
    cycle_sizes = get_cycle_sizes(signal)
    
    flip_value = []
    indx = 0
    while indx < len(cycle_sizes):
        cycle_size = cycle_sizes[indx]
        if cycle_size > break_point:
            flip_value.append(True)
        else:
            flip_value.append(False)
            indx += 1 ## Skip next value
        indx += 1

    data = ''
    current_bit = 1
    for flip in flip_value:
        if flip:
            current_bit = not current_bit
        data += str(int(current_bit))
    
    return data
    

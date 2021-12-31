#!/usr/bin/python3

from microphone import MICROPHONE_CHUNK_SIZE, Microphone
import struct
import math
from numpy import fft as fft

RATE = 48000
SECONDS = 5
SHORT_NORMALIZE = (1.0 / 32768.0)
SOME_RANDO_AMPLITUDE = 0.1


def get_rms(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n

    return math.sqrt(sum_squares / count)


if __name__ == '__main__':
    mic = Microphone(channels=1, bitrate=RATE)
    frames = []

    print('\nListening...')
    mic.start()

    for i in range(0, int(RATE / MICROPHONE_CHUNK_SIZE * SECONDS)):
        data = mic.read()
        frames.append(data)
        if get_rms(data) > SOME_RANDO_AMPLITUDE:
            print('Loud sound detected')

    print('Stopping microphone after {} seconds...'.format(SECONDS))
    mic.close()

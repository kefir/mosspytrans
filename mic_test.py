#!/usr/bin/python3

from microphone import MICROPHONE_CHUNK_SIZE, Microphone
import struct
import math
from numpy import fft as fft
from panel_sim import PanelType, PanelGeometry, PanelSim

RATE = 48000
SECONDS = 5
SHORT_NORMALIZE = (1.0 / 32768.0)
SOME_RANDO_AMPLITUDE = 0.1

PANEL_SIDE_SIZE = 8


def panel_sim_init() -> PanelSim:
    panel = PanelSim(width=PANEL_SIDE_SIZE, height=PANEL_SIDE_SIZE)
    return panel


def get_rms(block) -> float:
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


def get_second_rms(dt: float):

    data = mic.read()
    rms = get_rms(data)

    rms_color = int(rms * 255.0)
    rms_color += 50
    color = (rms_color, int(rms_color/2), int(rms_color*2), 255)

    # if get_rms(data) > SOME_RANDO_AMPLITUDE:
    #     color = (255, 123, 123, 255)

    panel.label_text_update('{:02.4f}'.format(rms), color)


if __name__ == '__main__':
    mic = Microphone(channels=1, bitrate=RATE)

    mic.start()

    panel = panel_sim_init()
    panel.window().set_caption('MossPyTrans')
    panel.label_update_set(get_second_rms, 0.0000001)
    panel.run()

    print('Stopping microphone')
    mic.close()

import serial
import numpy as np
from struct import *
import os
from uwb_utils.DecaUWB_interface import UWBSensorInterface
import time
import csv
import pandas as pd
from collections import deque
from matplotlib import pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks


def fit_knot(x_y, knot_num=2, x_start=-5, x_stop=60):
    x_range = x_stop - x_start
    step_size = 1 / knot_num
    time_stamp = np.linspace(x_start, x_stop, x_range * knot_num, endpoint=False)

    # print(step_size)

    amp = np.zeros(time_stamp.size)
    counter = np.zeros(time_stamp.size)

    # print(np.max(x_y[:, 0]))
    for xy in x_y:
        if xy[0] < x_stop - 0.5 * step_size:
            knot_index = int((xy[0] - x_start + 0.5 * step_size) // step_size)

            amp[knot_index] = xy[1] + amp[knot_index]
            counter[knot_index] += 1

    if 0 in amp:
        amp[0] = amp[1]
        counter[0] = counter[1]

    amp = amp / counter

    fitted = np.vstack((time_stamp, amp)).T
    return fitted


def peaks_detection(x_y, threshold, distance, width, prominence):
    x = x_y[:, 0]
    y = x_y[:, 1]
    peaks, properties = find_peaks(y, height=threshold,
                                   distance=distance,
                                   width=width,
                                   prominence=prominence)

    return np.vstack((x[peaks], y[peaks])).T


def average_delay_key_generation(peaks_xy, key_Length):
    # extracting n highest peaks
    peak_nums = key_Length + 1
    y = peaks_xy[:, 1]

    # index of all the picks

    peaks_index = y.argsort()[-peak_nums:]
    # [::-1]
    peaks_index = np.sort(peaks_index)
    peaks_xy_useful = np.array([peaks_xy[i] for i in peaks_index])
    # peaks_xy_useful = peaks_xy[0:key_Length+1,:]
    print(peaks_xy_useful)

    # use filtered peaks for key generation
    peaks_useful_x = peaks_xy_useful[:, 0]
    peaks_useful_y = peaks_xy_useful[:, 1]
    print(peaks_useful_x)
    # print(peaks_useful_y)

    average_delay = (peaks_useful_x[-1] - peaks_useful_x[0]) / key_Length

    relative_delay = np.diff(peaks_useful_x)

    key = []

    for i in relative_delay:
        key.append(0) if i < average_delay else key.append(1)

    # print(key)

    return key


# def mag_key_generation(peaks_xy, key_Length):
#     # extracting n highest peaks
#     peak_nums = key_Length + 1
#     y = peaks_xy[:, 1]
#
#     # index of all the picks
#
#     peaks_index = y.argsort()[-peak_nums:]
#     # [::-1]
#     peaks_index = np.sort(peaks_index)
#     peaks_xy_useful = np.array([peaks_xy[i] for i in peaks_index])
#     # peaks_xy_useful = peaks_xy[0:key_Length+1,:]
#     print(peaks_xy_useful)
#
#     # use filtered peaks for key generation
#     peaks_useful_x = peaks_xy_useful[:, 0]
#     peaks_useful_y = peaks_xy_useful[:, 1]
#
#     # quantize the highest key_length peaks
#     mag_max =
#
#
#     return key


def complete_average_delay_key_generation(peaks_xys, key_Length=4):
    complete_key = []
    for peaks_xy in peaks_xys:
        key = average_delay_key_generation(peaks_xy, key_Length=key_Length)
        complete_key.append(key)

    complete_key = np.array(complete_key)
    return np.array(complete_key)


def cir_group_generation(frames_raw, frame_length=65, frame_per_cir=100,
                         knot_num=2, x_start=-5, x_stop=60
                         ):
    #     we should have 450 groups cir generated
    cirs = []

    for i in range(0, int(frames_raw.shape[0] / frame_length - frame_per_cir)):
        cir_raw = frames_raw[i * frame_length: (i + frame_per_cir) * frame_length]

        cir = fit_knot(cir_raw, knot_num=knot_num, x_start=x_start, x_stop=x_stop)
        cirs.append(cir)
        i += 1

    cirs = np.array(cirs)
    return cirs


def keys_generation(cirs):
    keys = []
    for cir in cirs:
        peaks = peaks_detection(x_y=cir, threshold=1000, distance=4, width=1, prominence=500)
        print()

        key = average_delay_key_generation(peaks_xy=peaks, key_Length=8)

        plt.plot(cir[:, 0], cir[:, 1])
        plt.plot(peaks[:, 0], peaks[:, 1], "x")
        plt.show()
        print(key)

        keys.append(key)

    keys = np.array(keys)
    return keys


def error_analysis(key1, key2, keyLength):
    return

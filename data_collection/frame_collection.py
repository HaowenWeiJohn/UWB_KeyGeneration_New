import serial
import numpy as np
from struct import *
import os
#  we are reading distance information from anchor
from uwb_utils.DecaUWB_interface import UWBSensorInterface
import time
import csv
import pandas as pd
from collections import deque
from matplotlib import pyplot as plt

measure_num = 550
frame_size = 65 * 4 * 2 + 8 * 4
Anchor = UWBSensorInterface('Anchor', frame_size=frame_size)
Anchor.connect_virtual_port('COM32')

data_buffer = []

if __name__ == '__main__':
    i = 0
    ranging_info = 0
    while i < measure_num:
        ranging_info = Anchor.generate_frame()
        if ranging_info is not None:
            data_buffer.append(ranging_info)

            i += 1

    data_buffer = np.array(data_buffer)
    data_buffer = data_buffer.reshape(-1, 7)
    print(data_buffer)
    y1, y2, y3, x = data_buffer[:, 0], data_buffer[:, 1], data_buffer[:, 2], data_buffer[:, 3]
    plt.figure(figsize=(25, 25))
    plt.scatter(x, y1)
    plt.scatter(x, y2)
    plt.show()
    plt.figure(figsize=(25, 25))
    plt.scatter(x, y3)
    plt.show()

    df = pd.DataFrame(data=data_buffer, columns=["real", "img", "mag", "time_stamp", "tof", "rsl", "fsl"])
    df.to_csv('5ft_new.csv')

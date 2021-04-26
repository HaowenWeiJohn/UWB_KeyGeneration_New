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
from algorithm_utils.keyGeneration_utils import *

cir_df = pd.read_csv('../archieve_data/5m_Anchor_living_LOS.csv')
cir_df_less = cir_df.tail(50 * 65)
x_y = cir_df_less[['time_stamp', 'mag']]


fitted = fit_knot(np.array(x_y), knot_num=5, x_start=-5, x_stop=60)

peaks_detection(x_y=fitted, threshold=1000, distance=10, width=4, prominence=0)


cir_df = pd.read_csv('../archieve_data/5m_Tag_living_LOS.csv')
cir_df_less = cir_df.tail(50 * 65)
x_y = cir_df_less[['time_stamp', 'mag']]


fitted = fit_knot(np.array(x_y), knot_num=5, x_start=-5, x_stop=60)


peaks = peaks_detection(x_y=fitted, threshold=1000, distance=5, width=3, prominence=0)
average_delay_key_generation(peaks_xy=peaks, key_Length=4)


group_test = cir_df[['time_stamp', 'mag']]
cirs = cir_group_generation(np.array(group_test), frame_length=65, frame_per_cir=50)




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

anchor_2_los = np.array(pd.read_csv('../archieve_data/2m_Anchor_living_LOS.csv')[['time_stamp', 'mag']])[50 * 65:, :][
               ::2]
anchor_3_los = np.array(pd.read_csv('../archieve_data/3m_Anchor_living_LOS.csv')[['time_stamp', 'mag']])[50 * 65:, :][
               ::2]
anchor_4_los = np.array(pd.read_csv('../archieve_data/4m_Anchor_living_LOS.csv')[['time_stamp', 'mag']])[50 * 65:, :][
               ::2]
anchor_5_los = np.array(pd.read_csv('../archieve_data/5m_Anchor_living_LOS.csv')[['time_stamp', 'mag']])[50 * 65:, :][
               ::2]


tag_2_los = np.array(pd.read_csv('../archieve_data/2m_Tag_living_LOS.csv')[['time_stamp', 'mag']])[25 * 65: 525 * 65,
            :]
tag_3_los = np.array(pd.read_csv('../archieve_data/3m_Tag_living_LOS.csv')[['time_stamp', 'mag']])[25 * 65: 525 * 65,
            :]
tag_4_los = np.array(pd.read_csv('../archieve_data/4m_Tag_living_LOS.csv')[['time_stamp', 'mag']])[25 * 65: 525 * 65,
            :]
tag_5_los = np.array(pd.read_csv('../archieve_data/5m_Tag_living_LOS.csv')[['time_stamp', 'mag']])[25 * 65: 525 * 65,
            :]


anchor_2_los = cir_group_generation(anchor_2_los)
keys_anchor_2_los = keys_generation(anchor_2_los)

tag_2_los = cir_group_generation(tag_2_los)
keys_tag_2_los = keys_generation(tag_2_los)



# anchor_5_los = cir_group_generation(anchor_5_los)
# keys_anchor_5_los = keys_generation(anchor_5_los)
#
# tag_5_los = cir_group_generation(tag_5_los)
# keys_tag_5_los = keys_generation(tag_5_los)


plt.plot()
a = 1






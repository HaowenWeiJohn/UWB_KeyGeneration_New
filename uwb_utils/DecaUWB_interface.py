import serial
import numpy as np
from struct import *
import os


class UWBSensorInterface:

    def __init__(self, role, frame_size, baud_rate=9600, uport=None, exe_file=None):

        self.role = role
        self.baud_rate = baud_rate
        self.frame_size = frame_size
        self.data_buffer = b''
        self.uport = uport
        self.exe_file = None
        self.connected = False

    def connect_virtual_port(self, virtual_port):
        try:
            self.uport = serial.Serial(port=virtual_port, baudrate=self.baud_rate, timeout=0)
            self.uport.flushOutput()
            self.connected = True

        except:
            print("port is in use or not open")
            return

    def generate_frame(self):

        # print(len(bits))
        self.data_buffer += self.uport.readline()

        # print(len(self.data_buffer))
        if len(self.data_buffer) >= self.frame_size:

            real_imag_pairs = np.reshape(unpack("i" * 130, self.data_buffer[0:self.frame_size - 8 * 4]), (-1, 2))
            HLP_TOF_RSL_FSL = np.array(unpack("d" * 4, self.data_buffer[self.frame_size - 8 * 4:]))
            mag = np.sqrt(np.square(real_imag_pairs[:, 0]) + np.square(real_imag_pairs[:, 1])).reshape(-1, 1)
            leading_index = HLP_TOF_RSL_FSL[0]
            TOF_RSL_FSL = [HLP_TOF_RSL_FSL[1:]] * 65

            back_trace_index = 4 + leading_index - (int)(leading_index)
            time_stamp = (np.array(range(0, 65)) - back_trace_index).reshape(-1, 1)

            # uwb_data = np.reshape(unpack("d" * 2, self.data_buffer[0:self.frame_size]), (-1, 2))
            # uwb_data = np.array(unpack("d" * 2, self.data_buffer[0:self.frame_size]))
            rangingInfo = np.hstack((real_imag_pairs, mag, time_stamp, TOF_RSL_FSL))

            self.data_buffer = self.data_buffer[self.frame_size:]

            return rangingInfo
        else:
            return None

    def disconnect_virtual_port(self):
        try:
            self.uport.close()
        except:
            print("already closed or cannot close")
            return

    def start_sensor(self, exe_path):
        self.exe_file = exe_path
        try:
            os.system("taskkill /im " + exe_path)
            os.startfile(exe_path)
        except:
            print("cannot open sensor")
            return

    def stop_sensor(self):
        os.system("taskkill /im " + self.exe_file)
        os.startfile(self.exe_file)

import numpy as np
import pandas as pd
import utils
import time

class Brain_waves:
    def __init__(self, eeg, channels,fs, frame=200):

        self.eeg = eeg
        self.fs = fs
        self.frame = frame
        self.channels_num = channels
        self.flag = False
        self.buff = 2500
        self.data = []
        self.delim = ','


    def callback_main(self, sample):
        if self.flag:
            if len(self.data) != 0 and len(self.data) %self.frame == 0:
                self.data = self.data[-self.buff:]
                for i in range(len(self.callbacks)):
                    data = np.array(self.data).transpose()
                    band = self.bands[i]
                    freq = [ i[-1] for i in self.analyze(data, band)]
                    self.callbacks[i](freq)

            channel_data = sample.channel_data
            self.data.append(channel_data)
            if self.save_path != None:
                row = ''
                row += str(time.time())
                row += self.delim
                row += str(sample.id)
                row += self.delim
                for i in sample.channel_data:
                    row += str(i)
                    row += self.delim
                for i in sample.aux_data:
                    row += str(i)
                    row += self.delim
                row += '\n'
                with open(self.save_path, 'a') as f:
                    f.write(row)


    def analyze(self, data, band):
        band_vals = []
        for i in range(self.channels_num):
            clear_data = utils.bandpass(band[0], band[1], data[i], self.fs)
            _band_val = utils.frequency_of_channel_band(clear_data, band, self.fs, self.frame)
            band_vals.append(_band_val)
        return band_vals


    def start_streaming(self, func, band, time_limit, file_name = None):
        self.flag = True
        self.save_path = file_name
        if type(func) != list:
            func = [func]
        if type(band) != list:
            band = [band]
        if len(func) != len(band):
            raise AssertionError("number of functions and bands are not equal")
        self.callbacks = func
        self.bands = band
        self.eeg.start_streaming(self.callback_main, time_limit)


    def read_csv_waves(self, file_name, band):
        eeg_data = pd.read_csv(file_name, sep=self.delim, header=None, index_col=False).values
        raw_data = eeg_data[:, 2:2 + self.channels_num].transpose()
        time_lenght = eeg_data[:, 0][-1] - eeg_data[:, 0][0]
        band_vals = self.analyze(raw_data, band)
        time = np.linspace(0,time_lenght, len(band_vals[0]))
        return band_vals, time

import numpy as np
from scipy import signal

eeg_bands = {'delta': (0, 4),
             'theta': (4, 8),
             'alpha': (8, 12),
             'beta': (12, 30),
             'gamma': (30, 45)}


def bandpass(start, stop, data, fs):
    bp_Hz = np.array([start, stop])
    b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
    return signal.lfilter(b, a, data, axis=0)


def notch(val, data, fs):
    bp_stop_Hz = val + 3.0 * np.array([-1, 1])
    b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
    fin = signal.lfilter(b, a, data)
    return fin


def fft(data, fs):
    L = len(data)
    freq = np.linspace(0.0, 1.0 / (2.0 * fs **-1), int(L / 2))
    yi = np.fft.fft(data)#[1:]
    y = yi[range(int(L / 2))]
    return freq, abs(y)


def frequency_bands(one_channel_frame_data, band, fs):
    freq, y = fft(one_channel_frame_data, fs)
    freq_ix = np.where((freq >= band[0]) &
                       (freq <= band[1]))[0]
    dat = np.mean(y[freq_ix])
    return dat


def _split(channel_data, frame):
    frame_len = frame
    chunks = len(channel_data) // frame_len
    if chunks == 0:
        chunks = 1
    data = np.array_split(channel_data, chunks)
    return data


def frequency_of_channel_band(channel_data, band, fs, frame):
    splited = _split(channel_data,frame)
    data = []
    for i in range(len(splited)):
        dat = frequency_bands(splited[i],band, fs)
        data.append(dat)
    return data
# Brain waves analyzer for OpenBci

Bci tool for real time brain waves frequency analysis for [OpenBci](https://openbci.com/) eeg devices.
#### Dependencies
- numpy==1.14.3
- pandas==0.22.0
- scipy==1.0.0

For usage [OpenBCI_Python](https://github.com/OpenBCI/OpenBCI_Python) is needed.



#### Brain waves
Brain waves are produced by synchronised electrical pulses from neurons firing with each other, so are representing electrical activity of the brain part. They are detected using EEG.<br />
Brain waves are usually divided into bandwidths:  alpha, beta, delta, and theta

| name|frequency (Hz) |
| --------- | -----:|
| alpha  |8-13 |
| beta     |  13-30 |
| delta|   1-5 |
| theta|  4-8|

- ***Alpha***: In general, the alpha rhythm is the prominent EEG wave pattern of an adult who is awake but relaxed with eyes closed. Each region of the brain had a characteristic alpha rhythm but alpha waves of the greatest amplitude are recorded from the occipital and parietal regions of the cerebral cortex. In general, amplitudes of alpha waves diminish when subjects open their eyes and are attentive to external stimuli although some subjects trained in relaxation techniques can maintain high alpha amplitudes even with their eyes open.


- ***Beta***: Beta rhythms occur in individuals who are alert and attentive to external stimuli or exert specific mental effort, or paradoxically, beta rhythms also occur during deep sleep, REM (Rapid Eye Movement) sleep when the eyes switch back and forth.  This does not mean that there is less electrical activity, rather that the “positive” and “negative” activities are starting to counterbalance so that the sum of the electrical activity is less.  Thus, instead of getting the wave-like synchronized pattern of alpha waves, desynchronization or alpha block occurs.  So, the beta wave represents arousal of the cortex to a higher state of alertness or tension.  It may also be associated with “remembering” or retrieving memories.



- ***Delta and Theta***: Delta and theta rhythms are low-frequency EEG patterns that increase during sleep in the normal adult.  As people move from lighter to deeper stages of sleep (prior to REM sleep), the occurrence of alpha waves diminish and is gradually replaced by the lower frequency theta and then delta frequency rhythms.

> from: [psych.westminster.edu](http://www.psych.westminster.edu/psybio/BN/Labs/Brainwaves.htm)

#### Usage
***Real time***</br>
start_streaming function of Brain_waves object takes a callback function or list of functions. Every frame (if frame = 200, and record frequency = 200, every 1 second) magnitude of the specified band or list of bands is computed and is passed to the callback function as an argument in form : [channel1 amplitude, channel2 amplitude, ...channelx amplitude]
If file_name is specified, data are saved in csv file.
```python
import brain_waves_openbci
from openbci.ganglion import OpenBCIGanglion #import OpenBCI_Python module

eeg_device = OpenBCIGanglion()
number_of_channels = 4
recording_frequency = 200
frame = 200
brw = brain_waves.Brain_waves(eeg_device, number_of_channels, recording_frequency, frame = 200)

def example_callback(sample):
   print(sample)

time_limit = 20
band = (8,13) # alpha
brw.start_streaming(example_callback, band, time_limit,  file_name = 'data/test.csv')
```
***Read data and visualize***</br>
Recorded data can by read and analyzed with read_csv_waves. Vizualization can be useful for selecting threshold.

```python
import matplotlib.pyplot as plt
import brain_waves_openbci as waves

number_of_channels = 4
recording_frequency = 200
br = waves.Brain_waves(None, number_of_channels, recording_frequency)
band = (13,30) # beta
band_vals, time = br.read_csv_waves('data/data_test.csv', band)
plt.plot(time, band_vals[0]) #plot first channel data
plt.show()
```
J.M.

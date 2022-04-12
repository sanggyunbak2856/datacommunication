import math

import scipy.fftpack
import numpy as np

SHORTMAX = 2**(16-1)-1
channels = 1
length = 5.0
samplerate = 48000
frequencies = [261.625, 523.251, 1046.502] # C4, C5, C6
volumes = [1.0, 0.75, 0.5]
waves = []

for frequency, volume in zip(frequencies, volumes):
    audio = []
    for i in range(int(length*samplerate)):
        audio.append(volume*SHORTMAX*math.sin(2*math.pi*frequency*i/samplerate))
    waves.append(audio)

track = [0]*int(length*samplerate)
for i in range(len(track)):
    for w, v in zip(waves, volumes):
        track[i] = track[i] + w[i]
    track[i] = track[i] / len(waves)

freq = scipy.fftpack.fftfreq(len(track))
fourier = scipy.fftpack.fft(track)
print(freq[np.argmax(abs(fourier))] * samplerate)

for i in range(len(freq)):
    if 261.125 <= freq[i]*samplerate and freq[i]*samplerate <= 262.125:
        print(f'{i} => {freq[i]*samplerate}')
    elif 522.751 <= freq[i]*samplerate and freq[i]*samplerate <= 523.751:
        print(f'{i} => {freq[i]*samplerate}')
    elif 1046.002 <= freq[i]*samplerate and freq[i]*samplerate <= 1047.002:
        print(f'{i} => {freq[i]*samplerate}')


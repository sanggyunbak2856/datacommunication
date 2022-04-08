import os
import sys
import re
import math
import wave
import struct
import statistics
import time

import pyaudio

import morsecode

FLAGS = _ = None
DEBUG = False
CHANNELS = 1
SAMPLERATE = 48000
FREQUENCY = 523.251
UNIT = 0.1
SHORTMAX = 2**(16-1)-1
MORSE_THRESHOLD = SHORTMAX // 4
UNSEEN_THRESHOLD = 3.0


def text2morse(text):
    text = text.upper()
# 텍스트를 모스코드로 만들기
    morse = ''
    for t in text:
        for key, value in morsecode.code.items():
            if t == key:
                morse = morse + value + ' '
        if t == ' ':
            morse = morse + ' ' # morse에 공백이 두칸인 경우 단어 사이 구분
    return morse


def morse2audio(morse):
    audio = []
    words = morse.split("  ") # 단어 사이 구분
# Need to edit below!
    for word in words:
        for m in word:
            if m == '.': # 짧은 음, 1unit
                for i in range(math.ceil(SAMPLERATE*UNIT)*1):
                    audio.append(int(SHORTMAX*math.sin(2*math.pi*FREQUENCY*i/SAMPLERATE)))
            elif m == '-': # 긴 음, 3unit
                for i in range(math.ceil(SAMPLERATE*UNIT)*3):
                    audio.append(int(SHORTMAX*math.sin(2*math.pi*FREQUENCY*i/SAMPLERATE)))
            elif m == ' ': # 문자 사이, 3unit, 3 - 1 - 1
                for i in range(math.ceil(SAMPLERATE*UNIT)*1):
                    audio.append(int(0))
            for i in range(math.ceil(SAMPLERATE*UNIT)*1): # 모스부호 사이의 구분, 1unit
                audio.append(int(0))
        for i in range(math.ceil(SAMPLERATE*UNIT)*6): # 단어 사이 구분, 7unit, 7 - 1
                audio.append(int(0))
        
# Need to edit above!
    return audio


def play_audio(audio):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLERATE,
                    frames_per_buffer=SAMPLERATE,
                    output=True)

    for a in audio:
        stream.write(struct.pack('<h', a))

    time.sleep(0.5/UNIT) # Wait for play

    stream.stop_stream()
    stream.close()
    p.terminate()

#temp
def audio2file(audio, filename):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(4)
        w.setframerate(48000)
        for a in audio:
            w.writeframes(struct.pack('<l', a))


def send_data():
    while True:
        print('Type some text (only English)')
        text = input('User input: ').strip()
        if re.match(r'[A-Za-z0-9 ]+', text):
            break
    morse = text2morse(text)
    print(f'MorseCode: {morse}')
    audio = morse2audio(morse)
    audio2file(audio, 't.wav')
    print(f'AudioSize: {len(audio)}')
    play_audio(audio)


def record_audio():
    unit_size = math.ceil(SAMPLERATE*UNIT)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLERATE,
                    frames_per_buffer=SAMPLERATE,
                    input=True)

# Need to edit below!
    morse = ''
    zerocount = 0
    start = False

    while True:
        unit = [] # 1unit data
        data = stream.read(unit_size) # 1unit
        for i in range(0, len(data), 2):
            d = struct.unpack('<h', data[i:i+2])[0]
            if abs(d) > MORSE_THRESHOLD: # 데이터가 임계값을 넘었는지 확인, 넘었다면 듣기 시작
                start = True
                break
        if start:
            for i in range(0, len(data), 2): # 1unit 데이터 듣기
                d = struct.unpack('<h', data[i:i+2])[0]
                unit.append(d)
            stdev = statistics.stdev(unit)
            print(stdev)
            if stdev > 3500: 
                zerocount = 0
                morse += '.'
            else:
                zerocount += 1
                morse += ' '
        if zerocount == 30:
            break
    
    morse = morse.replace('...', '-')
    morse = morse.rstrip()
# Need to edit above!

    return morse


def morse2text(morse):
    text = ''
# Need to edit below!
    morse_split= morse.split('   ')
    for m in morse_split:
        m = m.replace(" ", "")
        for key, value in morsecode.code.items():
            if m == value:
                text = text + key
        if m == '':
            text = text + ' '
    return text
        
# Need to edit above!


def receive_data():
    morse = record_audio()
    print(f'Morse: {morse}')
    text = morse2text(morse)
    print(f'Sound input: {text}')


def main():
    while True:
        print('Morse Code Data Communication 2022')
        print('[1] Send data over sound (play)')
        print('[2] Receive data over sound (record)')
        print('[q] Exit')
        select = input('Select menu: ').strip().upper()
        if select == '1':
            send_data()
        elif select == '2':
            receive_data()
        elif select == 'Q':
            print('Terminating...')
            break;


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                         help='The present debug message')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()


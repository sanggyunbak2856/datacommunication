import sys
import math
import wave
import struct
import statistics

english = {'A':'.-'   , 'B':'-...' , 'C':'-.-.' , 
           'D':'-..'  , 'E':'.'    , 'F':'..-.' , 
           'G':'--.'  , 'H':'....' , 'I':'..'   , 
           'J':'.---' , 'K':'-.-'  , 'L':'.-..' , 
           'M':'--'   , 'N':'-.'   , 'O':'---'  , 
           'P':'.--.' , 'Q':'--.-' , 'R':'.-.'  , 
           'S':'...'  , 'T':'-'    , 'U':'..-'  , 
           'V':'...-' , 'W':'.--'  , 'X':'-..-_', 
           'Y':'-.--' , 'Z':'--..'  }

number = { '1':'.----', '2':'..---', '3':'...--', 
           '4':'....-', '5':'.....', '6':'-....', 
           '7':'--...', '8':'---..', '9':'----.', 
           '0':'-----'}

def text2morse(text):
    text = text.upper()
    morse = ''
    
    for t in text:
        print(t)
        for key, value in english.items():
            if t == key:
                morse = morse + value
        for key, value in number.items():
            if t == key:
                morse = morse + value
        if t == ' ':
            morse = morse + '/' # 모스 부호에 공백 추가
        else:
            morse = morse + ' '
    return morse

def morse2audio(morse):
    t = 0.1
    fs = 48000
    f = 523.251
    audio = []
    INTMAX = 2**(32-1)-1
    for m in morse:
        if m == '.':
            for i in range(int(t*fs*1)):
                audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))
        elif m == '-':
            for i in range(int(t*fs*3)):
                audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))
        elif m == '/': # 단어 사이 (공백, 7-2-2)
            for i in range(int(t*fs*3)):
                audio.append(int(0))
        elif m == ' ': # 문자 사이 (3초, 3-2)
            for i in range(int(t*fs*1)):
                audio.append(int(0))
        for i in range(int(t*fs)): # 문자 사이
            audio.append(int(0))
    return audio


def audio2file(audio, filename):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(4)
        w.setframerate(48000)
        for a in audio:
            w.writeframes(struct.pack('<l', a))


text = input()
morse = text2morse(text)
print(morse)
audio = morse2audio(morse)
audio2file(audio,'t.wav')
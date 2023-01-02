import audiobusio
import audiocore
import board
import array
import time
import math
import keypad
import asyncio
import audiomixer
from ulab import numpy as np


i2s  = audiobusio.I2SOut(bit_clock=board.GP10, word_select=board.GP11, data=board.GP9)

sample_rate = 32000
tone_volume = 0.4  # Increase or decrease this to adjust the volume of the tone.



KEY_PINS = (
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7
)


mixer = audiomixer.Mixer(voice_count=8, sample_rate=sample_rate, channel_count=1,
                         bits_per_sample=16, samples_signed=False)

def generate_signal(frequency,volume=1):
    length = int(sample_rate // frequency)
    i = np.linspace(0,length,length)
    signal_decimal = np.linspace(0,length,length)

    #normalize signal
    """
    signal_decimal = np.sin(np.pi*2*i*frequency/sample_rate)*1\
        +(np.sin(np.pi*2*i*2*frequency/sample_rate)*0.4)\
        +(np.sin(np.pi*2*i*3*frequency/sample_rate)*0.2)\
        +(np.sin(np.pi*2*i*4*frequency/sample_rate)*0.2)\
        +(np.sin(np.pi*2*i*5*frequency/sample_rate)*0.05)\
        +(np.sin(np.pi*2*i*6*frequency/sample_rate)*0.05)\
        +(np.sin(np.pi*2*i*7*frequency/sample_rate)*0.05)\
        +(np.sin(np.pi*2*i*8*frequency/sample_rate)*0.05)
    """
    """
    signal_decimal = np.sin(np.pi*2*i*frequency/sample_rate)\
        +(np.sin(np.pi*2*i*3*frequency/sample_rate)/3)\
        +(np.sin(np.pi*2*i*5*frequency/sample_rate)/5)\
        +(np.sin(np.pi*2*i*7*frequency/sample_rate)/7)\
        +(np.sin(np.pi*2*i*9*frequency/sample_rate)/9)\
        +(np.sin(np.pi*2*i*11*frequency/sample_rate)/11)\
        +(np.sin(np.pi*2*i*13*frequency/sample_rate)/13)\
        +(np.sin(np.pi*2*i*15*frequency/sample_rate)/15)\
        +(np.sin(np.pi*2*i*17*frequency/sample_rate)/17)\
        +(np.sin(np.pi*2*i*19*frequency/sample_rate)/19)\
        +(np.sin(np.pi*2*i*21*frequency/sample_rate)/21)\
        +(np.sin(np.pi*2*i*23*frequency/sample_rate)/23)\
        +(np.sin(np.pi*2*i*25*frequency/sample_rate)/25)\
        +(np.sin(np.pi*2*i*27*frequency/sample_rate)/27)\
        +(np.sin(np.pi*2*i*29*frequency/sample_rate)/29)
        """
    """
    signal_decimal = np.sin(np.pi*2*i*frequency/sample_rate)\
        +(np.sin(np.pi*2*i*2*frequency/sample_rate)/2)\
        +(np.sin(np.pi*2*i*3*frequency/sample_rate)/3)\
        +(np.sin(np.pi*2*i*4*frequency/sample_rate)/4)\
        +(np.sin(np.pi*2*i*5*frequency/sample_rate)/5)\
        +(np.sin(np.pi*2*i*6*frequency/sample_rate)/6)\
        +(np.sin(np.pi*2*i*7*frequency/sample_rate)/7)\
        +(np.sin(np.pi*2*i*8*frequency/sample_rate)/8)\
        +(np.sin(np.pi*2*i*9*frequency/sample_rate)/9)\
        +(np.sin(np.pi*2*i*10*frequency/sample_rate)/10)\
        +(np.sin(np.pi*2*i*11*frequency/sample_rate)/11)\
        +(np.sin(np.pi*2*i*12*frequency/sample_rate)/12)\
        +(np.sin(np.pi*2*i*13*frequency/sample_rate)/13)\
        +(np.sin(np.pi*2*i*14*frequency/sample_rate)/14)\
        +(np.sin(np.pi*2*i*15*frequency/sample_rate)/15)
    """
    for n in range(1,20):
        amplitude_factor = 1
        frequency_factor = 1
        if n==1:
            signal_decimal = (np.sin(np.pi*2*i*amplitude_factor*frequency/sample_rate)/frequency_factor)
        else:
            signal_decimal = signal_decimal + (np.sin(np.pi*2*i*amplitude_factor*frequency/sample_rate)/frequency_factor)

    #lfo
    #signal_decimal = signal_decimal + np.sin(np.pi*2*i/sample_rate)
    x = max(np.max(signal_decimal),np.min(signal_decimal))

    signal_decimal = signal_decimal/x
    signal_decimal = signal_decimal*volume*0.1


    x = max(np.max(signal_decimal),np.min(signal_decimal))

    signal = list(map(int,(((signal_decimal)+1)* (2 ** 15 - 1)).tolist()))

    signal = array.array("H",signal)


    return signal


tones = [523.25,587.33,659.25,698.46,783.99,880.00,987.77]

tones.reverse()

i2s.play(mixer)

def play_tones(keys):
    for index in range(len(mixer.voice)):
        mixer.stop_voice(index)

    for index in range(len(keys)):
        tone = tones[keys[index]]


        sine_wave_sample  = audiocore.RawSample(generate_signal(tone), sample_rate=sample_rate)
        print("Adding " + str(tone)  + " to voice " + str(index))
        mixer.play(sine_wave_sample, voice=index, loop=True);




keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)
pressed_keys = set()

while True:
    event = keys.events.get()
    if event:
        key_number = event.key_number
        # A key transition occurred.
        if event.pressed:
            pressed_keys.add(key_number)

        if event.released:
            pressed_keys.remove(key_number)
        play_tones(list(pressed_keys))


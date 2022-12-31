import audiobusio
import audiocore
import board
import array
import time
import math
import keypad
import asyncio
import audiomixer


i2s  = audiobusio.I2SOut(bit_clock=board.GP10, word_select=board.GP11, data=board.GP9)

sample_rate = 32000
tone_volume = 1  # Increase or decrease this to adjust the volume of the tone.



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

def generate_sine(frequency,volume=1):
    length = int(sample_rate // frequency)
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int(
        (math.sin(math.pi * 2 * frequency * i / sample_rate) * volume + 1)
        #+(math.sin(math.pi * 2 * frequency * i*3 / sample_rate) * volume + 1)/3
        #+(math.sin(math.pi * 2 * frequency * i*5 / sample_rate) * volume + 1)/5
        #+(math.sin(math.pi * 2 * frequency * i*7 / sample_rate) * volume + 1)/7
        #+(math.sin(math.pi * 2 * frequency * i*9 / sample_rate) * volume + 1)/9
        #+ (math.sin(math.pi * 2 * frequency* 2 * i * 2 / sample_rate) * volume + 1) * 0.1 * 0.5
        #+ (math.sin(math.pi * 2 * frequency* 2 * i * 3 / sample_rate) * volume + 1) * 0.35 * 0.5
        #+ (math.sin(math.pi * 2 * frequency* 2 * i * 4 / sample_rate) * 0.05 * volume + 1)
        #+ (math.sin(math.pi * 2 * frequency* 2 * i * 5 / sample_rate) * 0.05 * volume + 1)
        #+ (math.sin(math.pi * 2 * frequency* 2 * i * 6 / sample_rate) * 0.05 * volume + 1)
        * (2 ** 15 - 1)
        )

    return sine_wave


tones = [523.25,587.33,659.25,698.46,783.99,880.00,987.77]

tones.reverse()

i2s.play(mixer)

def play_tones(keys):
    for index in range(len(mixer.voice)):
        mixer.stop_voice(index)
    for index in range(len(keys)):
        tone = tones[keys[index]]


        sine_wave_sample  = audiocore.RawSample(generate_sine(tone), sample_rate=sample_rate)
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


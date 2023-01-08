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

class SignalGenerator:
    def __init__(self, sample_rate=44000):
        self.sampleRate = sample_rate
        self.signalDict = {}

    def generateSignal(self,freq, type="sine",inverse=False,customFreqCoeff=(),customAmplCoeff=()):
        length = int(self.sampleRate // freq)

        i = np.linspace(0,length,length)
        
        if type == "sine":
            signal = i*np.pi*2*freq/self.sampleRate
            if inverse:
                signal = -signal
            fourierSeries = np.sin(signal)
        else:
            if type == "square":
                freqCoefficientsList = np.arange(10)
                amplCoefficientsList = np.arange(10)
                freqCoefficientsList = freqCoefficientsList*2+1
                amplCoefficientsList = 1.0/(amplCoefficientsList*2+1)
                
            elif type == "sawtooth":
                freqCoefficientsList = np.arange(10)+1
                amplCoefficientsList = np.arange(10)+1
                amplCoefficientsList = 1.0/(amplCoefficientsList*2)

            elif type == "triangle":
                freqCoefficientsList = np.arange(3)+1
                amplCoefficientsList = np.arange(3)+1
                freqCoefficientsList = freqCoefficientsList*2-1
                amplCoefficientsList = ((-1.0)**amplCoefficientsList)/((2*amplCoefficientsList-1)**2)

            elif type == "custom":
                freqCoefficientsList = np.array(customFreqCoeff)
                amplCoefficientsList = np.array(customAmplCoeff)

            
            if inverse:
                amplCoefficientsList = -amplCoefficientsList

            freqCoefficients = np.array(freqCoefficientsList).reshape((len(freqCoefficientsList),1))
            amplCoefficients = np.array(amplCoefficientsList).reshape((len(amplCoefficientsList),1))

            signal = (freq*2*np.pi/self.sampleRate)*(freqCoefficients * i)

            fourierSeriesMatrix = np.sin(signal)*amplCoefficients 
            fourierSeries = np.sum(fourierSeriesMatrix, axis=0)
            
        return fourierSeries

    def getSignal(self,freq, type="sine",inverse=False,customFreqCoeff=(),customAmplCoeff=()):
        if (freq,type,inverse,customFreqCoeff,customAmplCoeff) not in self.signalDict:
            self.signalDict[(freq,type,inverse,customFreqCoeff,customAmplCoeff)] = self.generateSignal(freq,type,inverse,customFreqCoeff,customAmplCoeff)
        return self.signalDict[(freq,type,inverse,customFreqCoeff,customAmplCoeff)]
    
    def deleteSignal(self,freq, type="sine",inverse=False,custom_freq_coeff=(),custom_ampl_coeff=()):
        del  self.signalDict[(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)]

    def getSignalDict(self):
        return self.signalDict

    def getSampleRate(self):
        return self.sampleRate


def getFrequency(midiNumber):
    return round(440*2**((midiNumber-69)/12),2);

def getMidiNumberByName(octave, noteName):
    noteNames = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    return (octave+1)*12 + noteNames.index(noteName.upper())    


def getMidiNumberByNumber(octave, noteNumber):
    return (octave+1)*12 + noteNumber  



KEY_PINS = (
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7
)


sg = SignalGenerator()
i2s  = audiobusio.I2SOut(bit_clock=board.GP10, word_select=board.GP11, data=board.GP9)
mixer = audiomixer.Mixer(voice_count=8, sample_rate=sg.getSampleRate(), channel_count=1,
                         bits_per_sample=16, samples_signed=False)
i2s.play(mixer)


def findAvailableVoice(mixer):
    retv = -1
    for index in range(len(mixer.voice)):
        if not mixer.voice[index].playing:
            retv = index
            break
    return retv
            

voiceMap = {}

def stopKey(key):
    if key in voiceMap:
        voiceIdx = voiceMap[key]
        mixer.stop_voice(voiceIdx)
        print("Stopping " + str(key) + " on voice " +str(voiceIdx))

def playKey(key):
    frequency = getFrequency(getMidiNumberByNumber(4,key))
    voiceIdx = findAvailableVoice(mixer) 
    print("Playing " + str(key)+ " freq: " + str(frequency) + " on Voice:" + str(voiceIdx))
    if voiceIdx > -1:
        voiceMap[key] = voiceIdx
        signal_decimal = (sg.getSignal(frequency,type="sawtooth",inverse=True)*0.4 + 1) * (2 ** 15 - 1)
        signal_decimal = np.array(signal_decimal, dtype=np.uint16)
        signal = array.array('H',signal_decimal)
        signalAc = audiocore.RawSample(signal, sample_rate=sg.getSampleRate())
        mixer.play(signalAc, voice=voiceIdx, loop=True)


keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)
pressed_keys = set()

while True:
    event = keys.events.get()
    keyTranslation = [0,2,4,5,7,9,11]
    if event:
        key_number = keyTranslation[6-event.key_number]
        # A key transition occurred.
        if event.pressed:
            playKey(key_number)

        if event.released:
            stopKey(key_number)        


import time
import math
import sys

if sys.implementation.name == 'circuitpython':
    from ulab import numpy as np
    def timeit(s, f, n=100):
        t0 = time.monotonic_ns()
        for _ in range(n):
            x = f()
        t1 = time.monotonic_ns()
        r = (t1 - t0) * 1e-6 / n
        print("%-30s : %8.3fms [result=%f]" % (s, r, sum(x)))

else:
    import numpy as np
    import timeit
    



sample_rate = 44000

def generate_signal_math(frequency):
    length = int(sample_rate // frequency)
    sine_wave = [0.0]*length
    for i in range(length):
        sine_wave[i] = math.sin(math.pi*2*i*frequency/sample_rate)\
        +math.sin(math.pi*2*i*3*frequency/sample_rate)/3\
        +math.sin(math.pi*2*i*5*frequency/sample_rate)/5\
        +math.sin(math.pi*2*i*7*frequency/sample_rate)/7\
        +math.sin(math.pi*2*i*9*frequency/sample_rate)/9\
        +math.sin(math.pi*2*i*11*frequency/sample_rate)/11\
        +math.sin(math.pi*2*i*13*frequency/sample_rate)/13\
        +math.sin(math.pi*2*i*15*frequency/sample_rate)/15\
        +math.sin(math.pi*2*i*17*frequency/sample_rate)/17\
        +math.sin(math.pi*2*i*19*frequency/sample_rate)/19

    return sine_wave

def generate_signal(frequency,volume=1):
    length = int(sample_rate  *4 // frequency)
    i = np.linspace(0,length,length)
    signal_decimal = np.sin(np.pi*2*i*frequency/sample_rate)\
        +np.sin(np.pi*2*i*3*frequency/sample_rate)/3\
        +np.sin(np.pi*2*i*5*frequency/sample_rate)/5\
        +np.sin(np.pi*2*i*7*frequency/sample_rate)/7\
        +np.sin(np.pi*2*i*9*frequency/sample_rate)/9\
        +np.sin(np.pi*2*i*11*frequency/sample_rate)/11\
        +np.sin(np.pi*2*i*13*frequency/sample_rate)/13\
        +np.sin(np.pi*2*i*15*frequency/sample_rate)/15\
        +np.sin(np.pi*2*i*17*frequency/sample_rate)/17\
        +np.sin(np.pi*2*i*19*frequency/sample_rate)/19
            
    return signal_decimal

def generate_signal_betterly(freq, type="sine",inverse=False,custom_freq_coeff=[],custom_ampl_coeff=[]):
    length = int(sample_rate // freq)

    i = np.linspace(0,length,length)
    if type == "sine":
        signal = i*np.pi*2*freq/sample_rate
        if inverse:
            signal = -signal
        fourier_series = np.sin(signal)
    else:
        if type == "square":
            freq_coefficients_list = np.arange(10)
            ampl_coefficients_list = np.arange(10)
            freq_coefficients_list = freq_coefficients_list*2+1
            ampl_coefficients_list = 1.0/(ampl_coefficients_list*2+1)
            
        elif type == "sawtooth":
            freq_coefficients_list = np.arange(10)+1
            ampl_coefficients_list = np.arange(10)+1
            ampl_coefficients_list = 1.0/(ampl_coefficients_list*2)

        elif type == "triangle":
            freq_coefficients_list = np.arange(3)+1
            ampl_coefficients_list = np.arange(3)+1
            freq_coefficients_list = freq_coefficients_list*2-1
            ampl_coefficients_list = ((-1.0)**ampl_coefficients_list)/((2*ampl_coefficients_list-1)**2)

        elif type == "custom":
            freq_coefficients_list = np.array(custom_freq_coeff)
            ampl_coefficients_list = np.array(custom_ampl_coeff)

        
        if inverse:
            ampl_coefficients_list = -ampl_coefficients_list

        freq_coefficients = np.array(freq_coefficients_list).reshape((len(freq_coefficients_list),1))
        ampl_coefficients = np.array(ampl_coefficients_list).reshape((len(ampl_coefficients_list),1))
        
        signal = (freq*2*np.pi/sample_rate)*(freq_coefficients * i)
        
        fourier_series_matrix = np.sin(signal)*ampl_coefficients 
        
        fourier_series = np.sum(fourier_series_matrix, axis=0)
        
    return fourier_series
    

class SignalGenerator:
    def __init__(self, sample_rate=44000):
        self.sample_rate = sample_rate
        self.signal_dict = {}

    def generate_signal(self,freq, type="sine",inverse=False,custom_freq_coeff=(),custom_ampl_coeff=()):
        length = int(self.sample_rate // freq)

        i = np.linspace(0,length,length)
        
        if type == "sine":
            signal = i*np.pi*2*freq/self.sample_rate
            if inverse:
                signal = -signal
            fourier_series = np.sin(signal)
        else:
            if type == "square":
                freq_coefficients_list = np.arange(10)
                ampl_coefficients_list = np.arange(10)
                freq_coefficients_list = freq_coefficients_list*2+1
                ampl_coefficients_list = 1.0/(ampl_coefficients_list*2+1)
                
            elif type == "sawtooth":
                freq_coefficients_list = np.arange(10)+1
                ampl_coefficients_list = np.arange(10)+1
                ampl_coefficients_list = 1.0/(ampl_coefficients_list*2)

            elif type == "triangle":
                freq_coefficients_list = np.arange(3)+1
                ampl_coefficients_list = np.arange(3)+1
                freq_coefficients_list = freq_coefficients_list*2-1
                ampl_coefficients_list = ((-1.0)**ampl_coefficients_list)/((2*ampl_coefficients_list-1)**2)

            elif type == "custom":
                freq_coefficients_list = np.array(custom_freq_coeff)
                ampl_coefficients_list = np.array(custom_ampl_coeff)

            
            if inverse:
                ampl_coefficients_list = -ampl_coefficients_list

            freq_coefficients = np.array(freq_coefficients_list).reshape((len(freq_coefficients_list),1))
            ampl_coefficients = np.array(ampl_coefficients_list).reshape((len(ampl_coefficients_list),1))

            signal = (freq*2*np.pi/self.sample_rate)*(freq_coefficients * i)

            fourier_series_matrix = np.sin(signal)*ampl_coefficients 
            fourier_series = np.sum(fourier_series_matrix, axis=0)
            
        return fourier_series

    def get_signal(self,freq, type="sine",inverse=False,custom_freq_coeff=(),custom_ampl_coeff=()):
        if (freq,type,inverse,custom_freq_coeff,custom_ampl_coeff) not in self.signal_dict:
            self.signal_dict[(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)] = self.generate_signal(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)
        return self.signal_dict[(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)]


sg = SignalGenerator()


def main():
    number_of_times = 10000
    result = timeit.Timer(lambda:sg.get_signal(440,type="square"))
    print('SignalGenerator: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))    

def circuitPythonMain():
    number_of_times = 10000 
    timeit("SignalGenerator", lambda: sg.get_signal(440,type="square"))


if __name__ == "__main__":
    if sys.implementation.name == 'circuitpython':
        circuitPythonMain()
    else:
        main()

    
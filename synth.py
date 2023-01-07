import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time


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
            print('generated signal')
            self.signal_dict[(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)] = self.generate_signal(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)
        return self.signal_dict[(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)]



sg = SignalGenerator();


sd.play(sg.get_signal(550), sg.sample_rate,loop=True)
time.sleep(1)
sd.play(sg.get_signal(550,type="square"), sg.sample_rate,loop=True)
time.sleep(1)

sd.play(sg.get_signal(550,type="custom",custom_ampl_coeff=(1,0.1,0.33,0.05,0.05,0.05,0,0.02,0,0.01),custom_freq_coeff=range(1,11)), sg.sample_rate,loop=True)
time.sleep(1)

sd.play(sg.get_signal(550), sg.sample_rate,loop=True)
time.sleep(1)


if False:
    fig, axs = plt.subplots(3,2)
    axs[0, 0].plot(generate_signal_betterly(440))     
    axs[0, 0].set_title('Sine')
    axs[0, 1].plot(generate_signal_betterly(440,inverse=True))       
    axs[0, 1].set_title('Inverted Sine')
    axs[1, 0].plot(generate_signal_betterly(440,type="square"))   
    axs[1, 0].set_title('Square Wave')
    axs[1, 1].plot(generate_signal_betterly(440,type="sawtooth"))   
    axs[1, 1].set_title('Sawtooth Wave')
    axs[2, 0].plot(generate_signal_betterly(440,type="triangle"))   
    axs[2, 0].set_title('Triangle Wave')
    axs[2, 1].plot(generate_signal_betterly(440,type="custom",custom_ampl_coeff=[1,0.1,0.33,0.05,0.05,0.05,0,0.02,0,0.01],custom_freq_coeff=range(1,11)))
    axs[2, 1].set_title('Custom Wave(Piano approximation)')

    #axs[3, 0].plot(resample(generate_signal_betterly(440,type="custom",custom_ampl_coeff=[1,0.1,0.33,0.05,0.05,0.05,0,0.02,0,0.01],custom_freq_coeff=range(1,11)),440,550))
    #axs[3, 0].plot(generate_signal_betterly(550,type="custom",custom_ampl_coeff=[1,0.1,0.33,0.05,0.05,0.05,0,0.02,0,0.01],custom_freq_coeff=range(1,11)))
    #axs[3, 0].set_title('Resampling')

    #axs[3, 1].plot(resample(generate_signal_betterly(440,type="custom",custom_ampl_coeff=[1,0.1,0.33,0.05,0.05,0.05,0,0.02,0,0.01],custom_freq_coeff=range(1,11)),440,2000))
    #axs[3, 1].plot(generate_signal_betterly(2000,type="custom",custom_ampl_coeff=[1,0.1,0.33,0.05,0.05,0.05,0,0.02,0,0.01],custom_freq_coeff=range(1,11)))
    #axs[3, 1].set_title('Harder Resampling')

    plt.show()

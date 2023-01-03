import matplotlib.pyplot as plt
import numpy as np
import timeit


sample_rate = 44000

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

def generate_signal_betterly(freq):
    length = int(sample_rate *4 // freq)

    i = np.linspace(0,length,length)
    
    freq_coefficients_list = [1,3,5,7,9,11,13,15,17,19]
    ampl_coefficients_list = [1,3,5,7,9,11,13,15,17,19]

    
    freq_coefficients = np.array(freq_coefficients_list).reshape((10,1))
    ampl_coefficients = 1/np.array(ampl_coefficients_list).reshape((10,1))

    signal = (freq_coefficients * i).flatten()*np.pi*2*freq/sample_rate;

    sine = np.sin(signal).reshape((len(freq_coefficients_list),length))*ampl_coefficients
    sine = sine.sum(axis=0)
    
    return sine



def resample(signal,original,new):
    
    length = int(sample_rate // original)*4
    choice = np.round(np.linspace(1,len(signal)-1,num=int(original*length/new))).astype(int)
    print(choice)
    return signal[choice]

number_of_times = 10000
result = timeit.Timer(lambda:generate_signal(440))
print('Old function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))


number_of_times = 10000
result = timeit.Timer(lambda:generate_signal_betterly(440))
print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))


plt.plot(generate_signal_betterly(440))       # Plot the sine of each x point
plt.plot(generate_signal(440))       # Plot the sine of each x point
plt.show()

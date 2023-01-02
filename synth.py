import matplotlib.pyplot as plt
import numpy as np


sample_rate = 44000

def generate_signal(frequency,volume=1):
    length = int(sample_rate // frequency)
    i = np.linspace(0,length,length)
    signal_decimal = np.sin(np.pi*2*i*frequency/sample_rate)\
        +np.sin(np.pi*2*i*3*frequency/sample_rate)/3\
        +np.sin(np.pi*2*i*5*frequency/sample_rate)/5\
        +np.sin(np.pi*2*i*7*frequency/sample_rate)/7\
        +np.sin(np.pi*2*i*9*frequency/sample_rate)/9\
        +np.sin(np.pi*2*i*11*frequency/sample_rate)/11\
        +np.sin(np.pi*2*i*13*frequency/sample_rate)/13\
        +np.sin(np.pi*2*i*15*frequency/sample_rate)/15
        
    signal = ((signal_decimal+1)* (2 ** 15 - 1)).astype(int)
    
    return i,signal


def resample(signal,original,new):
    
    length = int(sample_rate // original)*4
    choice = np.round(np.linspace(1,len(signal)-1,num=int(original*length/new))).astype(int)
    print(choice)
    return signal[choice]

x,sine = generate_signal(440)
plt.plot(sine)       # Plot the sine of each x point


plt.plot(resample(sine,440,1600))       # Plot the sine of each x point

x,sine = generate_signal(1600)
plt.plot(sine)       # Plot the sine of each x point
plt.show()                   # Display the plot
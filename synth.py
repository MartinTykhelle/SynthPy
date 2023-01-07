import matplotlib.pyplot as plt
import numpy as np
import timeit
import cProfile


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

def generate_signal_betterly(freq, type="sine",inverse=False,custom_freq_coeff=(),custom_ampl_coeff=()):
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


signal_dict = {}
def get_signal(freq, type="sine",inverse=False,custom_freq_coeff=(),custom_ampl_coeff=()):
    
    if (freq,type,inverse,custom_freq_coeff,custom_ampl_coeff) not in signal_dict:
        signal_dict[(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)] = generate_signal_betterly(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)
    return signal_dict[(freq,type,inverse,custom_freq_coeff,custom_ampl_coeff)]



def resample(signal,original,new):
    
    choice = np.round(np.linspace(1,len(signal)-1,num=int(original*len(signal)/new))).astype(int)
    print(choice)
    return signal[choice]

if False:
    number_of_times = 10000
    result = timeit.Timer(lambda:generate_signal(440))
    print('Old function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))

if False:
    number_of_times = 10000
    result = timeit.Timer(lambda:generate_signal_betterly(440))
    print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))
    a = [
        {'freq':440,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':441,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':442,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':443,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':444,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':445,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':446,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':447,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':448,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':449,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':450,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':451,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
        {'freq':452 ,type:"sine",'inverse':False,'custom_freq_coeff':[],'custom_ampl_coeff':[]},
    ]
    
    result = timeit.Timer(lambda:next(item for item in a if item["freq"] == 450))
    print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))

if False:
    number_of_times = 10000
    result = timeit.Timer(lambda:generate_signal_betterly(440))
    print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))
    a = {}
    
    a[(440,'sine',False,(1,2,3),(1,2,3))] = 1
    a[(440,'saw',False)] = 2
    a[(440,'square',False)] = 3
    a[(440,'triangle',False)] = 4
    
    result = timeit.Timer(lambda:a[(440,'square',False)])
    print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))


if True:
    number_of_times = 10000
    result = timeit.Timer(lambda:generate_signal_betterly(440))
    print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))
    result = timeit.Timer(lambda:get_signal(440))
    print('Lookup function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))
    result = timeit.Timer(lambda:generate_signal_betterly(440,'square'))
    print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))
    result = timeit.Timer(lambda:get_signal(440,'square'))
    print('Lookup function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))
    result = timeit.Timer(lambda:generate_signal_betterly(880,'custom',custom_ampl_coeff=(1/1,1/2,1/2),custom_freq_coeff=(2,4,8)))
    print('New function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))
    result = timeit.Timer(lambda:get_signal(880,'custom',custom_ampl_coeff=(2,4),custom_freq_coeff=(2,4)))
    print('Lookup function: %fns' % (result.timeit(number=number_of_times)*1000*1000/10000))

plt.style.use('dark_background')

plt.plot(get_signal(440))     
plt.plot(get_signal(440,'square'))     
plt.plot(get_signal(880))       
plt.plot(get_signal(880,'custom',custom_ampl_coeff=(1/2,1/4,1/8),custom_freq_coeff=(2,4,8)))     
plt.show()

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

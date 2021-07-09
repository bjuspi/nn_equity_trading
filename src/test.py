# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 00:28:00 2021

@author: Johanes Suhardjo
"""

from numpy import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, TimeDistributed

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi']=300 # highres display

#import time
#from IPython.display import clear_output
rng = random.RandomState(23455)

input_data = "final_input.txt"
answer_data = "correct_ans_updown2.txt"
output_figure = "updown-5days-bs30-ep2.5k-time.png"
rnn_folder = "updown-5days-bs30-ep2.5k-time"
n_input_data = 21
kept_for_exam = 500 #number of data that we keep for examination so that it will not be trained on this 

def init_network():
    global rnn, timesteps, n_input_data
    rnn = Sequential()
    rnn.add(LSTM(1500, batch_input_shape=(None, timesteps, n_input_data), return_sequences=True))
    rnn.add(LSTM(1000, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=True))
#    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(TimeDistributed(Dense(2, activation='softmax')))
    rnn.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
    
def make_batch(batchsize, timesteps):
    """
    Take as argument: batchsize, timesteps. 
    This function will generate randomly the batches from the available data
    """

    global n_input_data, kept_for_exam
    all_y_ans = loadtxt(answer_data, usecols=0, unpack=True)
    length = shape(all_y_ans)[0]
    
    all_y_in = zeros([length, n_input_data])
    for i in range(n_input_data):
        all_y_in[:,i] = loadtxt(input_data, usecols=i, unpack=True)

    #Generate random samples with timesteps length.
    start_time = random.randint(0,length-kept_for_exam-timesteps+1, size =batchsize)
    yin = zeros([batchsize, timesteps, n_input_data])
    yans = zeros([batchsize, timesteps], dtype=int)


    for i in range(batchsize):
        yin[i,:,:] = all_y_in[start_time[i]:(start_time[i]+timesteps), :]
        yans[i, :] = all_y_ans[start_time[i]:(start_time[i]+timesteps)]
        
    #Normalizing the price and the volume wrt the zeroth price and volume in the time series
    for j in range(batchsize):
        yin[j, :, 0] = yin[j, :, 0]/yin[j,0,0]
        yin[j, :, 1] = yin[j, :, 1]/yin[j,0,1]
    
    #Reshaping yans for categorical cross entropy
    yans_new = zeros([batchsize, timesteps, 2])

    yans_new[:, :, 0] = (yans[:, :]==0)*1
    yans_new[:, :, 1] = (yans[:, :]==1)*1
    
    #New Addition:
    #y_ans = zeros([batchsize, 2])
    #y_ans[:,:] = yans_new[:,timesteps-1,:]
    return [yin, yans_new]
    

batchsize = 30
timesteps = 20
init_network()

epochs = 2500
errors = zeros(epochs)
acc = zeros(epochs)
for i in range(epochs):
#    if(i%10==0):
#        print(100*i/epochs)
        
    yin, yout = make_batch(batchsize, timesteps)
    temp = rnn.train_on_batch(yin, yout)
    errors[i] = temp[0]
    acc[i] = temp[1]
#    if(i%10==0):
#        im, (ax0, ax1) = plt.subplots(ncols=2)
#        ax0.plot(errors)
#        ax1.plot(acc)
#        plt.show()
#        clear_output(wait=True)
    
im, (ax0, ax1) = plt.subplots(ncols=2)
ax0.plot(errors)
ax1.plot(acc)
plt.savefig(output_figure)

rnn.save(rnn_folder)

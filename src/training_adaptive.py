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
import os
matplotlib.rcParams['figure.dpi']=300 # highres display

#import time
#from IPython.display import clear_output
rng = random.RandomState(12245)

input_data = "final_input.txt"
answer_data = "correct_ans_updown_000p.txt"
exam_y_input_txt = "exam_input.txt"
exam_y_ans_txt = "exam_answer_000p.txt"
output_figure = "updown-5days-bs30-epadap-time-000p.png"
rnn_folder = "updown-5days-bs30-epadap-time-000p"
exam_folder =  "exam-" + rnn_folder #shouldn't have existed
n_input_data = 21
kept_for_exam = 500 #number of data that we keep for examination so that it will not be trained on this 

os.mkdir(exam_folder)

def init_network():
    global rnn, timesteps, n_input_data
    rnn = Sequential()
    rnn.add(LSTM(1500, batch_input_shape=(None, timesteps, n_input_data), return_sequences=True))
    rnn.add(LSTM(1000, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(LSTM(800, return_sequences=False))
#    rnn.add(LSTM(800, return_sequences=True))
    rnn.add(Dense(2, activation='softmax'))
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
    y_ans = zeros([batchsize, 2])
    y_ans[:,:] = yans_new[:,timesteps-1,:]
    return [yin, y_ans]
    

batchsize = 30
timesteps = 20
init_network()

accuracy = 0
errors = []
acc = []
i=0
while(accuracy<0.93):
#    if(i%10==0):
#        print(100*i/epochs)
        
    yin, yout = make_batch(batchsize, timesteps)
    temp = rnn.train_on_batch(yin, yout)
    errors.append(temp[0])
    acc.append(temp[1])
    i+=1
    accuracy = temp[1]
#    if(i%10==0):
#        im, (ax0, ax1) = plt.subplots(ncols=2)
#        ax0.plot(errors)
#        ax1.plot(acc)
#        plt.show()
#        clear_output(wait=True)

#Adaptive + 1000 more epochs
for j in range(1000):
    yin, yout = make_batch(batchsize, timesteps)
    temp = rnn.train_on_batch(yin, yout)
    errors.append(temp[0])
    acc.append(temp[1])
    
errors = array(errors)
acc = array(acc)
    
im, (ax0, ax1) = plt.subplots(ncols=2)
ax0.plot(errors)
ax1.plot(acc)
plt.savefig(output_figure)

rnn.save(rnn_folder)

#input the testing answer
y_ans = loadtxt(exam_y_ans_txt, usecols = 0, unpack=True)
exam_number = shape(y_ans)[0]

#input the testing input
y_input = zeros([exam_number+timesteps-1, n_input_data])
for i in range(n_input_data):
    y_input[:, i] = loadtxt(exam_y_input_txt, usecols=i, unpack=True)
    
    
length = shape(y_input)[0] #NOTE THAT THIS IS NOT 500
prediction = []
for i in range(length-timesteps+1):
    current_y_input = zeros([1, timesteps, n_input_data])
    current_y_input[0,:,:] = y_input[i:i+timesteps, :]
    
    #Normalizing according to the simulation
    current_y_input[0,:,0]= current_y_input[0,:,0]/current_y_input[0,0,0]
    current_y_input[0,:,1] = current_y_input[0,:,1]/current_y_input[0,0,1]

    temp = (rnn.predict(current_y_input)[0][1]>0.5)*1 #IF TRUE IT IS PREDICTING THAT THE PRICE IS GOING UP
    prediction.append(temp)
    
prediction = array(prediction)
savetxt(exam_folder+"/prediction.txt", prediction)

accuracy_of_prediction=zeros(exam_number)
accuracy_of_prediction[:] = (y_ans[:]==prediction[:])*1
pred_acc = sum(accuracy_of_prediction)/exam_number

#Cutting the input to only the last 500 and store into price array
price = zeros(exam_number)
price[:] = y_input[-exam_number:, 0] #Note this is not the actual price, but its ok.and

output_exam = open(exam_folder + "/result.txt", "w+")
output_exam.write("Accuracy ="+ str(pred_acc) + "\n" +"\n")

for j in range(5): 
    have_share = False
    money = 10000
    shares = 0
    i=j
    lastbuy=0
    Gain = []
    Loss = []
    while(i < exam_number):
        if(prediction[i]==1):
            if(have_share==False):
                have_share=True
                shares += money/price[i]
                lastbuy = money
                money = 0
            
        if(prediction[i]==0):
            if(have_share==True):
                have_share = False
                money += shares*price[i]
                shares = 0
                if(money>lastbuy): Gain.append(money-lastbuy)
                elif(money<lastbuy): Loss.append(lastbuy-money)

        i+=5
        
    output_exam.write("\n######### Day "+ str(j) + " #########\n")
    output_exam.write("Ending Money: " + str(money+shares*price[499]) +"\n")
    output_exam.write("Gain: "+ str(Gain) +"\n")
    output_exam.write("Loss: "+ str(Loss) +"\n")
    
output_exam.close()
    
        
    


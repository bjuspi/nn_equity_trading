# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 23:23:28 2021

@author: Johanes Suhardjo
"""

import numpy as np

input_txt = "FB/final_input.txt"
answer_txt = "FB/correct_ans_updown2.txt"
output_txt = "FB/exam_input.txt"
output_txt2 = "FB/exam_answer.txt"
n_input_data = 21
exam_number = 500
timesteps=20

all_y_ans = np.loadtxt(answer_txt, usecols=0, unpack=True)
length = np.shape(all_y_ans)[0]
all_y_input = np.zeros([length, n_input_data])
for i in range(n_input_data):
    all_y_input[:, i] = np.loadtxt(input_txt, usecols=i, unpack=True)
    
y_exam = np.zeros([exam_number+timesteps-1, n_input_data])
y_exam[:, :] = all_y_input[-(exam_number+timesteps-1):, :]

np.savetxt(output_txt, y_exam)

exam_answer = np.zeros(exam_number)
exam_answer[:] = all_y_ans[-exam_number:]

np.savetxt(output_txt2, exam_answer)
    
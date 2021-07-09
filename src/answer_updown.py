# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 22:55:17 2021

@author: Johanes Suhardjo
"""

import numpy as np

input_txt = "FB/price.txt"
output_txt = "FB/correct_ans_updown3.txt"
daysforward=1
price_gap = 0

price = np.loadtxt(input_txt, usecols=1, unpack=True)
ans = np.zeros(np.shape(price)[0], dtype=int)
length = np.shape(price)[0]

for i in range(length-daysforward):
    if(price[i]+price_gap < price[i+daysforward]):
        ans[i]=1

np.savetxt(output_txt, ans)
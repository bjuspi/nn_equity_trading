import os
import numpy as np

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
datadir = os.path.join(rootdir, "data")
interimdatadir = os.path.join(datadir, "interim")

#FIRST COLUMN SHOULD BE THE NUMBER OF DAY, SCND THE OPENING PRICE, SIXTH THE VOLUME AND SO ON
# price_date_txt = "FB/price.txt" 
price_date_txt = os.path.join(os.path.join(interimdatadir, "FB"), "price.txt")
#THE COUNT STARTS FROM VOLUME
Ncolumns_price = 7 
#FIRST COLUMN IS FINANCIAL RELEASE DATE, THE SECOND SHOULD BE FINANCIAL STATEMENT DATE
# fs_txt = "FB/fs.txt" 
fs_txt = os.path.join(os.path.join(interimdatadir, "FB"), "fs.txt")
#UNLIKE ABOVE THIS INCLUDES THE DATES, SO MINIMUM IS 2
Ncolumns = 15 
# save_txt = "FB/final_input.txt"
save_txt = os.path.join(os.path.join(interimdatadir, "FB"), "final_input.txt")

price_date = np.loadtxt(price_date_txt, usecols=0, unpack=True)
fs_release_date, fs_date = np.loadtxt(fs_txt, usecols=(0,1), unpack=True)

length = np.shape(price_date)[0]
fs_length = np.shape(fs_release_date)[0]

fs = np.zeros([Ncolumns-2,fs_length])
for j in range(Ncolumns-2):
    fs[j,:] = np.loadtxt(fs_txt, usecols = j+2, unpack=True)


ans = np.zeros([length])
fs_ans = np.zeros([Ncolumns-2, length])

for i in range(fs_length-1):
    cond = (price_date > fs_release_date[i]) & (price_date <= fs_release_date[i+1])
    ans[cond] = price_date[cond] - fs_date[i] 
    
    temp = np.transpose(fs_ans[:,cond])
    temp += fs[:,i]
    fs_ans[:,cond] = np.transpose(temp)
        
i = fs_length-1
cond = (price_date>fs_release_date[i])
ans[cond] = price_date[cond] - fs_date[i]
temp = np.transpose(fs_ans[:,cond])
temp += fs[:,i]
fs_ans[:,cond] = np.transpose(temp)
#fs_ans[:, cond] += fs[:,i]

#WRITING THE OUTPUT, NOT SO ESSENTIAL AND JUST FOR CONVENIENCE
Ntotal = Ncolumns_price + Ncolumns - 1
final = np.zeros([Ntotal, length])
final[0,:] = np.loadtxt(price_date_txt, usecols=1, unpack=True)
for i in range(Ncolumns_price):
    final[i+1,:] = np.loadtxt(price_date_txt, usecols=5+i, unpack=True)
#final[2,:] = np.copy(ans)

for i in range(Ncolumns_price+1, Ntotal):
    final[i,:] = fs_ans[i-Ncolumns_price-1,:]

#final[Ntotal-1, :] = final[Ntotal-1,:]/final[0,:]*100
#final[Ntotal-2, :] = final[Ntotal-2,:]/final[0,:]*100    
final[0, :] = final[0, :]/final[0,0]*100
final[1, :] = final[1, :]/final[1,0]*100
np.savetxt(save_txt, final.transpose())
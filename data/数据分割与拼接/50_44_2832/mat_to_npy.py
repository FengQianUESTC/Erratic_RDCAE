import os
import random
import imageio
import numpy as np
import torch
import matplotlib.pyplot as plt
import h5py
import scipy.io as sio


###############输入转换##############
#h5py打开mat文件
mat = h5py.File('seis_dn_chongdie_50_44_2832_12_29.mat')
print(mat.keys())
data = mat['data']
print(data.shape)

data = np.reshape(data, (-1, 1,44, 50))
print(data.shape)
np.save('seis_dn_chongdie_50_44_2832.npy',data)
data = np.load('seis_dn_chongdie_50_44_2832.npy')
print(data.shape)
fig = plt.figure(1)
plt.imshow(data[760].squeeze(),aspect='auto' )
plt.show()
import h5py as h5py
import numpy as np
import matplotlib.pyplot as plt

dataping=h5py.File('seis_dn_chongdie_50_44_272_12_29.mat')
data=dataping['/data']
# zhongjian=permute(data, [1, 3, 2])
zhongjian=np.zeros((272,1,44,50), dtype=float, order='C')

for i in range(272):
    zhongjian[i,0,:,:] = data[i,:,:].squeeze()

np.save("seis_dn_chongdie272_1_44_50.npy",zhongjian)
plt.imshow(zhongjian[39,0,:,:].squeeze(), aspect='auto')
plt.savefig('seis_dn_chongdie_50_44_272_12_29.png')
plt.show()





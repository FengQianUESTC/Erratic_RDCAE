# from model.unet_model import UNet
# from model.autoencoder import autoencoder
from model.autoencoder_seisdata import autoencoder_seisdata,TVLoss,total_variation
from torch import optim
import torch.nn as nn
import torch
from torch.utils.data import Dataset,DataLoader,TensorDataset
import math
import os
import torch.nn.functional as F
from torchvision import datasets, transforms
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
# os.environ["CUDA_VISIBLE_DEVICES"]='1'

def welsch_loss(labels, logits, C):
    z=torch.sub(input=labels,alpha=1,other=logits)
    z2 = torch.pow(z,2)
    c2 = 2.0 * math.pow(C, 2)  # 2*c的平方
    res=1-torch.exp(-1*(z2/c2))
    # print(res.shape)
    return res
#

def train_net(net, device, train_loader, epochs=200, lr=1e-3):
    # 加载训练集

    # 定义RMSprop算法
    # optimizer = optim.RMSprop(net.parameters(), lr=lr, weight_decay=1e-8, momentum=0.9)
    optimizer = optim.Adam(net.parameters(),eps=1e-9)
    # 定义Loss算法
    # addition = TVLoss()
    # best_loss统计，初始化为正无穷
    best_loss = float('inf')
    # 训练epochs次
    loss_val_vector = []
    C=2
    for epoch in range(epochs):
        # 训练模式
        net.train()
        # 按照batch_size开始训练
        total_welsch = 0
        total_Tv = 0
        total_loss = 0
        print(C)
        for image, label in train_loader:
            optimizer.zero_grad()
            # 将数据拷贝到device中

            image = image.to(device=device, dtype=torch.float)
            label = label.to(device=device, dtype=torch.float)

            pred = net(image)
            # 计算loss

            Tv = 25e-4 * total_variation(pred)
            # Tv = 1e-5*total_variation(pred)
            welsch = 1e2*torch.mean(welsch_loss(label, pred, C=0.1))
            loss = 1e2*torch.mean(welsch_loss(label,pred,C=0.1))+Tv

            total_Tv +=Tv.item()
            total_welsch +=welsch.item()
            total_loss += loss.item()

            # 更新参数
            loss.backward()
            optimizer.step()

        print('epoch:',epoch)
        print('total_Loss/train', total_loss)
        print('total_welsch/train', total_welsch)
        print('total_Tv/train', total_Tv)
        loss_val_vector.append(total_loss)
    torch.save(net.state_dict(), 'best_unetmodel_2832tv.pth')
    if epoch == (epochs - 1):

        lolength = len(loss_val_vector)  # 不能一样
        minvalue = min(loss_val_vector)
        maxvalue = max(loss_val_vector)
        index = range(0, lolength)
        # index={1,2,3,4,5,6,7,8,9,10}
        plt.figure(1)
        plt.plot(index, loss_val_vector, linewidth=4)
        plt.title("loss_val_vector1 趋势曲线", fontsize=14)
        plt.xlabel("迭代次数", fontsize=14)
        plt.ylabel("loss—value", fontsize=14)
        plt.tick_params(axis='x', labelsize=10)
        plt.axis([-1, lolength, minvalue - 0.00001, maxvalue + 0.00001])
        plt.savefig('diedai.png')
        plt.show()



if __name__ == "__main__":

    batch_size = 5
    data = np.load('seis_dn_chongdie_50_44_2832.npy')

    data = torch.from_numpy(data)
    length = data.shape[0]
    train_dataset = TensorDataset(data, data)
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=batch_size,
                                               shuffle=True)

    # 选择设备，有cuda用cuda，没有就用cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # device = 'cpu'
    print(device)

    net = autoencoder_seisdata()
    # 将网络拷贝到deivce中
    net.to(device=device)
    # train_net(net, device, train_loader)

    #测试
    net.load_state_dict(torch.load('best_unetmodel_2832tv.pth', map_location=device))
    net.eval()
    data_test = np.load('seis_dn_chongdie272_1_44_50.npy')
    data_test = torch.from_numpy(data_test)

    data_test = data_test.to(device=device, dtype=torch.float)
    pred = net(data_test)

    inputs = data_test.detach().cpu().numpy()
    print(inputs.shape)
    outputs = pred.detach().cpu().numpy()
    sio.savemat('auto_seis_welsch_2.mat', {'outdata': outputs.squeeze()})
    # fig = plt.figure(2)
    # plt.imshow(inputs[57].squeeze(), aspect='auto')
    # plt.savefig('figuresource.png')
    # plt.show()
    #
    # fig = plt.figure(3)
    # plt.imshow(outputs[57].squeeze(), aspect='auto')
    # plt.savefig('figureout.png')
    # plt.show()
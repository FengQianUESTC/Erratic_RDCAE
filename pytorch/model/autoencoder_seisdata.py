import torch
import torch.nn as nn
import torch.nn.functional as F

class autoencoder_seisdata(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Sequential(                 #conv1 1-32  5 1 44 50
            nn.Conv2d(1,32,kernel_size=3,padding=1),           #           5  32  44  50
            nn.ReLU(inplace=True)
        )
        self.layer2 = nn.MaxPool2d(kernel_size=2,stride=2)      #          5 32 22 25

        self.layer3 = nn.Sequential(                #conv2 32-64
            nn.Conv2d(32,64,kernel_size=3,padding=1),         #            5 64 22 25
            nn.ReLU(inplace=True)
        )
        self.layer4 = nn.Sequential(                #conv3 64-32
            nn.Conv2d(64,32,kernel_size=3,padding=1),         #            5 32 22 25
            nn.ReLU(inplace=True)
        )
        self.layer5 = nn.MaxPool2d(kernel_size=2,stride=2)    #            5 32 11 12
        self.layer6 = torch.nn.Flatten()            #默认从第一维度开始平坦化 5 4224

        self.fc1 = nn.Sequential(
            nn.Linear(in_features=4224,out_features=352),  #5 352
            nn.ReLU(inplace=True),
        )
        self.fc2 = nn.Sequential(
            nn.Linear(in_features=352, out_features=4224), #352 4224
            nn.ReLU(inplace=True), )

        # self.reshaping = torch.reshape(self.fc2,[-1,32,11,12])

        #########
        # decoder
        #########
        self.layer7 = nn.Sequential(                #conv7 32-32
            nn.Conv2d(32,32,kernel_size=3,padding=1),         #            5 32 11 12
            nn.ReLU(inplace=True)
        )
        self.unsampling1 = nn.UpsamplingNearest2d([22, 25])    #5 32 22 25
        self.layer8 = nn.Sequential(                #conv8 32-64
            nn.Conv2d(32,64,kernel_size=3,padding=1),         #            5 64 22 25
            nn.ReLU(inplace=True)
        )
        self.layer9 = nn.Sequential(                # conv9 64-32
            nn.Conv2d(64, 32, kernel_size=3,padding=1),       # 5 32 22 25
            nn.ReLU(inplace=True)
        )
        self.unsampling2 = nn.UpsamplingNearest2d([44, 50])     #5 32 44 50

        self.layer10 = nn.Sequential(                # conv10 32-1
            nn.Conv2d(32, 1, kernel_size=3,padding=1)      # 5 1 44 50
        )

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.layer5(x)
        x = self.layer6(x)
        x = self.fc1(x)
        x = self.fc2(x)
        x = torch.reshape(x, [-1,32,11,12])
        # x = self.reshaping(x)
        x = self.layer7(x)
        x = self.unsampling1(x)
        x = self.layer8(x)
        x = self.layer9(x)
        x = self.unsampling2(x)
        x = self.layer10(x)
        return x


class TVLoss(nn.Module):
    def __init__(self,TVLoss_weight=1):
        super(TVLoss,self).__init__()
        self.TVLoss_weight = TVLoss_weight

    def forward(self,x):
        batch_size = x.size()[0]
        h_x = x.size()[2]
        w_x = x.size()[3]
        count_h =  (x.size()[2]-1) * x.size()[3]
        count_w = x.size()[2] * (x.size()[3] - 1)
        h_tv = torch.pow((x[:,:,1:,:]-x[:,:,:h_x-1,:]),2).sum()
        w_tv = torch.pow((x[:,:,:,1:]-x[:,:,:,:w_x-1]),2).sum()
        return self.TVLoss_weight*2*(h_tv/count_h+w_tv/count_w)/batch_size


def total_variation(images, name=None):
    ndims = 4
    if ndims == 3:
        # The input is a single image with shape [height, width, channels].

        # Calculate the difference of neighboring pixel-values.
        # The images are shifted one pixel along the height and width by slicing.
        pixel_dif1 = images[1:, :, :] - images[:-1, :, :]
        pixel_dif2 = images[:, 1:, :] - images[:, :-1, :]

        # Sum for all axis. (None is an alias for all axis.)
        sum_axis = None
    elif ndims == 4:
        # The input is a batch of images with shape:
        # [batch, height, width, channels].

        # Calculate the difference of neighboring pixel-values.
        # The images are shifted one pixel along the height and width by slicing.
        pixel_dif1 = images[:, :, 1:, :] - images[:, :, :-1, :]
        pixel_dif2 = images[:, :, :, 1:] - images[:, :, :, :-1]

        # Only sum for the last 3 axis.
        # This results in a 1-D tensor with the total variation for each image.
        sum_axis = [1, 2, 3]
    else:
        raise ValueError('\'images\' must be either 3 or 4-dimensional.')

    # Calculate the total variation by taking the absolute value of the
    # pixel-differences and summing over the appropriate axis.

    tot_var = torch.mean(torch.sum(torch.abs(pixel_dif1), [1, 2, 3]) + torch.sum(torch.abs(pixel_dif2), [1, 2, 3]))

    return tot_var
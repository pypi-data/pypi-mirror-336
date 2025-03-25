from functools import partial
from yip.learner import GeneralRelu, TrainCB, MetricsCB, ProgressCB, to_cpu, Callback, BaseSchedCB, BatchSchedCB, Learner, DeviceCB, CancelFitException
from yip.nn import conv, inplace ,DataLoaders, show_img
import torch
import torch.nn as nn
from torch.nn import init
from torchvision.transforms import ToTensor
from datasets import load_dataset
import torch.optim.lr_scheduler as lr_scheduler
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

def noop(x):
    return x

def conv_block(ni, nf, stride, act=gr, norm=None, ks=3):
    conv2 = conv(nf, nf, stride=stride, act=None, norm=norm, ks=ks)
    #if norm: init.constant_(conv2[1].weight,0.) #Sets first convolution to output zero => allows resblock to behave like a single neuron at the start
    return nn.Sequential(conv(ni, nf, stride=1, act=act, norm=norm, ks=ks), conv2)

class ResBlock(nn.Module):
    def __init__(self, ni, nf, stride=1, act=gr, norm=None, ks=3):
        super().__init__()
        self.convs = conv_block(ni, nf, stride, act=gr, norm=norm, ks=3)
        self.idconv = noop if ni==nf else  conv(ni, nf, stride=1, act=None, ks=1) #adjust number of channels for the input to match the output
        self.pool = noop if stride==1 else nn.AvgPool2d(2, ceil_mode=True) #match spatial dimensions
        self.act = act()

    def forward(self, x): return self.act(self.convs(x) + self.idconv(self.pool(x))) 
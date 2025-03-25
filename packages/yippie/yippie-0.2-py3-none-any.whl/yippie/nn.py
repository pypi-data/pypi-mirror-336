from torch import tensor, nn, optim
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler, BatchSampler, default_collate
import torch.nn.functional as F
import torch

from collections.abc import Mapping

import matplotlib.pyplot as plt
from operator import itemgetter
from datasets import load_dataset, load_dataset_builder

def_device = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'

def to_device(x, device=def_device):
    if isinstance(x, torch.Tensor): return x.to(device)
    if isinstance(x, Mapping): return {k:v.to(device) for k,v in x.items()}
    return type(x)(to_device(o, device) for o in x)

def collate_device(b): return to_device(default_collate(b))

def accuracy(out, yb): return (out.argmax(dim=1)==yb).float().mean()

def report(loss, preds, yb): print(f'{loss:.2f}, {accuracy(preds, yb):.2f}')

def fit(epochs, model, loss_func, opt, train_dl, valid_dl):
    for epoch in range(epochs):
        model.train()
        for xb,yb in train_dl:
            loss = loss_func(model(xb), yb)
            loss.backward()
            opt.step()
            opt.zero_grad()

        model.eval()
        with torch.no_grad():
            tot_loss,tot_acc,count = 0.,0.,0
            for xb,yb in valid_dl:
                pred = model(xb)
                n = len(xb)
                count += n
                tot_loss += loss_func(pred,yb).item()*n
                tot_acc  += accuracy (pred,yb).item()*n
        print(epoch, tot_loss/count, tot_acc/count)
    return tot_loss/count, tot_acc/count

def get_dls(train_ds, valid_ds, bs, **kwargs):
    return (DataLoader(train_ds, batch_size=bs, shuffle=True, **kwargs),
            DataLoader(valid_ds, batch_size=bs*2, **kwargs))

def inplace(f):
    def _f(b):
        f(b)
        return b
    return _f

def collate_dict(ds):
    get = itemgetter(*ds.features)
    def _f(b): return get(default_collate(b))
    return _f



class Dataset():
    def __init__(self, x, y): self.x,self.y = x,y
    def __len__(self): return len(self.x)
    def __getitem__(self, i): return self.x[i],self.y[i]

    

class DataLoaders:
    def __init__(self, *dls): self.train,self.valid = dls[:2]

    @classmethod
    def from_dd(cls, dd, batch_size, as_tuple=True, **kwargs):
        f = collate_dict(dd['train'])
        return cls(*get_dls(*dd.values(), bs=batch_size, collate_fn=f, **kwargs))
    
def conv(ni, nf, ks=3, stride=2, act= nn.ReLU, norm=None, bias=True):
    layers = [nn.Conv2d(ni, nf, stride=stride, kernel_size=ks, padding=ks//2, bias=bias)] 
    if norm: layers.append(norm(nf)) #layernorm doesn't actually need to know the number of inputs
    if act: layers.append(act())
    return nn.Sequential(*layers)

def show_img(row, column, images, *args):
    fig, ax = plt.subplots(row, column)
    plt.subplots_adjust(wspace=0.5, hspace=0.7)
    i = 0

    if row == 1 and column == 1:
        ax = [[ax]]

    grayscale = len(images.shape) == 2
    for r in range(row):
        for c in range(column):
            if grayscale:  # Grayscale image
                ax[r][c].imshow(images[i], cmap="gray")
                #ax[r][c].title.set_text(titles[i])
                ax[r][c].axis("off")
                i += 1
            else:
                ax[r][c].imshow(images[i])
                #ax[r][c].title.set_text(titles[i])
                ax[r][c].axis("off")
                i += 1
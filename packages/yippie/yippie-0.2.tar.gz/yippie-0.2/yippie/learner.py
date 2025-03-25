import torch
from datasets import load_dataset,load_dataset_builder
from torchvision.transforms import ToTensor
from torch import optim, nn, tensor
import torch.nn.functional as F
from operator import attrgetter
from copy import copy
from collections.abc import Mapping
from functools import partial
from .nn import DataLoaders, inplace, def_device, to_device
from torcheval.metrics import MulticlassAccuracy, Mean
from fastprogress import progress_bar,master_bar
import fastcore.all as fc
from contextlib import contextmanager

class CancelFitException(Exception): pass
class CancelBatchException(Exception): pass
class CancelEpochException(Exception): pass

class Learner():
    def __init__(self, model, dls, loss_func, lr, cbs, opt_func=optim.SGD): 
        self.model = model
        self.dls = dls
        self.loss_func = loss_func
        self.lr = lr
        self.cbs = cbs
        self.opt_func = opt_func

    @contextmanager
    def cb_ctx(self, nm):
        self.callback(f"before_{nm}")
        yield
        self.callback(f"after_{nm}")

    def one_batch(self):
        self.predict()
        self.get_loss()
        if self.model.training:
            self.backward()
            self.step()
            self.zero_grad()

    def one_epoch(self, train):
        self.model.train(train)
        self.dl = self.dls.train if train else self.dls.valid
        try:
           with self.cb_ctx('epoch'):
               for self.iter,self.batch in enumerate(self.dl):
                try:
                    with self.cb_ctx('batch'):
                        self.one_batch()
                except CancelBatchException: pass
        except CancelEpochException: pass
    
    def fit(self, n_epochs):
        self.n_epochs = n_epochs
        self.epochs = range(n_epochs)
        self.opt = self.opt_func(self.model.parameters(), self.lr)
        try:
            with self.cb_ctx('fit'):
                for self.epoch in self.epochs:
                    self.one_epoch(True)
                    self.one_epoch(False)
        except CancelFitException: pass

    def callback(self, method_nm): run_cbs(self.cbs, method_nm, self)

    def __getattr__(self, name):
        if name in ('predict', 'get_loss', 'backward', 'step', 'zero_grad'): return partial(self.callback, name)
        raise AttributeError(name)

    @property
    def training(self): return self.model.training

class Callback: order = 0

class TrainCB(Callback):
    def __init__(self, n_inp=1): self.n_inp = n_inp
    def predict(self, learn): learn.preds = learn.model(*learn.batch[:self.n_inp])
    def get_loss(self, learn): learn.loss = learn.loss_func(learn.preds, *learn.batch[self.n_inp:])
    def backward(self, learn): learn.loss.backward()
    def step(self, learn): learn.opt.step()
    def zero_grad(self, learn): learn.opt.zero_grad()

class MetricsCB(Callback):
        def __init__(self, *ms, **metrics):
            for o in ms: metrics[type(o).__name__] = o
            self.metrics = metrics
            self.all_metrics = copy(metrics)
            self.all_metrics['loss'] = self.loss = Mean()

        def print(self, d): print(d)
        def before_fit(self, learn): learn.metrics = self
        def before_epoch(self, learn): [o.reset() for o in self.all_metrics.values()]
        def after_epoch(self, learn):
            log = {k: f"{v.compute():.3f}" for k,v in self.all_metrics.items()}
            log['epoch'] = learn.epoch
            log['train'] = learn.model.training
            self.print(log)

        def after_batch(self, learn):
            x,y = to_cpu(learn.batch)
            for m in self.metrics.values(): m.update(to_cpu(learn.preds), y)
            self.loss.update(to_cpu(learn.loss))

class ProgressCB(Callback):
    order = MetricsCB.order+1
    def __init__(self, plot=False): self.plot = plot
    def before_fit(self, learn):
        learn.epochs = self.mbar = master_bar(learn.epochs)
        self.first = True
        if hasattr(learn, 'metrics'): learn.metrics._log = self._log
        self.losses = []
        self.val_losses = []

    def _log(self, d):
        if self.first:
            self.mbar.write(list(d), table=True)
            self.first = False
        self.mbar.write(list(d.values()), table=True)

    def before_epoch(self, learn): learn.dl = progress_bar(learn.dl, leave=False, parent=self.mbar)
    def after_batch(self, learn):
        learn.dl.comment = f'{learn.loss:.3f}'
        if self.plot and hasattr(learn, 'metrics') and learn.training:
            self.losses.append(learn.loss.item())
            if self.val_losses: self.mbar.update_graph([[fc.L.range(self.losses), self.losses],[fc.L.range(learn.epoch).map(lambda x: (x+1)*len(learn.dls.train)), self.val_losses]])
    
    def after_epoch(self, learn): 
        if not learn.training:
            if self.plot and hasattr(learn, 'metrics'): 
                self.val_losses.append(learn.metrics.all_metrics['loss'].compute())
                self.mbar.update_graph([[fc.L.range(self.losses), self.losses],[fc.L.range(learn.epoch+1).map(lambda x: (x+1)*len(learn.dls.train)), self.val_losses]])
    

class DeviceCB(Callback):
    def __init__(self, device=def_device): fc.store_attr()
    def before_fit(self, learn):
        if hasattr(learn.model, 'to'): learn.model.to(self.device)
    def before_batch(self, learn): learn.batch = to_device(learn.batch, device=self.device)

    

def to_cpu(x):
    if isinstance(x, Mapping): return {k:to_cpu(v) for k,v in x.items()}
    if isinstance(x, list): return [to_cpu(o) for o in x]
    if isinstance(x, tuple): return tuple(to_cpu(list(x)))
    return x.detach().cpu()

def run_cbs(cbs, method_name, learn=None):
    for cb in sorted(cbs, key=attrgetter('order')):
        method = getattr(cb, method_name, None)
        if method is not None: method(learn)

class GeneralRelu(nn.Module):
    def __init__(self, leak=None, sub=None, maxv=None):
        super().__init__()
        self.leak,self.sub,self.maxv = leak,sub,maxv

    def forward(self, x): 
        x = F.leaky_relu(x,self.leak) if self.leak is not None else F.relu(x)
        if self.sub is not None: x -= self.sub
        if self.maxv is not None: x.clamp_max_(self.maxv)
        return x

class LayerNorm(nn.Module):
    def __init__(self, dummy, e=1e-5):
        super().__init__()
        self.e = e
        self.mult = nn.Parameter(tensor(1.))
        self.add = nn.Parameter(tensor(0.))

    def forward(self,x):
        #mean and var across CHW of NCHW
        mean = x.mean((1,2,3), keepdim=True)
        var =x.var((1,2,3), keepdim=True)
        z = (x - mean) / (var + self.e).sqrt()
        return self.mult * z + self.add

    
class BatchNormCB(Callback):
    def __init__(self, tfm): self.tfm = tfm
    def before_batch(self, learn): learn.batch = self.tfm(learn.batch)


class BaseSchedCB(Callback):
    def __init__(self, sched): self.sched = sched

    def before_fit(self, learn): self.schedo = self.sched(learn.opt)

    def _step(self, learn):
        if learn.training: self.schedo.step() #update the learning rate


#Create a scheduler to update the lr every batch
class BatchSchedCB(BaseSchedCB):
    def after_batch(self, learn): self._step(learn) #update the lr


class BatchTransformCB(Callback):
    def __init__(self, tfm, on_train=True, on_val=True):
        self.tfm = tfm
        self.on_train = on_train
        self.on_val = on_val

    def before_batch(self, learn):
        if(self.on_train and learn.training) or (self.on_val and not learn.training):
            learn.batch = self.tfm(learn.batch)

class SingleBatchCB(Callback):
    order = 1
    def after_batch(self, learn): raise CancelFitException()



class CheckLayersCB(Callback):
    def __init__(self, model):
        self.model = model
        self.sizes = [[] for _ in model]  

    def checkLayers(self, i, module, inp, out):
        self.sizes[i].append(type(module).__name__)
        self.sizes[i].append(inp[0].shape)
        self.sizes[i].append(out[0].shape)
        self.sizes[i].append(sum([o.numel() for o in module.parameters()])) #for each tensor get the numnber of elements

    def before_fit(self, learn):
        for i, l in enumerate(self.model): l.register_forward_hook(partial(self.checkLayers, i))

    def display(self):
        data = self.sizes
        headers = ["Layer", "Input", "Output", "no. of parameters"]
        print(tabulate(data, headers, tablefmt="grid"))
    
    def init_weights(l):
        if isinstance(l, nn.Conv2d): init.kaiming_normal_(l.weight)
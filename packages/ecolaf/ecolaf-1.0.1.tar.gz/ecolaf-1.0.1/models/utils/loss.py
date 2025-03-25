import torch
import torch.nn as nn
import numpy as np
from torch import Tensor

KITTI_LOSS_WEIGHT = torch.tensor([
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # background
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # asphalt
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # concrete
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # metal
    [0.0, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # road marking
    [0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # tar
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # fabric, leather
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # glass
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # plaster
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # plastic
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # rubber, vinyl
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # mud sand soil gravel
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # ceramic
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # cobblestone
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # brick
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.1, 0.5, 0.0, 0.0, 0.0], # grass
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], # wood
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.2, 1.0, 0.0, 0.0, 0.0], # leaf
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], # water
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0], # human body
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], # sky
],dtype=torch.float32)

class MyCrossEntropyLoss(torch.nn.NLLLoss):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

    def forward(self, input: Tensor, target: Tensor, mask: Tensor) -> Tensor:
        if mask is not None:
            assert target.size() == mask.size()
            target[mask>0] = self.ignore_index
        return super().forward(torch.log(input+1e-20),target)


class MyWeightedCrossEntropyLoss(nn.NLLLoss):
    def __init__(self, weight=None, size_average=None, ignore_index=-100, reduce=None, reduction='mean'):
        super(MyWeightedCrossEntropyLoss, self).__init__(weight, size_average, ignore_index, reduce, reduction)

    def forward(self, input, target, weight):
        """
        Args:
            input: Log-probabilities from your model (shape: [batch_size, num_classes, ...]).
            target: Ground truth labels (shape: [batch_size, ...]).
            weight: A tensor of weights (shape: [batch_size, ...]) for each sample.
        """
        if weight is None:
            raise ValueError("Weight tensor must be provided for weighted loss computation.")

        # Apply log softmax to input if it's not already in log-probability format
        if not torch.is_tensor(weight):
            weight = torch.tensor(weight, dtype=torch.float32, device=input.device)

        nll_loss = F.nll_loss(torch.log(input+1e-20), target, weight=self.weight, reduction='none')

        # Multiply by the sample weights
        weighted_loss = nll_loss * weight

        # Aggregate according to the specified reduction
        if self.reduction == 'mean':
            return weighted_loss.mean()
        elif self.reduction == 'sum':
            return weighted_loss.sum()
        else:
            return weighted_loss


class MyMSE(torch.nn.MSELoss):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

    def forward(self, input: Tensor, target: Tensor, mask: Tensor) -> Tensor:
        return super().forward(input,target)


class MyOhemCrossEntropy(nn.Module):
    def __init__(self, ignore_label: int = 255, weight: Tensor = None, thresh: float = 0.7, aux_weights: list = [1, 1]) -> None:
        super().__init__()
        self.ignore_label = ignore_label
        self.aux_weights = aux_weights
        self.thresh = -torch.log(torch.tensor(thresh, dtype=torch.float))
        self.criterion = nn.NLLLoss(weight=weight, ignore_index=ignore_label, reduction='none')

    def _forward(self, preds: Tensor, labels: Tensor, weights: Tensor, mask=None) -> Tensor:
        # preds in shape [B, C, H, W] and labels in shape [B, H, W]
        n_min = labels[labels != self.ignore_label].numel() // 16
        loss = (weights * self.criterion(preds, labels)).view(-1)
        loss_hard = loss[loss > self.thresh]

        if loss_hard.numel() < n_min:
            loss_hard, _ = loss.topk(n_min)

        return torch.mean(loss_hard)

    def forward(self, preds, labels: Tensor, weights: Tensor) -> Tensor:
        if isinstance(preds, tuple):
            return sum([w * self._forward(pred, labels, weights=weights) for (pred, w) in zip(preds, self.aux_weights)])
        return self._forward(preds, labels, weights=weights)

class SegmentationLosses(object):
    def __init__(self, weight=None, size_average=True, batch_average=False, ignore_index=255, cuda=False):
        self.ignore_index = ignore_index
        self.weight = weight
        self.size_average = size_average
        self.batch_average = batch_average
        self.cuda = cuda

    def build_loss(self, mode='ce'):
        """Choices: ['ce' or 'focal' or 'original']"""
        if mode == 'ce':
            # return self.CrossEntropyLoss
            return self.CrossEntropyLossAdv
        elif mode == 'focal':
            return self.FocalLoss
        elif mode == 'original':
            return self.OriginalLoss
        elif mode == 'bce':
            return self.BCELoss
        elif mode == 'my_ce':
            return self.MyCrossEntropyAdv
        elif mode == 'my_ohem':
            return self.MyOhemCrossEntropy
        else:
            raise NotImplementedError

    def CrossEntropyLoss(self, logit, target):
        n, c, h, w = logit.size()
        criterion = nn.CrossEntropyLoss(weight=self.weight, ignore_index=self.ignore_index,
                                        size_average=self.size_average)
        if self.cuda:
            criterion = criterion.cuda()

        loss = criterion(torch.log(logit+1e-20), target.long())

        if self.batch_average:
            loss = loss/n

        return loss

    def MyCrossEntropyAdv(self, logit, target, mask=None):
        n, c, h, w = logit.size()
        if mask is not None:
            assert target.size() == mask.size()
            target[mask>0] = self.ignore_index
        criterion = nn.NLLLoss(weight=self.weight, ignore_index=self.ignore_index, size_average=self.size_average)
        if self.cuda:
            criterion = criterion.cuda()
        #loss=criterion(torch.log(logit+1e-20), target.long())
        loss = criterion(torch.log(torch.clamp(logit, 1e-20, 1)), target.long())
        if self.batch_average:
            loss = loss/n

        return loss


    def MyOhemCrossEntropy(self, logit, target, weights=None, mask=None, thresh: float = 0.7, aux_weights: list = [1, 1]):
            thresh = -torch.log(torch.tensor(thresh, dtype=torch.float))
            criterion = nn.NLLLoss(weight=self.weight, ignore_index=self.ignore_index, reduction='none')
            if self.cuda:
                criterion = criterion.cuda()


            def _forward(preds: Tensor, labels: Tensor, criterion, ignore_index=self.ignore_index) -> Tensor:
                # preds in shape [B, C, H, W] and labels in shape [B, H, W]
                n_min = labels[labels != ignore_index].numel() // 16
                if isinstance(weights, Tensor):
                    loss = (weights * criterion(torch.log(torch.clamp(preds, 1e-20, 1)), labels.long())).view(-1)
                else:
                    loss = criterion(torch.log(torch.clamp(preds, 1e-20, 1)), labels.long()).view(-1)
                loss_hard = loss[loss > thresh]

                if loss_hard.numel() < n_min:
                    loss_hard, _ = loss.topk(n_min)

                return torch.mean(loss_hard)

            if isinstance(logit, tuple):
                return sum([w * _forward(lo, labels, criterion) for (lo, w) in zip(logit, aux_weights)])
            return _forward(logit, target, criterion)



    def CrossEntropyLossAdv(self, logit, target, mask=None):
        n, c, h, w = logit.size()
        #print(target.long().size())
        #print(mask.size())
        if mask is not None:
            assert target.size() == mask.size()
            target[mask>0] = self.ignore_index
            #target[mask>0] = 0
        #print(self.ignore_index)
        criterion = nn.CrossEntropyLoss(weight=self.weight, ignore_index=self.ignore_index,
                                        size_average=self.size_average)
        #criterion = nn.BCEWithLogitsLoss(weight=self.weight,
        #                                 size_average=self.size_average)
        if self.cuda:
            criterion = criterion.cuda()
        #print(logit.size())   
        #target=target.unsqueeze(1) 
        #loss = criterion(logit, target.long())
        #a=nn.Sigmoid()
        #print(a(logit))
        #print(target.long().size())
        
        loss = criterion(logit, target.long())
        #print(loss)
        if self.batch_average:
            loss = loss/n

        return loss
    def BCELoss(self, logit, target1, mask=None):
        n, c, h, w = logit.size()
        loss=0
        #print(target.long().size())
        #print(mask.size())
        if mask is not None:
            assert target1.size() == mask.size()
            target1[mask>0] = self.ignore_index
            #target[mask>0] = 0
        criterion = nn.BCEWithLogitsLoss(weight=self.weight,
                                         size_average=self.size_average)
        if self.cuda:
            criterion = criterion.cuda()
        target2=np.zeros((target1.shape[0],20,target1.shape[1],target1.shape[2]))
        for k in range(target1.shape[0]):
            for i in range(20):
                target2[k,i,:,:]=np.int64(target1.cpu().numpy()[k,:,:]==i)
        target=torch.from_numpy(target2).cuda()
        for i in range(20):
            #print(target[:,i,:,:].shape)
            loss += criterion(logit[:,i,:,:], target[:,i,:,:])
        #print(loss)
        if self.batch_average:
            loss = loss/n

        return loss

    def FocalLoss(self, logit, target, mask=None, gamma=2, alpha=0.5):
        n, c, h, w = logit.size()

        if mask is not None:
            assert target.size() == mask.size()
            target[mask>0] = self.ignore_index

        criterion = nn.CrossEntropyLoss(weight=self.weight, ignore_index=self.ignore_index,
                                        size_average=self.size_average)
        if self.cuda:
            criterion = criterion.cuda()

        logpt = -criterion(logit, target.long())
        pt = torch.exp(logpt)
        if alpha is not None:
            logpt *= alpha
        loss = -((1 - pt) ** gamma) * logpt

        if self.batch_average:
            loss /= n

        return loss

    def OriginalLoss(self, logit, target):
        n, c, h, w = logit.size()
        criterion = nn.CrossEntropyLoss(weight=self.weight, ignore_index=self.ignore_index,
                                        size_average=self.size_average)
        if self.cuda:
            criterion = criterion.cuda()
        target_weight = KITTI_LOSS_WEIGHT[target.long()].permute((0,3,1,2)).float().cuda()
        exp_x  = torch.exp(logit)
        loss = torch.sum(torch.mean(-torch.sum(target_weight * logit,dim=1) + torch.log(torch.sum(exp_x,dim=1)),dim=(1,2)))

        if self.batch_average:
            loss /= n

        return loss

if __name__ == "__main__":
    loss = SegmentationLosses(cuda=True)
    a = torch.rand(1, 21, 7, 7).cuda()
    b = torch.rand(1, 7, 7).cuda()
    print(a)
    print(b)
    print(loss.CrossEntropyLoss(a, b).item())
    print(loss.FocalLoss(a, b, gamma=0, alpha=None).item())
    print(loss.OriginalLoss(a,b).item())
    print(loss.FocalLoss(a, b, gamma=2, alpha=0.5).item())





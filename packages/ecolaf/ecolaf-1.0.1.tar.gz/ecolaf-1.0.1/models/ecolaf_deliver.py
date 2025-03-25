from src.ecolaf import *
import torch
import torch.nn as nn
#import torchvision
from segformer import Segformer
from functools import partial
from models.dataloaders import make_data_loader
from tqdm import tqdm
import numpy as np
from models.utils.metrics import Evaluator

NUM_CLASSES = 25
CUDA = True

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
torch.autograd.set_detect_anomaly(True)

torch.set_float32_matmul_precision(precision="medium")

model_rgb = Segformer(
    pretrained = None,
    img_size = 512, 
    patch_size = 4, 
    embed_dims = (64, 128, 320, 512), 
    num_heads = (1, 2, 5, 8), 
    mlp_ratios = (4, 4, 4, 4),
    qkv_bias = True, 
    depths = (3, 4, 6, 3), 
    sr_ratios = (8, 4, 2, 1),
    drop_rate = 0.0, 
    drop_path_rate = 0.1,
    decoder_dim = 512,
    norm_layer = partial(nn.LayerNorm, eps=1e-6), 
    num_classes=NUM_CLASSES+1,
    ).to(device)
        
model_depth = Segformer(
    pretrained = None,
    img_size = 512, 
    patch_size = 4, 
    embed_dims = (64, 128, 320, 512), 
    num_heads = (1, 2, 5, 8), 
    mlp_ratios = (4, 4, 4, 4),
    qkv_bias = True, 
    depths = (3, 4, 6, 3), 
    sr_ratios = (8, 4, 2, 1),
    drop_rate = 0.0, 
    drop_path_rate = 0.1,
    decoder_dim = 512,
    norm_layer = partial(nn.LayerNorm, eps=1e-6), 
    num_classes=NUM_CLASSES+1, 
    in_chans=3,
    ).to(device)

model_lidar = Segformer(
    pretrained = None,
    img_size = 512, 
    patch_size = 4, 
    embed_dims = (64, 128, 320, 512), 
    num_heads = (1, 2, 5, 8), 
    mlp_ratios = (4, 4, 4, 4),
    qkv_bias = True, 
    depths = (3, 4, 6, 3), 
    sr_ratios = (8, 4, 2, 1),
    drop_rate = 0.0, 
    drop_path_rate = 0.1,
    decoder_dim = 512,
    norm_layer = partial(nn.LayerNorm, eps=1e-6), 
    num_classes=NUM_CLASSES+1,
    in_chans=3,
    ).to(device)

model_event = Segformer(
    pretrained = None,
    img_size = 512, 
    patch_size = 4, 
    embed_dims = (64, 128, 320, 512), 
    num_heads = (1, 2, 5, 8), 
    mlp_ratios = (4, 4, 4, 4),
    qkv_bias = True, 
    depths = (3, 4, 6, 3), 
    sr_ratios = (8, 4, 2, 1),
    drop_rate = 0.0, 
    drop_path_rate = 0.1,
    decoder_dim = 512,
    norm_layer = partial(nn.LayerNorm, eps=1e-6), 
    num_classes=NUM_CLASSES+1,
    in_chans=3,
    ).to(device)


device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

MyModel = ECOLAF([model_rgb, model_depth, model_lidar, model_event], NUM_CLASSES).to(device)

ckpt = torch.load('ECOLAF_DELIVER_checkpoint.pth.tar')

MyModel.load_state_dict(ckpt['state_dict'], strict=True)

train_loader, val_loader, test_loader = make_data_loader(dataset='DELIVER', root='/home/lderegnaucourt/data/DELIVER', crop_size=512, batch_size=1, test_batch_size=2)

tbar = tqdm(test_loader, desc='\r')

MyModel.eval()

evaluator = Evaluator(NUM_CLASSES)
evaluator.reset()

for i, (sample, label) in enumerate(tbar):
    image, target, depth, lidar, event = sample[0].to(device), label.to(device), sample[1].to(device), sample[2].to(device), sample[3].to(device)
    with torch.amp.autocast('cuda', enabled=False):
        with torch.no_grad():
            output = MyModel([image, depth, lidar, event], interpolation=True)
    pred = output.data.cpu().numpy()
    target_ = target.cpu().numpy()
    pred = np.argmax(pred, axis=1)
    evaluator.add_batch(target_, pred)

mIoU = evaluator.Mean_Intersection_over_Union()
print("mIoU:{}".format(mIoU))
confusion_matrix = evaluator.confusion_matrix
np.save('confusion_matrix',confusion_matrix)

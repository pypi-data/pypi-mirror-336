from src.ecolaf import *
import torch
import torch.nn as nn
#import torchvision
from segformer import Segformer
from functools import partial
#from dataloader import make_data_loader
from tqdm import tqdm
import numpy as np
#from JeanZayTraining.utils.metrics import Evaluator

NUM_CLASSES = 25 #19 #25
CUDA = True

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


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

        

ckpt = torch.load('checkpoint_DELIVER.pth.tar', weights_only=False)

rgb = {}
depth = {}
lidar = {}
event = {}

for k, v in ckpt["state_dict"].items():
    if 'model_rgb' in k:
        rgb[k[10:]] = v
    elif 'model_depth' in k:
        depth[k[12:]] = v
    elif 'model_lidar' in k:
        lidar[k[12:]] = v
    elif 'model_event' in k:
        event[k[12:]] = v
    else:
        print(k)

model_rgb.load_state_dict(rgb)
model_depth.load_state_dict(depth)
model_lidar.load_state_dict(lidar)
model_event.load_state_dict(event)

print('LOADING OK')

MyModel = ECOLAF([model_rgb, model_depth, model_lidar, model_event], NUM_CLASSES).cuda()


torch.save({'state_dict': MyModel.state_dict()}, 'new_ECOLAF_DELIVER_checkpoint.pth.tar')
print('checkpoint saved')


"""
MyModel = torch.load('checkpoint.pth.tar', weights_only = False).cuda()
for m in MyModel.models:
    m = m.cuda()
"""

ckpt = torch.load('new_ECOLAF_DELIVER_checkpoint.pth.tar')["state_dict"]
MyModel.load_state_dict(ckpt)

print('LOADING accomplished, sir!')
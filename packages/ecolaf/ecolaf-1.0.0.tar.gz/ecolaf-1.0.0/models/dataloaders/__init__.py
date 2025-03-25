from dataloaders.datasets import deliver, muses, muses_clear_train
from torch.utils.data import DataLoader
from dataloaders.augmentations_mm import *

def make_data_loader(dataset, root='PathToDELIVER', crop_size=1024, batch_size=2, test_batch_size=2, **kwargs):

    if dataset == 'DELIVER':
        modals=['img', 'depth', 'lidar', 'event']
        #cases=['cloud', 'fog', 'night', 'rain', 'sun', 'motionblur', 'overexposure', 'underexposure', 'lidarjitter', 'eventlowres']
        traintransform = get_train_augmentation((crop_size, crop_size), seg_fill=255)
        valtransform = get_val_augmentation((crop_size, crop_size))
        testtransform = get_val_augmentation((crop_size, crop_size)) #(1024,1024) original image shape
        train_set = deliver.DELIVER(transform=traintransform, root=root, split='train', modals=modals)
        val_set = deliver.DELIVER(transform=valtransform, root=root, split='val', modals=modals)
        test_set = deliver.DELIVER(transform=testtransform, root=root, split='test', modals=modals)

        train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, **kwargs)
        val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, **kwargs)
        test_loader = DataLoader(test_set, batch_size=test_batch_size, shuffle=False, **kwargs)

        return train_loader, val_loader, test_loader


    elif dataset == 'MUSES':
        modals=['img', 'event', 'lidar', 'radar']
        traintransform = get_train_augmentation((700, 1250), seg_fill=255)
        valtransform = get_val_augmentation((700, 1250))
        testtransform = get_val_augmentation((700, 1250))  #(1080,1920) original shape
        train_set = muses.MUSES(transform=traintransform, split='train', modals=modals)
        val_set = muses.MUSES(transform=valtransform, split='val', modals=modals)
        test_set = muses.MUSES(transform=testtransform, split='test', modals=modals)

        train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, **kwargs)
        val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, **kwargs)
        test_loader = DataLoader(test_set, batch_size=test_batch_size, shuffle=False, **kwargs)

        return train_loader, val_loader, test_loader

    elif dataset == 'MUSES_CLEAR_TRAIN':
        modals=['img', 'event', 'lidar', 'radar']
        traintransform = get_train_augmentation((700, 1250), seg_fill=255)
        valtransform = get_val_augmentation((700, 1250))
        testtransform = get_val_augmentation((700,1250)) #(1080,1920) original shape
        train_set = muses_clear_train.MUSES_CLEAR_TRAIN(transform=traintransform, split='train', modals=modals, case='clear')
        val_set = muses_clear_train.MUSES_CLEAR_TRAIN(transform=valtransform, split='val', modals=modals, case='clear')
        test_set = muses_clear_train.MUSES_CLEAR_TRAIN(transform=testtransform, split='test', modals=modals, case='rainy') #CHANGER LES CONDITIONS METEO ICI ['rainy', 'fog', 'snow']

        train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, **kwargs)
        val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, **kwargs)
        test_loader = DataLoader(test_set, batch_size=test_batch_size, shuffle=False, **kwargs)

        return train_loader, val_loader, test_loader
    else:
        raise NotImplementedError

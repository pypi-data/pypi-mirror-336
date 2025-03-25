__author__='Lucas DEREGNAUCOURT'
__author_email__='lucas.deregnaucourt@insa-rouen.fr'

import torch
import torch.nn as nn
import torch.nn.functional as F

from Dempster_Shafer_utils import *

class ECOLAF(nn.Module):
    def __init__(self, models:list, num_classes:int):
        '''
        models: a list of M unimodal models.
        !!! Be sure that the linear layer output K+1 values (K: number of classes) !!!

        num_classes (Integer): number of classes
        '''
        super(ECOLAF, self).__init__()

        self.models = nn.ModuleList(models)
        self.fusion_layer = Dempster_layer()
        self.discounting_layer = Discounting_layer(num_classes, len(models))
        self.proba_transform = DSmP(1e-3)

    def forward(self, input:list, output_unimodal=False, output_conflict=False, output_discounting_coef=False, interpolation=False, output_keyword=None):
        '''
        We consider that M models were given for the initialization.
        
        input: list of M images
        
        output_unimodal (Boolean): returns the list of outputs for each model
        
        output_conflict (Boolean): returns a conflict map of shape BxMxHxW (B: batch size)
        
        output_discounting_coef (Boolean): returns the discounting coefficients map of shape BxMxHxW (B: batch size)
        
        interpolation (Boolean): interpolates the output to the original image size
        
        output_keyword (String): key to access to the output tensor if the model's output is a dictionary 
        (for example, the deeplabV3_resnet50 model from torchvision requires output_keyword='out')
        '''


        '''
        Infer the output for each modality
        '''
        unimodals = [] if output_unimodal else None        
        modality_outputs = []

        for i in range(len(self.models)):
            out_u = self.models[i](input[i])
            
            if output_keyword is not None:
                out_u = out_u[output_keyword]
            out_u = F.softmax(out_u, dim=1)
            if output_unimodal:
                unimodals.append(out_u)
            modality_outputs.append(out_u)

        out = torch.stack(modality_outputs, dim=2)
        
        '''
        Discount the mass functions with the adaptive discounting layer
        '''
        out_discounted, conflict_map, discounting_coefs_map = self.discounting_layer(out, output_conflict, output_discounting_coef)

        '''
        Merge the mass functions with the Dempster's rule
        '''
        out_fusion = self.fusion_layer(out_discounted)
            
        '''
        Resize the output to the original shape
        '''
        interp_size = input[0].shape[2:]  #shape for the interpolation

        if interpolation:
            out_fusion = F.interpolate(out_fusion, size=interp_size, mode='bilinear', align_corners=False)
        
        out_fusion = self.proba_transform(out_fusion)

        outputs = [out_fusion]

        if output_unimodal:
            if interpolation:
                unimodals = [self.proba_transform(F.interpolate(o, size=interp_size, mode='bilinear', align_corners=False)) for o in unimodals]
            else:
                unimodals = [self.proba_transform(o) for o in unimodals]
            outputs.append(unimodals)


        if output_conflict:
            outputs.append(conflict_map)
        if output_discounting_coef:
            outputs.append(discounting_coefs_map)
        
        return out_fusion if len(outputs)==1 else outputs

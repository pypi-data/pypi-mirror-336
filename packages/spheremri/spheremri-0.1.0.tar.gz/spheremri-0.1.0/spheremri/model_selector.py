# Set environment variable to disable xFormers warnings 
# This must be done before importing torch
import os
os.environ['DINOV2_XFORMERS_DISABLED'] = '1'

import torch
import torch.nn as nn
from transformers import AutoImageProcessor
from torchvision.transforms import Compose, Normalize
import pdb

class DictToTensor(nn.Module):
    def __init__(self, key='features'):
        super().__init__()
        self.key = key
    
    def forward(self, x):
        return x[self.key]
    
class ModelSelector:
    """
    Class to load different pretrained models and their corresponding transforms
    """
    def __init__(self, model_name='dinov2_small'):
        self.model_name = model_name
        self.model = None
        self.transform = None
        self.embedding_dim = None
        self._load_model_and_transform()

    def _load_model_and_transform(self):
        """
        Load the specified model and its preprocessing transforms
        """
        # DINOv2
        model_path = 'facebookresearch/dinov2'
        hub_model = 'dinov2_vits14_reg'
        self.embedding_dim = 384
            
        self.model = torch.hub.load(model_path, hub_model)
        self.transform = Compose([
            Normalize(mean=[0.485, 0.456, 0.406], 
                      std=[0.229, 0.224, 0.225])
        ])

    
    def get_model(self):
        
        return self.model
    
    def get_transform(self):
        
        return self.transform
    
    def get_embedding_dim(self):
        
        return self.embedding_dim
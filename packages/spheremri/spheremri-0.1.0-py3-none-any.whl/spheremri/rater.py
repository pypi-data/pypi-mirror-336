"""
NiftiQualityRater module for rating MRI image quality
"""

import torch
import torch.nn.functional as F
from pathlib import Path
from PIL import Image
from torchvision import transforms
import numpy as np
from tqdm import tqdm
import nibabel as nib
import os
import pkg_resources


class NiftiQualityRater:
    def __init__(self, model, device='cuda', contrastive='angular', num_anchor_images=30, use_prebuilt_anchor=True, contrast='tse'):
        """
        Initialize the image rater
        
        Args:
            model: Your embedding model
            device: Device to run inference on
            num_anchor_images: Number of high-quality images to use for anchor
            use_prebuilt_anchor: Whether to use the prebuilt anchor embedding
            contrast: Type of contrast to use ('tse' or 't1')
        """
        self.model = model.to(device)
        self.model.eval()
        self.device = device
        self.num_anchor_images = num_anchor_images
        self.anchor_embedding = None
        self.contrastive = contrastive
        self.contrast = contrast
        
        # Standard image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Load prebuilt anchor if requested
        if use_prebuilt_anchor:
            try:
                self.load_prebuilt_anchor()
            except Exception as e:
                print(f"Could not load prebuilt anchor: {e}")
    
    def load_prebuilt_anchor(self):
        """
        Load a prebuilt anchor embedding from the package
        """
        try:
            # Determine which anchor file to use based on contrast
            if self.contrast == 't1':
                anchor_filename = 't1_anchor.pt'
            else:  # Default to TSE
                anchor_filename = 'tse_anchor.pt'
                
            # Get the path to the anchor file in the package
            anchor_path = pkg_resources.resource_filename('spheremri', anchor_filename)
            if os.path.exists(anchor_path):
                self.anchor_embedding = torch.load(anchor_path, map_location=self.device)
                return True
            else:
                print(f"Prebuilt anchor not found at {anchor_path}")
                return False
        except Exception as e:
            print(f"Error loading prebuilt anchor: {e}")
            return False
    
    def nifti_to_tensor(self, nifti_path, slice_idx):
        """
        Convert a NIfTI image slice to a tensor
        
        Args:
            nifti_path: Path to NIfTI file
            slice_idx: Index of slice to use (-1 for last slice)
            
        Returns:
            tensor: Preprocessed image tensor
        """
        # Load NIfTI file
        nifti_img = nib.load(nifti_path)
        img_data = nifti_img.get_fdata()
        
        img_tensors = []
        if slice_idx == -1:
            for idx in range(img_data.shape[slice_idx]):
                slice_data = np.rot90(img_data[:,:,idx], 1)
                slice_data = ((slice_data - np.nanmin(slice_data)) * (255.0 / (np.nanmax(slice_data) - np.nanmin(slice_data) + 1e-6))).astype(np.uint8)
                img_pil = Image.fromarray(np.stack([slice_data] * 3, axis=-1))
                img_tensor = self.transform(img_pil).unsqueeze(0).to(self.device)
                img_tensors.append(img_tensor.squeeze())

        elif slice_idx == 1:
            for idx in range(img_data.shape[slice_idx]):
                slice_data = np.rot90(img_data[:,idx,:], 1)
                slice_data = ((slice_data - np.nanmin(slice_data)) * (255.0 / (np.nanmax(slice_data) - np.nanmin(slice_data) + 1e-6))).astype(np.uint8)
                img_pil = Image.fromarray(np.stack([slice_data] * 3, axis=-1))
                img_tensor = self.transform(img_pil).unsqueeze(0).to(self.device)
                img_tensors.append(img_tensor.squeeze())

        return torch.stack(img_tensors)
    
    def compute_angular_distance(self, emb1, emb2):
        """Compute angular distance between embeddings"""
        emb1 = F.normalize(emb1, p=2, dim=1)
        emb2 = F.normalize(emb2, p=2, dim=1)
        
        cos_sim = torch.mm(emb1, emb2.t())
        cos_sim = torch.clamp(cos_sim, -1 + 1e-7, 1 - 1e-7)
        angular_dist = torch.arccos(cos_sim) / torch.pi
        
        return angular_dist
    
    def create_anchor_embedding(self, quality_image_dir, slice_idx):
        """
        Create anchor embedding from high-quality images and store individual embeddings
        """
        quality_dir = Path(quality_image_dir)
        image_paths = list(quality_dir.glob('*.nii.gz')) + list(quality_dir.glob('*.nii'))
        
        if len(image_paths) > self.num_anchor_images:
            image_paths = np.random.choice(image_paths, self.num_anchor_images, replace=False)
        
        all_anchor_embeddings = []  
        
        with torch.no_grad():
            for img_path in tqdm(image_paths, desc="Creating anchor embedding"):
                try:
                    img_tensor = self.nifti_to_tensor(img_path, slice_idx)
                    embedding = self.model(img_tensor)
                    all_anchor_embeddings.append(embedding)
                    
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
                    continue
        
        if not all_anchor_embeddings:
            raise ValueError("No valid images found for anchor embedding")
        
        self.all_anchor_embeddings = torch.cat(all_anchor_embeddings, dim=0)
        
        self.anchor_embedding = torch.mean(self.all_anchor_embeddings, dim=0, keepdim=True)

        if len(self.anchor_embedding.shape) == 4:
            self.anchor_embedding = self.anchor_embedding.squeeze(-1).squeeze(-1)

        return self.anchor_embedding
    
    def rate_image(self, image_path, slice_idx):
        """
        Rate a single image by comparing to anchor embedding
        
        Args:
            image_path: Path to NIfTI image to rate
            slice_idx: Index of slice to use (-1 for last slice)
            
        Returns:
            score: Quality score (0-1, where 1 is highest quality)
            embedding: Image embedding
        """
        if self.anchor_embedding is None:
            raise ValueError("Must create anchor embedding first")
        
        with torch.no_grad():
            img_tensor = self.nifti_to_tensor(image_path, slice_idx)
            embedding = self.model(img_tensor)    

            if len(embedding.shape) == 4:
                embedding = embedding.squeeze(-1).squeeze(-1)

            if self.contrastive == 'angular':
                distance = self.compute_angular_distance(embedding, self.anchor_embedding)    
                score = 1 - distance.mean().item()

                return score, embedding, distance.detach().cpu().squeeze()
            elif self.contrastive == 'euclidean':
                raw_distance = torch.cdist(F.normalize(embedding, p=2, dim=1), F.normalize(self.anchor_embedding, p=2, dim=1))
                score = 1 - torch.clamp(raw_distance, 0, 1).mean().item()

                return score, embedding, raw_distance.detach().cpu().squeeze()

import torch
import os
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

class ResNetFeatureExtractor:
    def __init__(self):
        """
        Initialize the ResNet-50 model pretrained on ImageNet.
        Removes the final classification layer to get feature vectors.
        """
        # Load pretrained ResNet50
        self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        # Remove the last fully connected layer
        self.feature_extractor = nn.Sequential(*list(self.model.children())[:-1])
        self.feature_extractor.eval()
        
        # Preprocessing transforms (ResNet expects 3 channels, even if grayscale was used)
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def load_weights(self, path):
        """Load weights (e.g., from federated training update)."""
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path))
            self.feature_extractor = nn.Sequential(*list(self.model.children())[:-1])
            self.feature_extractor.eval()
            return True
        return False

    def extract_features(self, preprocessed_image):
        """
        Extract 2048-dimensional feature vector from a preprocessed image.
        
        Args:
            preprocessed_image (np.array): Preprocessed grayscale image (normalized).
            
        Returns:
            np.array: 2048-dimensional feature vector.
        """
        # ResNet expects 3 channels. If we have 1 channel (grayscale), repeat it.
        if len(preprocessed_image.shape) == 2:
            image_3ch = np.stack([preprocessed_image] * 3, axis=-1)
        else:
            image_3ch = preprocessed_image

        # Convert to PIL for transforms
        # Scale back to 255 for PIL if normalized to 0-1
        pil_image = Image.fromarray((image_3ch * 255).astype(np.uint8))
        
        # Apply transforms and add batch dimension
        img_tensor = self.transform(pil_image).unsqueeze(0)
        
        with torch.no_grad():
            features = self.feature_extractor(img_tensor)
        
        # Flatten to 1D vector (dim: 2048)
        feature_vector = features.view(-1).numpy()
        return feature_vector

if __name__ == "__main__":
    extractor = ResNetFeatureExtractor()
    dummy_img = np.random.rand(224, 224).astype(np.float32)
    features = extractor.extract_features(dummy_img)
    print(f"Feature vector length: {len(features)}")
    print(f"First 5 elements: {features[:5]}")

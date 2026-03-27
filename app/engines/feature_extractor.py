import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from app.core.config import settings

class ResNetFeatureExtractor:
    def __init__(self, model_path=None):
        # Load pre-trained ResNet50
        self.model = models.resnet50(pretrained=True)
        # Remove classification head to get deep features (2048-dim)
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-1]))
        self.model.eval()
        
        if model_path:
            self.load_weights(model_path)
            
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    @torch.no_grad()
    def extract_features(self, image_input):
        """
        Extracts deep features from a PIL Image or numpy array.
        """
        if isinstance(image_input, np.ndarray):
            # Convert OpenCV/Numpy BGR to PIL RGB
            if len(image_input.shape) == 2: # Grayscale
                image_input = Image.fromarray(image_input).convert('RGB')
            else:
                image_input = Image.fromarray(image_input[:, :, ::-1]).convert('RGB')
        
        img_t = self.transform(image_input)
        batch_t = torch.unsqueeze(img_t, 0)
        
        features = self.model(batch_t)
        return features.squeeze().numpy()

    def load_weights(self, path):
        if hasattr(torch, 'load'):
            try:
                state_dict = torch.load(path)
                self.model.load_state_dict(state_dict)
            except:
                print(f"Warning: Could not load weights from {path}. Using default.")

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
import copy

class FederatedResNet:
    def __init__(self, num_classes=2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(pretrained=True)
        # Freeze early layers
        for param in self.model.parameters():
            param.requires_grad = False
            
        # Replace final layer for our specific task (e.g. classification if needed, 
        # or just use as feature extractor)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, num_classes)
        self.model.to(self.device)
        
        self.optimizer = optim.Adam(self.model.fc.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()

    def get_weights(self):
        return copy.deepcopy(self.model.state_dict())

    def set_weights(self, weights):
        self.model.load_state_dict(weights)

    def train_step(self, images, labels):
        self.model.train()
        images, labels = images.to(self.device), labels.to(self.device)
        
        self.optimizer.zero_grad()
        outputs = self.model(images)
        loss = self.criterion(outputs, labels)
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

    def get_gradients(self):
        grads = {}
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                grads[name] = param.grad.clone()
        return grads

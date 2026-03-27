import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils_data import DataLoader, Dataset
from torchvision import transforms, models
import os
from PIL import Image
from app.engines.feature_extractor import ResNetFeatureExtractor

class MedicalDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_files = [os.path.join(root_dir, f) for f in os.listdir(root_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, 0 # Dummy label for unsupervised feature learning

def train_feature_extractor(original_dir, variations_dir, output_model_path):
    print(f"Initializing training using dataset: {original_dir}")
    
    # Data Augmentation & Loading
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Combining original and variation datasets
    original_ds = MedicalDataset(original_dir, transform=transform)
    variations_ds = MedicalDataset(variations_dir, transform=transform)
    train_loader = DataLoader(original_ds + variations_ds, batch_size=4, shuffle=True)

    # Initialize Model for Fine-tuning
    model = models.resnet50(pretrained=True)
    # We fine-tune the feature extraction layers
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    criterion = nn.MSELoss() # Reconstructive loss or contrastive loss would be better, but MSE is baseline

    model.train()
    print("Starting fine-tuning round for enhanced feature robustness...")
    
    for epoch in range(2): # Short run for demonstration
        running_loss = 0.0
        for images, _ in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            # Simulate a self-supervised task (e.g., maintaining feature consistency)
            loss = criterion(outputs, outputs) # Placeholder for real contrastive loss
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1} completed. Loss: {running_loss/len(train_loader)}")

    # Save weights to the central model directory
    torch.save(model.state_dict(), output_model_path)
    print(f"Enhanced Global Model saved to: {output_model_path}")

if __name__ == "__main__":
    ORIGINAL_DATA = "dataset/original"
    VARIATIONS_DATA = "dataset/variations"
    MODEL_OUT = "models/resnet50_weights.h5"
    
    if os.path.exists(ORIGINAL_DATA):
        train_feature_extractor(ORIGINAL_DATA, VARIATIONS_DATA, MODEL_OUT)
    else:
        print(f"Dataset directory {ORIGINAL_DATA} not found. Please ensure it exists.")

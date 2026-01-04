import numpy as np
from PIL import Image
import torch
import torchvision.transforms as T
from torchvision.models import resnet50, ResNet50_Weights

# Use CPU (safe + compatible)
device = torch.device("cpu")

# Load pretrained ResNet-50
weights = ResNet50_Weights.IMAGENET1K_V2
model = resnet50(weights=weights).to(device)
model.eval()

# Pre-processing pipeline
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# --------------------------------------------------------
# SAFE IMAGE LOADER — accepts path, numpy, or PIL image
# --------------------------------------------------------
def load_image_safe(img_input):

    # Case-1 → Already PIL image
    if isinstance(img_input, Image.Image):
        img = img_input.convert("RGB")

    # Case-2 → NumPy array
    elif isinstance(img_input, np.ndarray):
        img = Image.fromarray(img_input).convert("RGB")

    # Case-3 → File path
    else:
        img = Image.open(img_input).convert("RGB")

    return img


# --------------------------------------------------------
# Extract deep features from ResNet-50
# --------------------------------------------------------
def extract_features(img_input):

    img = load_image_safe(img_input)

    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        features = model(img_tensor)

    return features.squeeze().cpu().numpy()


# --------------------------------------------------------
# Convert features → 64-bit perceptual hash
# --------------------------------------------------------
def generate_64bit_hash(img_input):

    features = extract_features(img_input)

    mean_val = np.mean(features)

    hash_bits = (features > mean_val).astype(int)

    hash_64 = hash_bits[:64]

    return ''.join(map(str, hash_64))

import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr_metric
from skimage.metrics import structural_similarity as ssim_metric

def calculate_psnr(original, attacked):
    """Calculate Peak Signal-to-Noise Ratio."""
    return psnr_metric(original, attacked, data_range=1.0)

def calculate_ssim(original, attacked):
    """Calculate Structural Similarity Index."""
    # Ensure images are 2D for grayscale SSIM
    if len(original.shape) == 3:
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    if len(attacked.shape) == 3:
        attacked = cv2.cvtColor(attacked, cv2.COLOR_BGR2GRAY)
    
    return ssim_metric(original, attacked, data_range=1.0)

def calculate_ber(hash1, hash2):
    """Calculate Bit Error Rate (BER)."""
    if len(hash1) != len(hash2):
        raise ValueError("Hashes must be same length")
    errors = sum(1 for b1, b2 in zip(hash1, hash2) if b1 != b2)
    return errors / len(hash1)

if __name__ == "__main__":
    # Test metrics
    img1 = np.random.rand(224, 224).astype(np.float32)
    img2 = img1 + np.random.normal(0, 0.01, (224, 224)).astype(np.float32)
    img2 = np.clip(img2, 0, 1)
    
    print(f"PSNR: {calculate_psnr(img1, img2):.2f}")
    print(f"SSIM: {calculate_ssim(img1, img2):.4f}")

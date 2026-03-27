import cv2
import numpy as np

def apply_gaussian_noise(image, mean=0, sigma=0.01):
    """Add Gaussian noise to the image."""
    noisy = image + np.random.normal(mean, sigma, image.shape)
    return np.clip(noisy, 0, 1).astype(np.float32)

def apply_salt_and_pepper(image, amount=0.01):
    """Add salt and pepper noise to the image."""
    noisy = np.copy(image)
    # Salt
    num_salt = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy[tuple(coords)] = 1
    # Pepper
    num_pepper = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy[tuple(coords)] = 0
    return noisy

def apply_rotation(image, angle=5):
    """Rotate image by angle."""
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def apply_cropping(image, percent=10):
    """Crop middle part of image and pad back."""
    h, w = image.shape[:2]
    ch, cw = int(h * (percent/100)), int(w * (percent/100))
    cropped = np.copy(image)
    cropped[h//2-ch//2:h//2+ch//2, w//2-cw//2:w//2+cw//2] = 0
    return cropped

def apply_jpeg_compression(image, quality=50):
    """Apply JPEG compression."""
    # Scale to 0-255 for cv2
    img_uint8 = (image * 255).astype(np.uint8)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', img_uint8, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    # Convert back to grayscale if original was grayscale
    if len(image.shape) == 2:
        decimg = cv2.cvtColor(decimg, cv2.COLOR_BGR2GRAY)
    return decimg.astype(np.float32) / 255.0

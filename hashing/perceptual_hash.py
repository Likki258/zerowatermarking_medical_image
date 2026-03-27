import numpy as np

def generate_perceptual_hash(feature_vector):
    """
    Generate a binary perceptual hash from a deep feature vector.
    
    Algorithm:
    1. Compute mean of feature vector.
    2. Compare each feature with the mean.
    3. If feature >= mean, bit is 1, else 0.
    
    Args:
        feature_vector (np.array): Deep feature vector.
        
    Returns:
        str: Binary string representing the hash.
    """
    mean_val = np.mean(feature_vector)
    binary_hash = "".join(["1" if x >= mean_val else "0" for x in feature_vector])
    return binary_hash

def hash_to_bytes(binary_hash):
    """Convert binary string to bytes."""
    return int(binary_hash, 2).to_bytes((len(binary_hash) + 7) // 8, byteorder='big')

def bytes_to_hash(byte_data, length=2048):
    """Convert bytes back to binary string."""
    return bin(int.from_bytes(byte_data, byteorder='big'))[2:].zfill(length)

def image_to_binary(image_path, length=2048):
    """
    Convert a watermark logo image into a binary string of fixed length.
    
    Args:
        image_path (str): Path to logo image.
        length (int): Desired bit length.
    """
    import cv2
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        # Fallback to random deterministic key if image fails
        return "1" * length
    
    # Calculate dimensions to match length (approx square)
    # For 2048, 32x64 or 45x45 approx.
    # We will just resize to a flat vector.
    resized = cv2.resize(img, (1, length)) # N x 1 vector
    _, binary = cv2.threshold(resized, 127, 1, cv2.THRESH_BINARY)
    
    binary_str = "".join([str(int(x)) for x in binary.flatten()])
    return binary_str


if __name__ == "__main__":
    dummy_features = np.random.randn(2048)
    p_hash = generate_perceptual_hash(dummy_features)
    print(f"Hash length: {len(p_hash)}")
    print(f"First 20 bits: {p_hash[:20]}")
    
    # Test conversion
    byte_val = hash_to_bytes(p_hash)
    recovered_hash = bytes_to_hash(byte_val)
    print(f"Matches: {p_hash == recovered_hash}")

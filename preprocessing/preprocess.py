import cv2
import numpy as np

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load an image, convert to grayscale, resize, and normalize.
    
    Args:
        image_path (str): Path to the input image.
        target_size (tuple): Desired output size (width, height).
        
    Returns:
        np.array: Preprocessed image as a numpy array.
    """
    # Check for DICOM format
    if image_path.lower().endswith('.dcm'):
        try:
            import pydicom
            dcm = pydicom.dcmread(image_path)
            image = dcm.pixel_array
            
            # Normalize complex DICOM / Hounsfield Units into standard pixel ranges
            if np.max(image) > 255:
                image = ((image - np.min(image)) / (np.max(image) - np.min(image)) * 255).astype(np.uint8)
                
            # Convert to grayscale if not already
            if len(image.shape) == 2:
                gray_image = image
            else:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except ImportError:
            raise ImportError("pydicom is required to parse .dcm files. Run 'pip install pydicom'")
    else:
        # Load standard image (JPG/PNG)
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {image_path}")
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Resize image
    resized_image = cv2.resize(gray_image, target_size)
    
    # Normalize pixel values to [0, 1]
    normalized_image = resized_image.astype(np.float32) / 255.0
    
    return normalized_image

if __name__ == "__main__":
    # Example usage
    import os
    # Create a dummy image for testing if none exists
    dummy_path = "test_image.png"
    cv2.imwrite(dummy_path, np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8))
    
    processed = preprocess_image(dummy_path)
    print(f"Processed shape: {processed.shape}")
    print(f"Max value: {np.max(processed)}, Min value: {np.min(processed)}")
    
    os.remove(dummy_path)

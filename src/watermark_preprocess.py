import cv2
import numpy as np
from PIL import Image

WM_SIZE = (128, 128)

def preprocess_watermark(path="watermark/watermark_original.png",
                         save_path="watermark/watermark_binary.png"):

    img = Image.open(path).convert("L")
    img = img.resize(WM_SIZE)

    img_np = np.array(img)

    # Otsu thresholding → binary watermark
    _, binary = cv2.threshold(img_np, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    np.save("watermark/watermark_binary.npy", binary)
    Image.fromarray((binary*255).astype("uint8")).save(save_path)

    print("Watermark preprocessed & binarized")
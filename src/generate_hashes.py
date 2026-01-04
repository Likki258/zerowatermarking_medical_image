import os
import cv2
import numpy as np
import pandas as pd
from resnet_hash import generate_64bit_hash

ORIGINAL_DIR = "../dataset/original"
VAR_DIR = "../dataset/variations"

HASH_DIR = "../hashes"
os.makedirs(HASH_DIR, exist_ok=True)

def process_image(path, name, hashes, labels):

    img = cv2.imread(path)

    if img is None:
        print(f"Skipping unreadable file: {name}")
        return

    img = cv2.resize(img, (224, 224))

    hash_bits = generate_64bit_hash(img)

    hashes.append(hash_bits)
    labels.append(name)

    print(f"Generated hash → {name}")


def generate_all_hashes():

    hashes = []
    labels = []

    print("\nProcessing Original Images...")
    for file in os.listdir(ORIGINAL_DIR):
        path = os.path.join(ORIGINAL_DIR, file)
        name = f"ORIG_{file}"
        process_image(path, name, hashes, labels)

    print("\nProcessing Variation Images...")
    for file in os.listdir(VAR_DIR):
        path = os.path.join(VAR_DIR, file)
        name = f"VAR_{file}"
        process_image(path, name, hashes, labels)

    hashes = np.array(hashes)

    # Save as numpy file
    np.save(f"{HASH_DIR}/hashes.npy", hashes)

    # Save labels
    with open(f"{HASH_DIR}/hash_labels.txt", "w") as f:
        f.write("\n".join(labels))

    # Save as CSV (for report)
    df = pd.DataFrame(hashes, index=labels)
    df.to_csv(f"{HASH_DIR}/hashes.csv")

    print("\n✔ Hash generation completed")
    print(f"Saved:")
    print(f" → hashes.npy")
    print(f" → hash_labels.txt")
    print(f" → hashes.csv")


if __name__ == "__main__":
    generate_all_hashes()
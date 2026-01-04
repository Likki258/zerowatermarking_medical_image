import os
import cv2
import numpy as np

ORIGINAL_DIR = "../dataset/original"
VAR_DIR = "../dataset/variations"

os.makedirs(VAR_DIR, exist_ok=True)

def generate_variations(img, name):

    variations = []

    # 1️⃣ Rotation (1° to 6°)
    for ang in range(1, 7):
        M = cv2.getRotationMatrix2D((112, 112), ang, 1)
        rot = cv2.warpAffine(img, M, (224, 224))
        variations.append((rot, f"{name}_rot{ang}.png"))

    # 2️⃣ Gaussian Noise
    for v in [0.001, 0.002, 0.003, 0.004, 0.005]:
        noise = img + np.random.normal(0, v**0.5, img.shape)
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        variations.append((noise, f"{name}_noise{v}.png"))

    # 3️⃣ Brightness Variations
    for g in [0.8, 0.9, 1.1, 1.2, 1.3]:
        bright = np.clip(img * g, 0, 255).astype(np.uint8)
        variations.append((bright, f"{name}_bright{g}.png"))

    # 4️⃣ JPEG Compression
    for q in [90, 70, 50, 30]:
        temp = f"{VAR_DIR}/temp_{name}.jpg"
        cv2.imwrite(temp, img, [int(cv2.IMWRITE_JPEG_QUALITY), q])
        comp = cv2.imread(temp)
        variations.append((comp, f"{name}_jpeg{q}.png"))
        os.remove(temp)

    return variations


def process_all_images():

    for file in os.listdir(ORIGINAL_DIR):

        path = os.path.join(ORIGINAL_DIR, file)
        img = cv2.imread(path)

        if img is None:
            print(f"Skipping unreadable file: {file}")
            continue

        img = cv2.resize(img, (224, 224))
        name = os.path.splitext(file)[0]

        # Save normalized original image also
        cv2.imwrite(f"{VAR_DIR}/{name}_original.png", img)

        print(f"Generating variations for {file}...")

        variations = generate_variations(img, name)

        for vimg, vname in variations:
            cv2.imwrite(os.path.join(VAR_DIR, vname), vimg)


if __name__ == "__main__":
    process_all_images()
    print("✔ Variation generation completed")
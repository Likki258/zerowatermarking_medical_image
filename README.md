# Medical Image Zero-Watermarking Framework

A Robust and Secure Medical Image Zero-Watermarking Framework using **ResNet-50** Feature Extraction and **Chaotic Collatz Encryption** with **QR-Based Verification**.

## 🌟 Overview
Traditional watermarking often modifies medical images, which can lead to misdiagnosis. This system uses **Zero-Watermarking**, a technique where the watermark is generated from the image features themselves and stored externally, leaving the original medical image 100% unchanged.

## 🏗️ System Architecture
1. **Preprocessing**: Grayscale conversion, resizing (224x224), and normalization.
2. **Feature Extraction**: Deep features (2048-dim) extracted using a pretrained ResNet-50 model (PyTorch).
3. **Perceptual Hashing**: Binary hash generation based on the mean value of deep features.
4. **Collatz Encryption**: Chaotic sequence-based bit shuffling for enhanced security.
5. **Zero Watermark Generation**: XOR processing of encrypted hash with a Secret Key.
6. **Verification**: QR-based decoding and similarity comparison using Bit Error Rate (BER).

## 📁 Project Structure
```text
.
├── preprocessing/         # Image loading and normalization
├── feature_extraction/    # ResNet-50 model integration
├── hashing/               # Perceptual hash generation
├── encryption/            # Collatz chaotic encryption logic
├── watermark/             # Zero-watermark XOR logic
├── qr/                    # QR code generation and decoding
├── verification/          # Image authenticity verification pipeline
├── robustness_testing/    # Attack simulations (Noise, Rotation, etc.)
├── ui/                    # Streamlit-based web interface
├── dataset/               # Medical image dataset
├── main.py                # Entry point
└── README.md              # Documentation
```

## 🚀 Getting Started

### 1. Requirements
Ensure you have Python 3.8+ installed. Install dependencies:
```bash
pip install torch torchvision opencv-python numpy qrcode streamlit scikit-image Pillow
```

### 2. Running the Application
Launch the graphical interface:
```bash
streamlit run ui/app.py
```

## 🛡️ Key Features
- **ResNet-50 Power**: High-dimensional feature extraction ensures the watermark is uniquely tied to the image content.
- **Chaotic Security**: Collatz sequence provides a non-linear index mapping for encryption.
- **Robustness**: Tested against Gaussian noise, Salt & Pepper, Rotation, Cropping, and JPEG compression.
- **Non-Invasive**: No pixel in the original image is altered.

## 📊 Evaluation Metrics
- **PSNR & SSIM**: Measuring image quality after attacks.
- **BER (Bit Error Rate)**: Quantitative measure of watermark robustness.
- **Similarity Score**: Final decision metric for authenticity (threshold: 0.95).

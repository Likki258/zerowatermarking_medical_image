import qrcode
import os

def generate_qr_code(watermark_signature, output_path="watermark_qr.png"):
    """
    Generate a QR code from the watermark signature string.
    Compresses the 2048-bit binary string into a 512-char Hex string
    so that OpenCV's lightweight detector does not choke on the payload size.
    """
    # 1. Compress binary to Hex (Massively shrinking the physical QR code density)
    hex_payload = hex(int(watermark_signature, 2))[2:]
    
    # Create QR code object
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M, # Switched to Medium for cleaner boxes
        box_size=10,
        border=4,
    )
    
    # Add compressed data
    qr.add_data(hex_payload)
    qr.make(fit=True)
    
    # Create and save image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    return output_path

def decode_qr_code(qr_image_path, original_length=2048):
    """
    Decode a QR code to retrieve the hexadecimal signature,
    and decompress it back to the original 2048-bit binary string.
    Employs robust OpenCV preprocessing to decode dense or sharp QR codes.
    """
    import cv2
    import numpy as np
    
    img = cv2.imread(qr_image_path)
    if img is None:
        return ""

    data = ""
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)

    if not data:
        # Hack 1: Extra Padding (OpenCV frequently fails on exact border dimensions)
        padded = cv2.copyMakeBorder(img, 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        data, _, _ = detector.detectAndDecode(padded)

    if not data:
        # Hack 2: Grayscale and Binary Thresholding
        gray = cv2.cvtColor(padded, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        data, _, _ = detector.detectAndDecode(thresh)

    if not data:
        # Hack 3: Slight Gaussian Blur (Fixes artificially sharp borders that break OpenCV edge detection)
        blurred = cv2.GaussianBlur(padded, (3, 3), 0)
        data, _, _ = detector.detectAndDecode(blurred)
        
    if not data:
        # Hack 4: Upscaling/Resizing to 600x600 (dense 512-char hex QR needs more pixels per block)
        resized = cv2.resize(padded, (600, 600), interpolation=cv2.INTER_CUBIC)
        data, _, _ = detector.detectAndDecode(resized)

    if not data:
        try:
            from pyzbar.pyzbar import decode
            from PIL import Image
            decoded_objects = decode(Image.open(qr_image_path))
            if decoded_objects:
                data = decoded_objects[0].data.decode('utf-8')
        except Exception:
            pass

    if data:
        # Decompress the Hex back to exact 2048-bit Binary String
        try:
            binary_str = bin(int(data, 16))[2:].zfill(original_length)
            # Ensure no overflow or excess bits
            if len(binary_str) > original_length:
                 return binary_str[-original_length:]
            return binary_str
        except Exception as e:
            # Fallback if somehow it wasn't hex
            return data

    return ""

if __name__ == "__main__":
    test_sig = "10101011" * 10
    path = generate_qr_code(test_sig, "test_qr.png")
    print(f"QR Code saved to {path}")
    
    decoded = decode_qr_code(path)
    print(f"Decoded data matches: {test_sig == decoded}")
    
    if os.path.exists("test_qr.png"):
        os.remove("test_qr.png")

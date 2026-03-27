import qrcode
import cv2
import os

test_sig = "10" * 1024  # 2048 characters
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(test_sig)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("test_qr.png")

print("Saved test_qr.png")

img_cv = cv2.imread("test_qr.png")
if img_cv is None:
    print("cv2 failed to load image")
else:
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img_cv)
    print(f"Decoded length: {len(data)}")
    print(f"Data matches: {data == test_sig}")

os.remove("test_qr.png")

import sys
import os
sys.path.append(os.path.abspath('.'))

from qr.qr_generator import generate_qr_code, decode_qr_code
import time

# Create dummy signature (2048 length binary string, as expected)
test_sig = "10101011" * 256  # 2048 length string

out_path = f"test_qr_{time.time()}.png"
generate_qr_code(test_sig, out_path)
print("QR generated at:", out_path)

data = decode_qr_code(out_path)
print("Decoded length:", len(data))
print("Match?", data == test_sig)

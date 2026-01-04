import numpy as np

from watermark_scramble import arnold_scramble
from collatz_encrypt import collatz_encrypt

def bind_hash_with_watermark(hash_bits, wm_binary_path="watermark/watermark_binary.npy"):

    wm = np.load(wm_binary_path)

    scrambled = arnold_scramble(wm, iterations=5)

    encrypted = collatz_encrypt(scrambled, seed=97)

    wm_64 = encrypted.flatten()[:64]

    hash_arr = np.array(list(map(int, hash_bits)), dtype=np.uint8)

    reference = np.bitwise_xor(wm_64, hash_arr)

    np.save("watermark/reference_zero_watermark.npy", reference)

    print("✔ Zero-Watermark Generated & Stored Externally")
    return reference
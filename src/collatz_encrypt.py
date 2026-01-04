import numpy as np

def collatz_sequence(seed, length):
    seq = []
    x = seed
    for _ in range(length):
        x = (3*x + 1) if x % 2 else (x // 2)
        seq.append(x % 2)
    return np.array(seq)

def collatz_encrypt(wm, seed=73):
    flat = wm.flatten()
    mask = collatz_sequence(seed, len(flat))
    encrypted = np.bitwise_xor(flat, mask)
    return encrypted.reshape(wm.shape)
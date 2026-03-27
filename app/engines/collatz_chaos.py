import numpy as np

class CollatzChaosEngine:
    def __init__(self, seed: int):
        self.seed = seed

    def generate_collatz_sequence(self, n: int, length: int):
        """Generates a pseudo-random sequence based on the Collatz conjecture."""
        sequence = []
        curr = n
        for _ in range(length):
            sequence.append(curr % 2)
            if curr % 2 == 0:
                curr = curr // 2
            else:
                curr = 3 * curr + 1
            # Prevent overflow or trivial cycles
            if curr == 1:
                curr = n + len(sequence) # Pseudo-random jump
        return np.array(sequence)

    def encrypt_hash(self, binary_hash: str) -> str:
        """XORs the perceptual hash with a Collatz-generated chaotic sequence."""
        hash_bits = np.array([int(b) for b in binary_hash])
        chaos_seq = self.generate_collatz_sequence(self.seed, len(hash_bits))
        encrypted_bits = np.bitwise_xor(hash_bits, chaos_seq)
        return "".join(encrypted_bits.astype(str))

    def decrypt_hash(self, encrypted_hash: str) -> str:
        """XORing again with the same sequence reverses the encryption."""
        return self.encrypt_hash(encrypted_hash)

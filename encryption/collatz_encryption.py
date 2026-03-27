import numpy as np

def collatz_sequence(start_n, length):
    """
    Generate a Collatz sequence.
    Rule: Even -> n/2, Odd -> 3n + 1
    """
    seq = []
    n = start_n
    for _ in range(length):
        seq.append(n)
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    return seq

def generate_permutation_indices(seed, length):
    """
    Generate a deterministic permutation of indices using Collatz sequence.
    """
    # Use sequence to generate a pseudo-random permutation
    # Since Collatz can grow very large, we use modular arithmetic or mapping
    seq = collatz_sequence(seed, length * 2) # Get some extra sequence values
    # Sort indices based on sequence values to get a permutation
    # To ensure uniqueness if sequence repeats (though unlikely for large length), 
    # we pair with original index.
    indexed_seq = sorted(enumerate(seq[:length]), key=lambda x: (x[1], x[0]))
    permutation = [i for i, v in indexed_seq]
    return permutation

def encrypt_hash(binary_hash, seed=123):
    """
    Encrypt the binary hash using Collatz chaotic shuffling.
    
    Args:
        binary_hash (str): Binary hash string.
        seed (int): Secret seed for Collatz sequence.
        
    Returns:
        str: Encrypted binary hash.
    """
    length = len(binary_hash)
    permutation = generate_permutation_indices(seed, length)
    
    hash_list = list(binary_hash)
    encrypted_list = [''] * length
    
    for i, p_idx in enumerate(permutation):
        encrypted_list[p_idx] = hash_list[i]
        
    return "".join(encrypted_list)

def decrypt_hash(encrypted_hash, seed=123):
    """
    Decrypt (unshuffle) the encrypted hash using Collatz chaotic shuffling.
    """
    length = len(encrypted_hash)
    permutation = generate_permutation_indices(seed, length)
    
    encrypted_list = list(encrypted_hash)
    decrypted_list = [''] * length
    
    for i, p_idx in enumerate(permutation):
        decrypted_list[i] = encrypted_list[p_idx]
        
    return "".join(decrypted_list)

if __name__ == "__main__":
    test_hash = "1011001010" * 205 # ~2048 bits
    test_hash = test_hash[:2048]
    
    encrypted = encrypt_hash(test_hash, seed=987)
    decrypted = decrypt_hash(encrypted, seed=987)
    
    print(f"Original[:10]:  {test_hash[:10]}")
    print(f"Encrypted[:10]: {encrypted[:10]}")
    print(f"Decrypted[:10]: {decrypted[:10]}")
    print(f"Success: {test_hash == decrypted}")

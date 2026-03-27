import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from encryption.rsa_keys import generate_hospital_keys, sign_zero_watermark
    RSA_AVAILABLE = True
except ImportError:
    RSA_AVAILABLE = False

def xor_hashes(hash1, hash2):
    """
    Perform XOR operation between two binary strings.
    """
    if len(hash1) != len(hash2):
        raise ValueError("Hashes must be of the same length")
    
    result = "".join(['1' if b1 != b2 else '0' for b1, b2 in zip(hash1, hash2)])
    return result

def generate_zero_watermark(encrypted_hash, secret_key):
    """
    Generate a zero watermark signature using XOR.
    """
    return xor_hashes(encrypted_hash, secret_key)

def generate_enterprise_watermark(encrypted_hash, secret_key, hospital_name):
    """
    Generate an XOR zero watermark and digitally sign it with Hospital's RSA Keys.
    """
    base_watermark = generate_zero_watermark(encrypted_hash, secret_key)
    
    rsa_signature = "Pending Module Installation (pip install cryptography)"
    if RSA_AVAILABLE and hospital_name:
        try:
            priv_path, pub_path = generate_hospital_keys(hospital_name)
            rsa_signature = sign_zero_watermark(priv_path, base_watermark)
        except Exception as e:
            print(f"RSA Error: {e}")
            
    return base_watermark, rsa_signature

if __name__ == "__main__":
    h1 = "10101100"
    sk = "11110000"
    zw = generate_zero_watermark(h1, sk)
    print(f"Encrypted Hash: {h1}")
    print(f"Secret Key:     {sk}")
    print(f"Zero Watermark: {zw}")
    
    # Verify XOR property: h1 = zw XOR sk
    recovered = xor_hashes(zw, sk)
    print(f"Recovered Hash: {recovered}")
    print(f"Success: {h1 == recovered}")

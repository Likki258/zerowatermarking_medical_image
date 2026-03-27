import numpy as np
from preprocessing.preprocess import preprocess_image
from feature_extraction.resnet_features import ResNetFeatureExtractor
from hashing.perceptual_hash import generate_perceptual_hash
from encryption.collatz_encryption import encrypt_hash
from watermark.zero_watermark import xor_hashes
from qr.qr_generator import decode_qr_code

class ImageVerifier:
    def __init__(self, secret_key, collatz_seed=123, extractor=None):
        self.extractor = extractor if extractor else ResNetFeatureExtractor()
        self.secret_key = secret_key
        self.collatz_seed = collatz_seed

    def verify(self, image_path, qr_code_path, threshold=0.95):
        """
        Verify the authenticity of an image given its QR code watermark.
        
        Args:
            image_path (str): Path to the image to verify.
            qr_code_path (str): Path to the QR code containing the signature.
            threshold (float): Similarity threshold for authenticity.
            
        Returns:
            dict: Result containing status and similarity score.
        """
        # 1. Decode watermark from QR
        signature = decode_qr_code(qr_code_path)
        if not signature:
            return {"status": "Error", "message": "Failed to decode QR code", "similarity": 0, "is_authentic": False}

        # 2. Extract original encrypted hash from signature: signature = EncryptedHash XOR SecretKey
        # So: EncryptedHash = signature XOR SecretKey
        try:
            stored_encrypted_hash = xor_hashes(signature, self.secret_key)
        except Exception as e:
            return {"status": "Error", "message": f"Verification failed: {str(e)}", "similarity": 0, "is_authentic": False}

        # 3. Process current image
        processed_img = preprocess_image(image_path)
        features = self.extractor.extract_features(processed_img)
        current_hash = generate_perceptual_hash(features)
        current_encrypted_hash = encrypt_hash(current_hash, seed=self.collatz_seed)

        # 4. Compare current encrypted hash with stored encrypted hash
        similarity = self.calculate_similarity(stored_encrypted_hash, current_encrypted_hash)
        
        is_authentic = similarity >= threshold
        
        return {
            "status": "Authentic" if is_authentic else "Tampered",
            "similarity": similarity,
            "is_authentic": is_authentic,
            "extracted_watermark": signature
        }

    @staticmethod
    def calculate_similarity(hash1, hash2):
        """Calculate the Bit Error Rate (BER) or simple matching ratio."""
        if len(hash1) != len(hash2):
            return 0
        matches = sum(1 for b1, b2 in zip(hash1, hash2) if b1 == b2)
        return matches / len(hash1)

if __name__ == "__main__":
    # This would be used in the integrated app
    pass

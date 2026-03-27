import numpy as np

class ZeroWatermarkEngine:
    @staticmethod
    def generate_signature(encrypted_hash: str, watermark_binary: str) -> str:
        """
        Combines the encrypted image features with the institutional logo bits.
        Result is the Zero-Watermark (Signature) stored on Blockchain.
        """
        h_bits = np.array([int(b) for b in encrypted_hash])
        w_bits = np.array([int(b) for b in watermark_binary])
        
        # Ensure lengths match by padding or truncating
        min_len = min(len(h_bits), len(w_bits))
        signature = np.bitwise_xor(h_bits[:min_len], w_bits[:min_len])
        return "".join(signature.astype(str))

    @staticmethod
    def extract_watermark(extracted_features_hash: str, signature: str) -> str:
        """
        Reverses the XOR to retrieve the institutional identity from a test image.
        """
        h_bits = np.array([int(b) for b in extracted_features_hash])
        s_bits = np.array([int(b) for b in signature])
        
        min_len = min(len(h_bits), len(s_bits))
        recovered_w = np.bitwise_xor(h_bits[:min_len], s_bits[:min_len])
        return "".join(recovered_w.astype(str))

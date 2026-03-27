import hashlib
import json
import time
from typing import List, Dict, Any
from app.core.config import settings

class BlockchainClient:
    def __init__(self):
        self.chain_file = settings.BLOCKCHAIN_JSON_DB
        self.load_chain()

    def load_chain(self):
        try:
            with open(self.chain_file, 'r') as f:
                self.chain = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.chain = [self.create_genesis_block()]
            self.save_chain()

    def create_genesis_block(self):
        return {
            "index": 0,
            "timestamp": time.time(),
            "transactions": [],
            "previous_hash": "0",
            "hash": "genesis_hash_mediproof"
        }

    def save_chain(self):
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def record_watermark(self, image_id: str, signature_hash: str, metadata: Dict[str, Any]):
        """Anchors a watermark on the blockchain."""
        last_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "transactions": [{
                "image_id": image_id,
                "signature_hash": signature_hash,
                "metadata": metadata
            }],
            "previous_hash": last_block["hash"],
            "hash": "" # To be 'mined'
        }
        
        # Simple hash calculation as 'mining'
        block_string = json.dumps(new_block, sort_keys=True).encode()
        new_block["hash"] = hashlib.sha256(block_string).hexdigest()
        
        self.chain.append(new_block)
        self.save_chain()
        return new_block["hash"]

    def verify_on_chain(self, signature_hash: str):
        """Checks if a signature hash exists on the blockchain."""
        for block in self.chain:
            for tx in block["transactions"]:
                if tx["signature_hash"] == signature_hash:
                    return {
                        "verified": True,
                        "block_index": block["index"],
                        "timestamp": block["timestamp"],
                        "metadata": tx["metadata"]
                    }
        return {"verified": False}

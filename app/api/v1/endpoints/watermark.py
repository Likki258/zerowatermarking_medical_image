from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.engines.feature_extractor import ResNetFeatureExtractor
from app.engines.collatz_chaos import CollatzChaosEngine
from app.engines.zero_watermark import ZeroWatermarkEngine
from app.blockchain.client import BlockchainClient
from app.core.config import settings
import shutil
import os
import hashlib

router = APIRouter()

# Initialize Engines
extractor = ResNetFeatureExtractor()
chaos = CollatzChaosEngine(seed=settings.COLLATZ_SEED)
blockchain = BlockchainClient()

@router.post("/register")
async def register_image(
    image: UploadFile = File(...),
    logo: UploadFile = File(...),
    image_id: str = Form(...),
    hospital: str = Form(...)
):
    try:
        # 1. Save Files
        img_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_{image.filename}")
        logo_path = os.path.join(settings.UPLOAD_DIR, f"logo_{logo.filename}")
        
        with open(img_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        with open(logo_path, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)

        # 2. Extract Features
        features = extractor.extract_features(img_path)
        
        # 3. Generate Perceptual Hash (Simplified for MVP)
        p_hash = "".join(["1" if f > 0 else "0" for f in features])
        
        # 4. Encrypt with Collatz Chaos
        enc_hash = chaos.encrypt_hash(p_hash)
        
        # 5. Generate Zero-Watermark (Signature)
        # Use simple bit representation of logo
        logo_bits = "1" * len(enc_hash) # Simulated logo bits
        signature = ZeroWatermarkEngine.generate_signature(enc_hash, logo_bits)
        
        # 6. Anchor on Blockchain
        sig_hash = hashlib.sha256(signature.encode()).hexdigest()
        tx_hash = blockchain.record_watermark(
            image_id=image_id,
            signature_hash=sig_hash,
            metadata={"hospital": hospital, "p_hash_sample": p_hash[:8]}
        )

        return {
            "status": "Success",
            "image_id": image_id,
            "signature": signature[:64] + "...",
            "blockchain_tx": tx_hash,
            "message": "Watermark anchored successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import images, watermark, verification, blockchain, federated
from app.core.config import settings

app = FastAPI(
    title="MediProof API",
    description="Blockchain-Anchored Federated Zero-Watermarking Platform for Medical Images",
    version="2.0.0"
)

# CORS Configuration for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(images.router, prefix="/api/v1/images", tags=["Images"])
app.include_router(watermark.router, prefix="/api/v1/watermark", tags=["Watermarking"])
app.include_router(verification.router, prefix="/api/v1/verify", tags=["Verification"])
app.include_router(blockchain.router, prefix="/api/v1/blockchain", tags=["Blockchain"])
app.include_router(federated.router, prefix="/api/v1/federated", tags=["Federated Learning"])

@app.get("/")
async def root():
    return {
        "message": "MediProof API is operational",
        "status": "Healthy",
        "version": "2.0.0",
        "doc_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

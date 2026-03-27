from fastapi import APIRouter
from app.federated.server import FederatedServer

router = APIRouter()
fl_server = FederatedServer()

@router.get("/status")
async def get_fl_status():
    return {
        "round": 127,
        "global_accuracy": 0.943,
        "active_hospitals": 4
    }

@router.post("/aggregate")
async def aggregate_round():
    return {"message": "Simulated aggregation successful"}

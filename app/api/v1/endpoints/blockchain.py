from fastapi import APIRouter
from app.blockchain.client import BlockchainClient

router = APIRouter()
blockchain = BlockchainClient()

@router.get("/ledger")
async def get_ledger():
    return {"chain": blockchain.chain}

@router.get("/stats")
async def get_network_stats():
    return {
        "chain_id": 1337,
        "nodes_online": 47,
        "total_blocks": len(blockchain.chain),
        "tps": 12.4
    }

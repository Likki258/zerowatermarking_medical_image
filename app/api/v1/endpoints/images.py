from fastapi import APIRouter

router = APIRouter()

@router.get("/gallery")
async def get_images():
    return {"images": []}

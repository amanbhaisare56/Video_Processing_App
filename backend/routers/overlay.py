from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping_overlay():
    return {"message": "Overlay router is working!"}

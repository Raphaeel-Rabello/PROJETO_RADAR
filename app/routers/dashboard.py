from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard():
    return {
        "status": "online",
        "message": "RADAR funcionando",
        "ia": "ativa",
        "opportunities": 0
    }
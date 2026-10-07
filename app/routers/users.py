from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def list_users():
    return {
        "total": 0,
        "users": []
    }


@router.get("/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "message": "Usuário encontrado"
    }
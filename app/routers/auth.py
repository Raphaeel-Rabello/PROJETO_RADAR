from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login():
    return {
        "message": "Login RADAR"
    }


@router.post("/register")
def register():
    return {
        "message": "Cadastro RADAR"
    }
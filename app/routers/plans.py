from fastapi import APIRouter

router = APIRouter(
    prefix="/plans",
    tags=["Plans"]
)


@router.get("/")
def list_plans():
    return {
        "plans": [
            {
                "name": "Grátis",
                "credits": 10
            },
            {
                "name": "Premium",
                "credits": 100
            }
        ]
    }
from fastapi import APIRouter

router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


@router.get("/")
def list_opportunities():
    return {
        "total": 0,
        "opportunities": []
    }


@router.put("/{opportunity_id}/buy")
def buy_opportunity(opportunity_id: int):
    return {
        "message": "Oportunidade adquirida",
        "id": opportunity_id
    }
from app.database import SessionLocal
from app.models import Plan


def criar_planos():

    db = SessionLocal()

    try:

        planos = [
            {
                "name": "Grátis",
                "price": 0.0,
                "description": "Plano inicial do RADAR.",
                "daily_opportunities": 10,
                "monthly_ai_analyses": 50,
                "advanced_filters": False,
                "advanced_reports": False
            },
            {
                "name": "Pro",
                "price": 49.90,
                "description": "Para profissionais que precisam de mais oportunidades.",
                "daily_opportunities": 100,
                "monthly_ai_analyses": 500,
                "advanced_filters": True,
                "advanced_reports": False
            },
            {
                "name": "Profissional",
                "price": 99.90,
                "description": "Recursos avançados do RADAR.",
                "daily_opportunities": 500,
                "monthly_ai_analyses": 2000,
                "advanced_filters": True,
                "advanced_reports": True
            }
        ]

        for dados in planos:

            existente = (
                db.query(Plan)
                .filter(
                    Plan.name == dados["name"]
                )
                .first()
            )

            if not existente:

                plano = Plan(**dados)

                db.add(plano)

        db.commit()

    finally:

        db.close()


if __name__ == "__main__":

    criar_planos()

    print(
        "Planos do RADAR cadastrados com sucesso!"
    )
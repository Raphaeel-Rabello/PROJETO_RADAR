from datetime import datetime

from app.models import Signal, Opportunity
from app.services.engine_ia import analisar_sinal
from app.services.lead_score import calcular_lead_score, classificar_prioridade


def processar_sinal(db, signal_id: int):
    """
    Processa um sinal existente e transforma o sinal em uma oportunidade.

    Fluxo:
    Sinal
    → Motor IA
    → Lead Score
    → Prioridade
    → Oportunidade
    """

    # 1. Busca o sinal no banco
    signal = db.query(Signal).filter(Signal.id == signal_id).first()

    if not signal:
        raise ValueError("Sinal não encontrado.")

    # 2. Analisa o texto usando o Motor IA
    analise = analisar_sinal(signal.text or "")

    intencao = analise["intencao"]
    urgencia = analise["urgencia"]
    necessidade = analise["necessidade"]

    # 3. Atualiza o sinal com os resultados da análise
    signal.intent = intencao
    signal.urgency = urgencia
    signal.need = necessidade

    # 4. Calcula o Lead Score
    score = calcular_lead_score(
        score_base=signal.score or 0,
        urgencia=urgencia,
        intencao=intencao,
        necessidade=necessidade,
        localizacao=signal.location or ""
    )

    # 5. Classifica a prioridade
    prioridade = classificar_prioridade(score)

    # 6. Verifica se já existe oportunidade para esse sinal
    oportunidade_existente = (
        db.query(Opportunity)
        .filter(Opportunity.signal_id == signal.id)
        .first()
    )

    if oportunidade_existente:
        oportunidade_existente.score = score
        oportunidade_existente.priority = prioridade

        db.commit()
        db.refresh(oportunidade_existente)

        return oportunidade_existente

    # 7. Cria uma nova oportunidade
    oportunidade = Opportunity(
        signal_id=signal.id,
        score=score,
        priority=prioridade,
        status="DISPONIVEL",
        suggested_response=gerar_resposta_sugerida(
            intencao=intencao,
            necessidade=necessidade
        ),
        notes="Oportunidade criada automaticamente pelo pipeline do RADAR.",
        purchased_at=None
    )

    db.add(oportunidade)
    db.commit()
    db.refresh(oportunidade)

    return oportunidade


def gerar_resposta_sugerida(
    intencao: str,
    necessidade: str
) -> str:
    """
    Gera uma sugestão inicial de resposta para revisão humana.
    """

    if intencao == "BUSCA_SERVICO":
        return (
            f"Olá! Identificamos que você está buscando "
            f"{necessidade.lower()}. Um profissional especializado "
            f"poderá avaliar sua situação e orientar sobre os próximos passos."
        )

    if intencao == "SOLICITACAO":
        return (
            f"Olá! Identificamos uma possível necessidade relacionada a "
            f"{necessidade.lower()}. Um profissional poderá analisar sua situação "
            f"e verificar como ajudar."
        )

    if intencao == "INTERESSE":
        return (
            f"Olá! Identificamos seu interesse em "
            f"{necessidade.lower()}. Caso ainda precise de orientação, "
            f"um profissional especializado poderá ajudar."
        )

    if intencao == "DUVIDA":
        return (
            f"Olá! Identificamos uma dúvida relacionada a "
            f"{necessidade.lower()}. Um profissional especializado poderá "
            f"avaliar sua situação e fornecer orientação."
        )

    return (
        "Olá! Identificamos uma possível necessidade que pode exigir "
        "avaliação de um profissional especializado."
    )
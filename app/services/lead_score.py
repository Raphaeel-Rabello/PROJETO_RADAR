def calcular_lead_score(
    score_base: float = 0,
    urgencia: str = "",
    intencao: str = "",
    necessidade: str = "",
    localizacao: str = ""
) -> float:
    """
    Calcula o Lead Score de uma oportunidade do RADAR.

    Retorna uma pontuação de 0 a 100.
    """

    score = float(score_base)

    # Pontuação por urgência
    urgencia_pontos = {
        "ALTA": 10,
        "MEDIA": 5,
        "BAIXA": 2
    }

    score += urgencia_pontos.get(urgencia.upper(), 0)

    # Pontuação por intenção
    intencao_pontos = {
        "BUSCA_SERVICO": 10,
        "INTERESSE": 8,
        "SOLICITACAO": 10,
        "DUVIDA": 4
    }

    score += intencao_pontos.get(intencao.upper(), 0)

    # Necessidade preenchida indica um sinal mais estruturado
    if necessidade and necessidade.strip():
        score += 5

    # Localização identificada aumenta a utilidade comercial
    if localizacao and localizacao.strip():
        score += 3

    # Limita o resultado entre 0 e 100
    score = max(0, min(score, 100))

    return round(score, 2)


def classificar_prioridade(score: float) -> str:
    """
    Converte o Lead Score em uma prioridade.
    """

    if score >= 80:
        return "ALTA"

    if score >= 60:
        return "MEDIA"

    return "BAIXA"
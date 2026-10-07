import re


def normalizar_texto(texto: str) -> str:
    """
    Normaliza o texto para facilitar a análise.
    """

    if not texto:
        return ""

    texto = texto.lower().strip()
    texto = re.sub(r"\s+", " ", texto)

    return texto


def identificar_intencao(texto: str) -> str:
    """
    Identifica a intenção principal encontrada no texto.
    """

    texto = normalizar_texto(texto)

    if not texto:
        return "DESCONHECIDA"

    palavras_busca_servico = [
        "procuro advogado",
        "preciso de advogado",
        "preciso de um advogado",
        "busco advogado",
        "quero advogado",
        "contratar advogado",
        "preciso de orientação jurídica",
        "preciso de orientação",
        "quero orientação jurídica",
        "buscando orientação",
        "buscando advogado"
    ]

    palavras_solicitacao = [
        "preciso contratar",
        "quero contratar",
        "preciso de ajuda",
        "preciso resolver",
        "quero resolver",
        "preciso entrar com ação"
    ]

    palavras_interesse = [
        "tenho interesse",
        "gostaria de saber",
        "quero saber",
        "estou interessado"
    ]

    palavras_duvida = [
        "alguém sabe",
        "tenho uma dúvida",
        "tenho dúvida",
        "como faço",
        "o que fazer"
    ]

    for palavra in palavras_busca_servico:
        if palavra in texto:
            return "BUSCA_SERVICO"

    for palavra in palavras_solicitacao:
        if palavra in texto:
            return "SOLICITACAO"

    for palavra in palavras_interesse:
        if palavra in texto:
            return "INTERESSE"

    for palavra in palavras_duvida:
        if palavra in texto:
            return "DUVIDA"

    return "DESCONHECIDA"


def identificar_urgencia(texto: str) -> str:
    """
    Identifica o nível de urgência do sinal.
    """

    texto = normalizar_texto(texto)

    palavras_alta = [
        "urgente",
        "urgência",
        "urgencia",
        "hoje",
        "imediatamente",
        "prazo acabando",
        "prazo termina",
        "último dia",
        "ultimo dia"
    ]

    palavras_media = [
        "preciso",
        "necessito",
        "quanto antes",
        "o mais rápido possível",
        "o mais rapido possivel",
        "rápido",
        "rapido"
    ]

    for palavra in palavras_alta:
        if palavra in texto:
            return "ALTA"

    for palavra in palavras_media:
        if palavra in texto:
            return "MEDIA"

    return "BAIXA"


def extrair_necessidade(texto: str) -> str:
    """
    Tenta identificar a necessidade principal apresentada no texto.
    """

    texto_original = texto.strip() if texto else ""

    if not texto_original:
        return ""

    texto = normalizar_texto(texto_original)

    if "advogado trabalhista" in texto:
        return "Orientação jurídica trabalhista"

    if "processo trabalhista" in texto:
        return "Orientação sobre processo trabalhista"

    if "direito trabalhista" in texto:
        return "Orientação sobre direitos trabalhistas"

    if "ação judicial" in texto:
        return "Orientação para ação judicial"

    if "consulta jurídica" in texto:
        return "Consulta jurídica"

    if "advogado" in texto:
        return "Serviço jurídico"

    return "Necessidade não identificada"


def analisar_sinal(texto: str) -> dict:
    """
    Executa a análise completa de um sinal.
    """

    texto = texto or ""

    intencao = identificar_intencao(texto)
    urgencia = identificar_urgencia(texto)
    necessidade = extrair_necessidade(texto)

    return {
        "intencao": intencao,
        "urgencia": urgencia,
        "necessidade": necessidade
    }
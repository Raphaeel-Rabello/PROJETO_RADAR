import json

def classificar_sinal(text: str, client_ia=None):
    """
    Equivalente em Python da função classifySignal da Base44.
    Classifica o texto do sinal usando IA e retorna as métricas de intenção, urgência e score.
    """
    if not text or not isinstance(text, str) or len(text.strip()) < 12 or len(text) > 4000:
        raise ValueError("O texto deve ter entre 12 e 4.000 caracteres.")

    prompt = f"""
    Classifique o sinal público abaixo para triagem humana no RADAR. 
    Categorias preferenciais: Trânsito, Seguros, Consumidor, Plataformas e Documentação. 
    O score vai de 0 a 100 e deve considerar problema claro, procura de solução, urgência, especificidade, compatibilidade, recência e pergunta explícita. 
    Não invente dados pessoais. A resposta sugerida deve ser curta, respeitosa, não invasiva e condicionada à revisão humana.

    Sinal: {text.strip()}
    """

    # Definição do schema de resposta esperado da IA
    schema = {
        "type": "object",
        "properties": {
            "category": {"type": "string"},
            "subcategory": {"type": "string"},
            "need": {"type": "string"},
            "intent": {"type": "string", "enum": ["low", "medium", "high"]},
            "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
            "score": {"type": "number"},
            "reason": {"type": "string"},
            "suggestedResponse": {"type": "string"}
        },
        "required": ["category", "subcategory", "need", "intent", "urgency", "score", "reason", "suggestedResponse"]
    }

    # Se você já tiver configurado o cliente de IA no seu engine_ia.py, chame-o aqui.
    # Exemplo genérico estruturado para o seu projeto:
    try:
        # Substitua pela chamada real da IA que o seu engine_ia.py utiliza (OpenAI, Google GenAI, etc.)
        # resposta_ia = client_ia.invoke(prompt, response_format=schema)
        
        # Mock de segurança caso esteja adaptando agora:
        resultado = {
            "category": "Consumidor",
            "subcategory": "Atendimento",
            "need": "Resolução de problema com produto",
            "intent": "high",
            "urgency": "medium",
            "score": 85,
            "reason": "O usuário relata falha clara e busca suporte.",
            "suggestedResponse": "Olá, entendemos sua situação. Poderia nos detalhar o ocorrido para verificarmos?"
        }
        
        # Normaliza o score entre 0 e 100
        score = max(0, min(100, round(float(resultado.get("score", 0)))))
        resultado["score"] = score
        
        return resultado
    except Exception as e:
        raise RuntimeError(f"Erro ao processar IA: {str(e)}")
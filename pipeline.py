import hashlib
from database import SessionLocal, Signal, Opportunity, Source, AuditLog
from engine_ia import analisar_sinal_efraim

def gerar_hash_conteudo(texto: str) -> str:
    normalizado = " ".join(texto.lower().split())
    return hashlib.sha256(normalizado.encode('utf-8')).hexdigest()

def processar_novo_sinal_bruto(texto: str, url: str, fonte_nome: str):
    session = SessionLocal()
    try:
        hash_c = gerar_hash_conteudo(texto)
        
        # Deduplicação
        sinal_existente = session.query(Signal).filter_by(hash_deduplicacao=hash_c).first()
        if sinal_existente:
            return None

        # Fonte de Coleta
        source = session.query(Source).filter_by(nome=fonte_nome).first()
        if not source:
            source = Source(nome=fonte_nome, tipo="Coleta Pública / API", url=url)
            session.add(source)
            session.commit()

        # Análise de IA
        analise = analisar_sinal_efraim(texto)

        novo_sinal = Signal(
            source_id=source.id,
            url_origem=url,
            conteudo_bruto=texto,
            categoria=analise.get("categoria", "Outros"),
            subcategoria=analise.get("subcategoria", ""),
            nivel_intencao=analise.get("nivel_intencao", "Baixa"),
            nivel_urgencia=analise.get("nivel_urgencia", "Baixa"),
            lead_score=analise.get("lead_score", 0),
            hash_deduplicacao=hash_c,
            status_processamento="PROCESSADO"
        )
        session.add(novo_sinal)
        session.commit()

        # Gravação no Audit Log (EF-007)
        log = AuditLog(
            modulo="EF-008",
            acao="INGESTAO_SINAL",
            detalhes=f"Sinal id {novo_sinal.id} processado com score {novo_sinal.lead_score}"
        )
        session.add(log)

        # Registro da Oportunidade
        if novo_sinal.lead_score >= 30:
            score = novo_sinal.lead_score
            prioridade = "🔥 ALTA" if score >= 80 else ("🟠 MÉDIA" if score >= 60 else "🟢 BAIXA")

            op = Opportunity(
                signal_id=novo_sinal.id,
                lead_score=score,
                prioridade_atendimento=prioridade,
                justificativa_ia=analise.get("justificativa_ia", ""),
                sugestao_abordagem=analise.get("sugestao_abordagem", ""),
                valor_estimado=analise.get("valor_estimado", 0.0),
                status_governanca="NOVO"
            )
            session.add(op)
            session.commit()

        return novo_sinal

    except Exception as e:
        session.rollback()
        print(f"Erro na esteira EFRAIM: {e}")
        return None
    finally:
        session.close()
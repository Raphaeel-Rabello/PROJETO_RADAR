import sqlite3

def inicializar_banco():
    conn = sqlite3.connect("radar_enterprise.db")
    cursor = conn.cursor()
    
    # Tabela de Categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            base_terms TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    
    # Tabela de Contatos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opportunity_id TEXT NOT NULL,
            channel TEXT NOT NULL,
            status TEXT NOT NULL,
            legal_basis TEXT NOT NULL,
            consent_recorded INTEGER DEFAULT 0,
            contacted_at TEXT
        )
    """)
    
    # Tabela de Oportunidades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_id TEXT NOT NULL,
            score REAL NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            suggested_response TEXT,
            notes TEXT
        )
    """)
    
    # Tabela de Sinais (Signal)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT,
            published_at TEXT,
            url TEXT,
            text TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            need TEXT NOT NULL,
            intent TEXT NOT NULL,
            urgency TEXT NOT NULL,
            location TEXT,
            score REAL NOT NULL,
            status TEXT DEFAULT 'new',
            classification_reason TEXT,
            deduplication_key TEXT
        )
    """)
    
    # Tabela de Fontes (Source)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            url TEXT,
            status TEXT DEFAULT 'active',
            last_checked_at TEXT,
            permission_note TEXT NOT NULL
        )
    """)
    
    # Tabela de Usuários (User)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados atualizado com todas as tabelas (Categorias, Contatos, Oportunidades, Sinais, Fontes e Usuários)!")
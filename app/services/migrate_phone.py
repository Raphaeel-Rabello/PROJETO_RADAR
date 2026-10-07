import sqlite3

DB = "radar_enterprise.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cursor.fetchall()]

if "phone" in columns:
    print("CAMPO PHONE: JA EXISTE")
else:
    cursor.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20)")
    conn.commit()
    print("CAMPO PHONE: ADICIONADO COM SUCESSO")

conn.close()

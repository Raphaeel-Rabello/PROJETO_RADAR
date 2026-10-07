import sqlite3


DATABASE = "radar_enterprise.db"


COLUMNS = [
    ("cpf", "VARCHAR(14)"),
    ("cnpj", "VARCHAR(18)"),
    ("account_type", "VARCHAR(30) NOT NULL DEFAULT 'pessoa_fisica'"),
    ("professional_type", "VARCHAR(50)"),
    ("company_name", "VARCHAR(180)"),
    ("birth_date", "DATE"),
    ("terms_accepted", "BOOLEAN NOT NULL DEFAULT 0"),
    ("privacy_accepted", "BOOLEAN NOT NULL DEFAULT 0"),
    ("terms_version", "VARCHAR(30)"),
    ("privacy_version", "VARCHAR(30)"),
]


def get_existing_columns(cursor):
    cursor.execute("PRAGMA table_info(users)")
    return {
        row[1]
        for row in cursor.fetchall()
    }


def main():
    print("=" * 60)
    print("RADAR - MIGRAÇÃO DA TABELA USERS")
    print("=" * 60)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        existing_columns = get_existing_columns(cursor)

        added = 0

        for column_name, column_definition in COLUMNS:

            if column_name in existing_columns:
                print(f"[OK] {column_name} já existe.")
                continue

            sql = (
                f"ALTER TABLE users "
                f"ADD COLUMN {column_name} "
                f"{column_definition}"
            )

            cursor.execute(sql)

            print(f"[CRIADA] {column_name}")

            added += 1

        connection.commit()

        print("=" * 60)
        print(f"MIGRAÇÃO CONCLUÍDA! {added} coluna(s) adicionada(s).")
        print("=" * 60)

    except Exception as error:
        connection.rollback()

        print("=" * 60)
        print("ERRO DURANTE A MIGRAÇÃO")
        print(error)
        print("=" * 60)

        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()

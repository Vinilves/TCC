from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[2]

CAMINHO_BANCO = BASE_DIR / "data" / "sqlite" / "banco_respostas.sqlite"


def conectar() -> sqlite3.Connection:
    return sqlite3.connect(CAMINHO_BANCO)


def buscar_respostas(conn: sqlite3.Connection, ids):
    cursor = conn.cursor()

    placeholders = ",".join("?" * len(ids))

    cursor.execute(
        f"""
        SELECT
            id,
            question,
            answer,
            code,
            source
        FROM respostas
        WHERE id IN ({placeholders})
        """,
        [int(i) for i in ids]
    )

    resultados = cursor.fetchall()

    mapa = {linha[0]: linha for linha in resultados}

    return [mapa[i] for i in ids if i in mapa]
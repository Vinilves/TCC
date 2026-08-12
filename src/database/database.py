from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[2]

CAMINHO_BANCO = BASE_DIR / "data" / "sqlite" / "banco_respostas.sqlite"

def conectar() -> sqlite3.Connection:
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela_interacoes(conn: sqlite3.Connection) -> None:

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            modo TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            pergunta_processada TEXT,
            resposta TEXT,
            id_resposta INTEGER,
            similaridade REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()


def registrar_interacao(conn: sqlite3.Connection, session_id: str, modo: str, pergunta: str, pergunta_processada: str | None = None, resposta: str | None = None, id_resposta: int | None = None, similaridade: float | None = None) -> None:

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interacoes (
            session_id,
            modo,
            pergunta,
            pergunta_processada,
            resposta,
            id_resposta,
            similaridade
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            modo,
            pergunta,
            pergunta_processada,
            resposta,
            id_resposta,
            similaridade
        )
    )

    conn.commit()


def buscar_respostas(conn: sqlite3.Connection, ids):
    cursor = conn.cursor()

    if len(ids) == 0:
        return []

    placeholders = ",".join("?" * len(ids))

    cursor.execute(
        f"""
        SELECT
            id,
            question,
            answer,
            code,
            source,
            language
        FROM respostas
        WHERE id IN ({placeholders})
        """,
        [int(i) for i in ids]
    )

    resultados = cursor.fetchall()

    mapa = {linha[0]: linha for linha in resultados}

    return [mapa[i] for i in ids if i in mapa]

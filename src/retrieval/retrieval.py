from pathlib import Path
import faiss
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]

CAMINHO_INDICE = BASE_DIR / "data" / "faiss" / "indice_faiss.index"


def carregar_indice() -> faiss.Index:
    return faiss.read_index(str(CAMINHO_INDICE))


def buscar_respostas(
    indice: faiss.Index,
    embedding: np.ndarray,
    k: int = 10
):
    distancias, indices = indice.search(
        embedding.reshape(1, -1),
        k
    )

    return distancias, indices
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

modelo = SentenceTransformer(MODEL_NAME)


def gerar_embedding(texto: str) -> np.ndarray:
    embedding = modelo.encode(
        texto,
        normalize_embeddings=True
    )

    return np.asarray(embedding, dtype=np.float32)
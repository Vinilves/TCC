import re
import unicodedata

def normalizar(texto: str) -> str:

    texto = texto.lower().strip()

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto


def normalizar_para_comparacao(texto: str) -> str:

    texto = normalizar(texto)

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def remover_pontuacao_final(texto: str) -> str:

    return re.sub(
        r"[!?.,;:]+$",
        "",
        texto
    ).strip()
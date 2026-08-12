import re
import torch

from transformers import (AutoTokenizer, AutoModelForSeq2SeqLM)

MODEL_NAME = ("Helsinki-NLP/opus-mt-en-ROMANCE")


device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


print("Carregando modelo de tradução...")
print("Modelo:", MODEL_NAME)


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
).to(device)

model.eval()


def separar_codigo(texto):

    if not isinstance(texto, str):
        return [("texto", texto)]

    partes = []

    padrao = (
        r"(```[\s\S]*?```|`[^`\n]+`)"
    )

    ultimo_fim = 0

    for match in re.finditer(padrao, texto):

        inicio = match.start()
        fim = match.end()

        if inicio > ultimo_fim:

            partes.append(
                (
                    "texto",
                    texto[
                        ultimo_fim:inicio
                    ]
                )
            )

        partes.append(
            (
                "codigo",
                match.group(0)
            )
        )

        ultimo_fim = fim

    if ultimo_fim < len(texto):

        partes.append(
            (
                "texto",
                texto[ultimo_fim:]
            )
        )

    return partes

def traduzir_lote(textos, batch_size=16):

    resultados = []

    for inicio in range(
        0,
        len(textos),
        batch_size
    ):

        fim = min(
            inicio + batch_size,
            len(textos)
        )

        lote = textos[
            inicio:fim
        ]

        lote = [
            ">>pt_BR<< " + texto
            for texto in lote
        ]

        entradas = tokenizer(
            lote,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(device)

        with torch.inference_mode():

            saidas = model.generate(
                **entradas,
                max_length=512
            )

        traducoes = tokenizer.batch_decode(
            saidas,
            skip_special_tokens=True
        )

        resultados.extend(
            traducoes
        )

    return resultados


def traduzir_resposta(texto: str) -> str:

    if not isinstance(texto, str):
        return texto

    if not texto.strip():
        return texto

    partes = separar_codigo(texto)

    textos = []
    indices = []

    resultado = [
        None
    ] * len(partes)

    for i, (
        tipo,
        conteudo
    ) in enumerate(partes):

        if tipo == "texto":

            if conteudo.strip():

                textos.append(
                    conteudo
                )

                indices.append(i)

            else:

                resultado[i] = (
                    conteudo
                )

        else:

            resultado[i] = (
                conteudo
            )

    if textos:

        traducoes = traduzir_lote(
            textos
        )

        for indice, traducao in zip(
            indices,
            traducoes
        ):

            resultado[indice] = (
                traducao
            )

    return "".join(
        parte
        for parte in resultado
        if parte is not None
    )
import re
from src.preprocessing.normalizer import (normalizar_para_comparacao, remover_pontuacao_final)


MENSAGEM_SAUDACAO = (
    "Olá estudante! Sou um chatbot voltado ao ensino de programação em Python. "
    "Como posso ajudá-lo hoje?"
)

MENSAGEM_DESPEDIDA = (
    "Foi um prazer ajudar. Bons estudos em Python!"
)

MENSAGEM_MODERACAO = (
    "Peço que mantenhamos uma comunicação respeitosa para que eu possa ajudá-lo."
)

MENSAGEM_VAZIA = (
    "Digite uma pergunta relacionada à programação em Python para que eu possa ajudá-lo."
)


SAUDACOES = {
    "oi",
    "ola",
    "bom dia",
    "boa tarde",
    "boa noite",
    "e ai",
    "eae",
    "eai",
    "ei",
    "opa",
    "hello",
    "hi",
}


DESPEDIDAS = {
    "tchau",
    "ate logo",
    "ate mais",
    "ate breve",
    "falou",
    "flw",
}


AGRADECIMENTOS = {
    "obrigado",
    "obrigada",
    "valeu",
    "muito obrigado",
    "muito obrigada",
}


PALAVROES = {
    "idiota",
    "burro",
    "imbecil",
    "otario",
    "babaca",
    "estupido",
    "ignorante",
    "inutil",
    "ridiculo",
    "palhaco",
    "retardado",

    "merda",
    "bosta",
    "porra",
    "caralho",
    "cacete",
    "droga",

    "fdp",
    "arrombado",
    "desgracado",
    "corno",
}


def eh_mensagem_isolada(mensagem: str, conjunto: set[str]) -> bool:

    mensagem = remover_pontuacao_final(
        mensagem
    )

    return mensagem in conjunto


def contem_palavra_ofensiva(mensagem: str) -> bool:

    palavras = re.findall(
        r"\w+",
        mensagem
    )

    return any(
        palavra in PALAVROES
        for palavra in palavras
    )


def verificar_regras(texto: str) -> tuple[bool, str | None]:

    mensagem = normalizar_para_comparacao(
        texto
    )

    if not mensagem:
        return True, MENSAGEM_VAZIA

    if contem_palavra_ofensiva(mensagem):
        return True, MENSAGEM_MODERACAO

    if eh_mensagem_isolada(
        mensagem,
        SAUDACOES
    ):
        return True, MENSAGEM_SAUDACAO

    if eh_mensagem_isolada(
        mensagem,
        DESPEDIDAS
    ):
        return True, MENSAGEM_DESPEDIDA

    if eh_mensagem_isolada(
        mensagem,
        AGRADECIMENTOS
    ):
        return True, MENSAGEM_DESPEDIDA

    return False, None
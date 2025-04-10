# -*- coding: utf-8 -*-
# Autor: [Camily Albres e Daniela Lima]
# Data: 2025-04-10
# Descrição: Validador de expressões lógicas em LaTeX
# Uso: python validador.py <arquivo.txt>

r"""  #! extensão better comments pro vscode
* aceita expressões como:
true
1a
( \neg 2b )
( \wedge 1p false )
( \vee ( \neg 3x ) ( \rightarrow 4y true ) )

* rejeita coisas como:
( 1a \neg false ) — operador no lugar errado
( \vee true ) — operador binário com apenas 1 operando
\neg ( 1a ) — não está na forma ( ... )
"""

import re
import sys

# ======================
# LÉXICO
# ======================

TOKEN_REGEX = [
    ("ABREPAREN", r"\("),
    ("FECHAPAREN", r"\)"),
    ("OP_UNARIO", r"\\neg"),
    ("OP_BINARIO", r"\\wedge|\\vee|\\rightarrow|\\leftrightarrow"),
    ("CONSTANTE", r"true|false"),
    ("PROPOSICAO", r"[0-9][0-9a-z]*"),
    ("ESPACO", r"\s+"),
]


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"{self.tipo}({self.valor})"


def lexer(expr):
    """
    Lê a expressão caractere por caractere,
    usa regex para reconhecer os tipos de token,
    ignora espaços,
    se tudo certo → retorna lista de tokens
    """
    tokens = []
    i = 0
    while i < len(expr):
        match = None
        for tipo, regex in TOKEN_REGEX:
            pattern = re.compile(regex)
            match = pattern.match(expr, i)
            if match:
                if tipo != "ESPACO":  # ignora espaços
                    token = Token(tipo, match.group(0))
                    tokens.append(token)
                i = match.end()
                break
        if not match:
            return None  # erro léxico
    return tokens

# ======================
# SINTÁTICO
# ======================


class Parser:
    """
    cada método representa uma regra da gramática
    tenta reconhecer a entrada de tokens de acordo com essas regras
    usa uma estratégia recursiva: cada formula pode chamar outras formula, proposicao, etc

    se o parser conseguir chegar ao final da lista de tokens com sucesso, então a expressão está gramaticalmente correta
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, tipo):
        if self.pos < len(self.tokens) and self.tokens[self.pos].tipo == tipo:
            self.pos += 1
            return True
        return False

    def parse(self):
        return self.FORMULA() and self.pos == len(self.tokens)

    def FORMULA(self):
        return (
            self.CONSTANTE()
            or self.PROPOSICAO()
            or self.FORMULAUNARIA()
            or self.FORMULABINARIA()
        )

    def CONSTANTE(self):
        return self.match("CONSTANTE")

    def PROPOSICAO(self):
        return self.match("PROPOSICAO")

    def FORMULAUNARIA(self):
        start = self.pos
        if self.match("ABREPAREN") and self.match("OP_UNARIO") and self.FORMULA() and self.match("FECHAPAREN"):
            return True
        self.pos = start
        return False

    def FORMULABINARIA(self):
        start = self.pos
        if self.match("ABREPAREN") and self.match("OP_BINARIO") and self.FORMULA() and self.FORMULA() and self.match("FECHAPAREN"):
            return True
        self.pos = start
        return False

# ======================
# MAIN
# ======================


def validar_expressao(expr):
    tokens = lexer(expr)
    if tokens is None:
        return False
    parser = Parser(tokens)
    return parser.parse()


def main():
    if len(sys.argv) < 2:
        print("Uso: python validador.py <arquivo.txt>")
        return

    caminho_arquivo = sys.argv[1]
    try:
        with open(caminho_arquivo, "r") as f:
            linhas = f.readlines()
            qtd = int(linhas[0].strip())
            expressoes = [linha.strip() for linha in linhas[1:qtd+1]]

            for expr in expressoes:
                if validar_expressao(expr):
                    print("valida")
                else:
                    print("invalida")
    except Exception as e:
        print("Erro ao processar o arquivo:", e)


if __name__ == "__main__":
    main()

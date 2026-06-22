from dataclasses import dataclass, field

LAMBDA = "\\"
LIMITE_COMPUTACOES = 10000


# Estrutura que define uma transição e seus atributos.
@dataclass
class Transicao:
    origem: str
    destino: str
    entrada: str


# Estrutura que define um estado e seus atributos.
@dataclass
class Estado:
    nome: str
    inicial: bool = False
    final: bool = False
    transicoes: list[Transicao] = field(default_factory=list)


# Estrutura que define o AFN.
@dataclass
class AFN:
    estados: dict[str, Estado] = field(default_factory=dict)
    alfabetoEntrada: list[str] = field(default_factory=list)


# Cria um estado.
def criaEstadoAFN(afn, nome):
    afn.estados[nome] = Estado(nome=nome)


# Define se um estado é ou não inicial.
def defineEstadoInicial(afn, nomeEstado):
    afn.estados[nomeEstado].inicial = True


# Define os estados finais do AFN.
def defineEstadosFinais(afn, estadosFinais):
    for nome in estadosFinais:
        afn.estados[nome].final = True


# Cria uma transição do AFN.
def criaTransicaoAFN(afn, origem, destino, simboloLido):
    if simboloLido != LAMBDA and simboloLido not in afn.alfabetoEntrada:
        raise ValueError(
            f"Símbolo de entrada inválido: {simboloLido}. " )

    transicao = Transicao(origem=origem, destino=destino, entrada=simboloLido,)

    # Associa a transição ao estado de origem.
    afn.estados[origem].transicoes.append(transicao)


def inicializaAFN(nomesEstados, alfabetoEntrada, estadosIniciais, estadosFinais,transicoes):
    afn = AFN()
    afn.alfabetoEntrada = alfabetoEntrada

    for nome in nomesEstados:
        criaEstadoAFN(afn, nome)

    for estado in estadosIniciais:
        defineEstadoInicial(afn, estado)

    defineEstadosFinais(afn, estadosFinais)

    for origem, destino, simboloLido in transicoes:
        criaTransicaoAFN(afn, origem, destino, simboloLido)

    return afn


def marcarEstadosIniciais(afn):
    estadosIniciais = []

    for estado in afn.estados.values():
        if estado.inicial:
            estadosIniciais.append(estado)

    return estadosIniciais


def aplicaTransicaoAFN(transicao, palavra, indice):
    novo_indice = indice

    # Transição lambda não consome símbolo da palavra.
    if transicao.entrada == LAMBDA:
        return novo_indice

    # Se a palavra já acabou, não há símbolo para consumir.
    if indice >= len(palavra):
        return None

    # A transição só é válida se o símbolo atual bater com a entrada da transição.
    if palavra[indice] != transicao.entrada:
        return None

    # Consome um símbolo da palavra.
    novo_indice += 1

    return novo_indice


def reconhecerPalavraAFN(afn, palavra):
    estados_iniciais = marcarEstadosIniciais(afn)

    if len(estados_iniciais) == 0:
        print("O automato não possui estado inicial")
        return False
    # Foi reutilizado a mesma lógica da APN, porém aqui
    # Cada item da fronteira é uma configuração:
    # (estado_atual, indice_lido)
    #
    fronteira: list[tuple[Estado, int]] = [
        (estado, 0) for estado in estados_iniciais
    ]

    # Evita testar a mesma configuração infinitas vezes,
    # principalmente quando existem ciclos com transições lambda.
    visitados: set[tuple[str, int]] = set()

    configuracoes_testadas = 0

    while fronteira:
        estado_atual, indice = fronteira.pop()
        configuracoes_testadas += 1

        if configuracoes_testadas > LIMITE_COMPUTACOES:
            return False

        chave = (estado_atual.nome, indice)

        if chave in visitados:
            continue

        visitados.add(chave)

        # Reconhecimento de AFN:
        # a palavra foi completamente lida e o estado atual é final.
        palavra_lida = indice == len(palavra)

        if palavra_lida and estado_atual.final:
            return True

        # Testa todas as transições possíveis a partir do estado atual.
        # O reversed é usado para preservar a ordem original das transições
        # quando usamos fronteira.pop().
        for transicao in reversed(estado_atual.transicoes):
            novo_indice = aplicaTransicaoAFN(transicao, palavra, indice)

            if novo_indice is None:
                continue

            novo_estado = afn.estados[transicao.destino]

            # Guarda um novo caminho possível para ser testado depois.
            fronteira.append((novo_estado, novo_indice))

    return False


def processaPalavrasAFN(palavras):
    afn = AFN()
    for palavra in palavras:
        if reconhecerPalavraAFN(afn, palavra):
            print("OK")
        else:
            print("X")


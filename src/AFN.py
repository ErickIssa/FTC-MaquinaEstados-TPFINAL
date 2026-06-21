from dataclasses import dataclass, field

LAMBDA = "\\"
limite_Computacoes = 10000
#estrutura que define uma transicao e seus atributos
@dataclass
class Transicao:
    origem: str
    destino: str
    entrada: str
#estrutura que define um estado e seus atributos
@dataclass
class Estado:
    nome: str
    inicial: bool = False
    final: bool = False
    transicoes: list[Transicao] = field(default_factory=list)

#estrutura que define o APN
@dataclass
class AFN:
    estados: dict[str, Estado] = field(default_factory=dict)
    alfabetoEntrada: list[str] = field(default_factory=list)

#Cria um estado
def criaEstadoAFN(afn, nome):
    afn.estados[nome] = Estado(nome=nome)

#Define se um estado é ou não inicial
def defineEstadoInicial(afn, nomeEstado):
    afn.estados[nomeEstado].inicial = True

#Define os estados finais do APN
def defineEstadosFinais(afn, estadosFinais):
    for nome in estadosFinais:
        afn.estados[nome].final = True

#Cria as transicoes do APN
def criaTransicaoAPN(afn, origem, destino, simboloLido):
    transicao = Transicao(origem=origem, destino=destino, entrada=simboloLido)
    #associa transição ao estado de origem
    afn.estados[origem].transicoes.append(transicao)


def inicializaAPN(nomesEstados,alfabetoEntrada, estadosIniciais, estadosFinais, transicoes):
    afn = AFN()
    afn.alfabetoEntrada = alfabetoEntrada

    for nome in nomesEstados:
        criaEstadoAFN(afn, nome)

    for estado in estadosIniciais:
        defineEstadoInicial(afn, estado)

    defineEstadosFinais(afn, estadosFinais)

    for origem, destino, simboloLido in transicoes:
        criaTransicaoAPN(afn, origem, destino, simboloLido)

    return afn


def reconhecerPalavraAPN(apn, palavra):
    estadoAtual = None
    for estado in apn.estados.values():
        if estado.inicial:
            estadoAtual = estado
            break
    if estadoAtual is None:
        print("O automato não possui estado inicial")
        return False

    i = 0
    while True:
        encontrouTransicaoValida=False

        for t in estadoAtual.transicoes:

            if t.entrada == LAMBDA:
                simboloEntradaValido = True
            else:
                if i >= len(palavra):
                    continue
                simboloEntradaValido = (palavra[i] == t.entrada) #compara se o simbolo equivale a entrada da transição

            if not simboloEntradaValido: #se não bate, verifica a próxima transição existente
                continue

            # consome o simbolo de entrada, avança na palavra
            if t.entrada != LAMBDA:
                i += 1

            # avança para o próximo estado
            estadoAtual = apn.estados[t.destino]

            encontrouTransicaoValida=True
            break

        if not encontrouTransicaoValida:
            break

    # se consumiu a palavra toda, parou em um estado final e a pilha está vazia, reconhece a palavra
    return (i == len(palavra) and estadoAtual.final)


def processaPalavrasAFN(palavras, afn):
    for palavra in palavras:
        if reconhecerPalavraAPN(afn, palavra):
            print("OK")
        else:
            print("X")

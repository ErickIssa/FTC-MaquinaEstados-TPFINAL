from dataclasses import dataclass,field

LAMBDA = "\\"

#estrutura que define uma transicao e seus atributos
@dataclass
class Transicao:
    origem: str
    destino: str
    entrada: str
    desempilha: str
    empilha: list[str]

#estrutura que define um estado e seus atributos
@dataclass
class Estado:
    nome: str
    inicial: bool = False
    final: bool = False
    transicoes: list[Transicao] = field(default_factory=list) #lista de transicoes que saem desse estado

#estrutura que define o APD
@dataclass
class APD:
    estados: dict[str, Estado] = field(default_factory=dict) #lista de estados
    alfabetoEntrada: list[str] = field(default_factory=list)
    alfabetoPilha: list[str] = field(default_factory=list)
    pilha: list[str]=field(default_factory=list)
    
#Cria um estado
def criaEstadoAPD(apd, nome):

    estado=Estado(nome=nome)
    apd.estados[nome] = estado

#Define o estado inicial do apd
def defineEstadoInicial(apd, nomeEstado):
    apd.estados[nomeEstado].inicial = True

#Define os estados finais do apd
def defineEstadosFinais(apd, estadosFinais):
    for nome in estadosFinais:
        apd.estados[nome].final=True

#Cria as transicoes do apd
def criaTransicaoAPD(apd, origem, destino, simboloLido, desempilha, empilha):
    if empilha == LAMBDA:
        empilha = [] #se for lambda, o caractere a empilhar será vazio
    else:
        empilha = list(empilha)

    #cria a transição
    transicao = Transicao(origem=origem, destino=destino, entrada=simboloLido, desempilha=desempilha, empilha=empilha)

    #associa transição ao estado de origem
    apd.estados[origem].transicoes.append(transicao)

def inicializaAPD(nomesEstados, alfabetoPilha, alfabetoEntrada, estadoInicial, estadosFinais, transicoes):
    #cria o automato
    apd = APD()

    #atribui alfabetos da pilha e de entrada
    apd.alfabetoPilha = alfabetoPilha
    apd.alfabetoEntrada= alfabetoEntrada

    #cria os estados com seus respectivos nomes
    for nome in nomesEstados:
        criaEstadoAPD(apd, nome)

    #define os estados iniciais e finais
    defineEstadoInicial(apd, estadoInicial)
    defineEstadosFinais(apd, estadosFinais)

    #cria as transições
    for t in transicoes:

        origem = t[0]
        destino = t[1]
        simboloLido = t[2]
        desempilha = t[3]
        empilha = t[4]

        criaTransicaoAPD(apd, origem, destino, simboloLido, desempilha, empilha)

    return apd

def reconhecerPalavra(apd, palavra):

    # limpa a pilha
    apd.pilha.clear()

    # procura estado inicial
    estadoAtual = None
    for estado in apd.estados.values():
        if estado.inicial:
            estadoAtual = estado
            break

    if estadoAtual is None:
        print("O automato não possui estado inicial")
        return False

    i = 0 #indice do simbolo da palavra lido
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

            if t.desempilha != LAMBDA: #a transicao exige que desempilhe um simbolo

                #se a pilha esta vazia ou o topo não é o símbolo a ser desempilhado, vai pra próxima transição
                if len(apd.pilha) == 0:
                    continue 
                if apd.pilha[-1] != t.desempilha:
                    continue

            # consome o simbolo de entrada, avança na palavra
            if t.entrada != LAMBDA:
                i += 1

            # desempilha
            if t.desempilha != LAMBDA:
                apd.pilha.pop()

            # empilha
            for simbolo in reversed(t.empilha):
                apd.pilha.append(simbolo)

            # avança para o próximo estado
            estadoAtual = apd.estados[t.destino]

            encontrouTransicaoValida=True
            break

        if not encontrouTransicaoValida:
            break

    # se consumiu a palavra toda, parou em um estado final e a pilha está vazia, reconhece a palavra
    return (i == len(palavra) and estadoAtual.final and len(apd.pilha) == 0)

def processaPalavras(palavras,apd):
    for palavra in palavras:
        if reconhecerPalavra(apd, palavra):
            print("OK")
        else:
            print("X")



# def leEntrada(nomeArquivo):
#     nomesEstados = []
#     alfabetoPilha = []
#     alfabetoEntrada = []
#     estadoInicial = ""
#     estadosFinais = []
#     transicoes = []
#     palavras = []

#     lendoAutomato = True

#     with open(nomeArquivo, "r", encoding="utf-8") as arquivo:

#         for linha in arquivo:
#             linha = linha.rstrip("\n")

#             if lendoAutomato:

#                 if linha == "---":
#                     lendoAutomato = False
#                     continue

#                 if linha.startswith("Q:"):
#                     nomesEstados = linha[2:].strip().split()

#                 elif linha.startswith("S:"):
#                     alfabeto = linha[2:].strip()
#                     alfabetoEntrada = alfabeto.split() if " " in alfabeto else list(alfabeto)

#                 elif linha.startswith("G:"):
#                     alfabeto = linha[2:].strip()
#                     alfabetoPilha = alfabeto.split() if " " in alfabeto else list(alfabeto)

#                 elif linha.startswith("I:"):
#                     estadoInicial = linha[2:].strip()

#                 elif linha.startswith("F:"):
#                     estadosFinais = linha[2:].strip().split()

#                 elif "->" in linha:
#                     origem, resto = linha.split("->", 1)
#                     origem = origem.strip()

#                     destino, parteTransicoes = resto.split("|", 1)
#                     destino = destino.strip()

#                     for texto in parteTransicoes.split():
#                         entrada, resto = texto.split(",", 1)
#                         desempilha, empilha = resto.split("/", 1)

#                         transicoes.append([
#                             origem,
#                             destino,
#                             entrada,
#                             desempilha,
#                             empilha
#                         ])

#             else:
#                 # Guarda a palavra (inclusive vazia)
#                 palavras.append(linha)

#     apd = inicializaAPD(
#         nomesEstados,
#         alfabetoPilha,
#         alfabetoEntrada,
#         estadoInicial,
#         estadosFinais,
#         transicoes
#     )

#     return apd, palavras


# if __name__ == "__main__":

#     apd, palavras = leEntrada("entradaAPD.txt")

#     print("Alfabeto de entrada:", apd.alfabetoEntrada)
#     print("Alfabeto da pilha:", apd.alfabetoPilha)
#     print()

#     for nome, estado in apd.estados.items():
#         print("Estado:", nome)
#         print("Inicial:", estado.inicial)
#         print("Final:", estado.final)

#         for t in estado.transicoes:
#             print(t)

#         print()

#     print("Resultado do reconhecimento:")
#     processaPalavras(palavras,apd)



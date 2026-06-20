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

#estrutura que define o APN
@dataclass
class APN:
    estados: dict[str, Estado] = field(default_factory=dict) #lista de estados
    alfabetoEntrada: list[str] = field(default_factory=list)
    alfabetoPilha: list[str] = field(default_factory=list)
    pilha: list[str]=field(default_factory=list)
    
#Cria um estado
def criaEstadoAPN(apn, nome):

    estado=Estado(nome=nome)
    apn.estados[nome] = estado

#Define o estado inicial do APN
def defineEstadoInicial(APN, nomeEstado):
    APN.estados[nomeEstado].inicial = True

#Define os estados finais do APN
def defineEstadosFinais(APN, estadosFinais):
    for nome in estadosFinais:
        APN.estados[nome].final=True

#Cria as transicoes do APN
def criaTransicaoAPN(APN, origem, destino, simboloLido, desempilha, empilha):
    if empilha == LAMBDA:
        empilha = [] #se for lambda, o caractere a empilhar será vazio
    else:
        empilha = list(empilha)

    #cria a transição
    transicao = Transicao(origem=origem, destino=destino, entrada=simboloLido, desempilha=desempilha, empilha=empilha)

    #associa transição ao estado de origem
    APN.estados[origem].transicoes.append(transicao)

def inicializaAPN(nomesEstados, alfabetoPilha, alfabetoEntrada, estadoInicial, estadosFinais, transicoes):
    #cria o automato
    APN = APN()

    #atribui alfabetos da pilha e de entrada
    APN.alfabetoPilha = alfabetoPilha
    APN.alfabetoEntrada= alfabetoEntrada

    #cria os estados com seus respectivos nomes
    for nome in nomesEstados:
        criaEstadoAPN(APN, nome)

    #define os estados iniciais e finais
    defineEstadoInicial(APN, estadoInicial)
    defineEstadosFinais(APN, estadosFinais)

    #cria as transições
    for t in transicoes:

        origem = t[0]
        destino = t[1]
        simboloLido = t[2]
        desempilha = t[3]
        empilha = t[4]

        criaTransicaoAPN(APN, origem, destino, simboloLido, desempilha, empilha)

    return APN


def inicializaAPN(nomesEstados, alfabetoPilha, alfabetoEntrada, estadosIniciais, estadosFinais, transicoes):
    #cria o automato
    APN = APN()

    #atribui alfabetos da pilha e de entrada
    APN.alfabetoPilha = alfabetoPilha
    APN.alfabetoEntrada= alfabetoEntrada

    #cria os estados com seus respectivos nomes
    for nome in nomesEstados:
        criaEstadoAPN(APN, nome)

    #define os estados iniciais e finais
    for estado in estadosIniciais:
        defineEstadoInicial(APN, estado)
    defineEstadosFinais(APN, estadosFinais)

    #cria as transições
    for t in transicoes:

        origem = t[0]
        destino = t[1]
        simboloLido = t[2]
        desempilha = t[3]
        empilha = t[4]

        criaTransicaoAPN(APN, origem, destino, simboloLido, desempilha, empilha)

    return APN

def marcarEstadosIniciais(APN):
    estadosIniciais = []
    for estado in APN.estados.values():
        if estado.inicial:
            estadosIniciais.append(estado)

    return estadosIniciais


def reconhecerPalavraAPN(APN, palavra):

    # limpa a pilha
    APN.pilha.clear()

    # procura estado inicial
    estadoAtual = None
    estados = marcarEstadosIniciais(APN)

    if estados.size() == 0:
        print("O automato não possui estado inicial")
        return False

    for estado in estados:
        estadoAtual = estado


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
                    if len(APN.pilha) == 0:
                        continue 
                    if APN.pilha[-1] != t.desempilha:
                        continue

                # consome o simbolo de entrada, avança na palavra
                if t.entrada != LAMBDA:
                    i += 1

                # desempilha
                if t.desempilha != LAMBDA:
                    APN.pilha.pop()

                # empilha
                if (t.desempilha != LAMBDA):
                    for simbolo in reversed(t.empilha):
                        APN.pilha.append(simbolo)

                # avança para o próximo estado
                estadoAtual = APN.estados[t.destino]

                encontrouTransicaoValida=True
                break

            if not encontrouTransicaoValida:
                break
        if (i == len(palavra) and estadoAtual.final and len(APN.pilha) == 0):
            break
    # se consumiu a palavra toda, parou em um estado final e a pilha está vazia, reconhece a palavra
    return (i == len(palavra) and estadoAtual.final and len(APN.pilha) == 0)

def processaPalavrasAPN(palavras,APN):
    for palavra in palavras:
        if reconhecerPalavraAPN(APN, palavra):
            print("OK")
        else:
            print("X")


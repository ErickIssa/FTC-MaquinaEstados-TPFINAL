from dataclasses import dataclass, field

LAMBDA = "\\"
LIMITE_COMPUTACOES = 10000
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
    transicoes: list[Transicao] = field(default_factory=list)

#estrutura que define o APN
@dataclass
class APN:
    estados: dict[str, Estado] = field(default_factory=dict)
    alfabetoEntrada: list[str] = field(default_factory=list)
    alfabetoPilha: list[str] = field(default_factory=list)

#Cria um estado
def criaEstadoAPN(apn, nome):
    apn.estados[nome] = Estado(nome=nome)

#Define se um estado é ou não inicial
def defineEstadoInicial(apn, nomeEstado):
    apn.estados[nomeEstado].inicial = True

#Define os estados finais do APN
def defineEstadosFinais(apn, estadosFinais):
    for nome in estadosFinais:
        apn.estados[nome].final = True

#Cria as transicoes do APN
def criaTransicaoAPN(apn, origem, destino, simboloLido, desempilha, empilha):
    if empilha == LAMBDA:
        simbolos_empilhados: list[str] = []#se for lambda, o caractere a empilhar será vazio
    else:
        simbolos_empilhados = list(empilha)
    #cria a transição
    transicao = Transicao(origem=origem, destino=destino, entrada=simboloLido, desempilha=desempilha, empilha=simbolos_empilhados,
    )
    #associa transição ao estado de origem
    apn.estados[origem].transicoes.append(transicao)


def inicializaAPN(nomesEstados, alfabetoPilha, alfabetoEntrada, estadosIniciais, estadosFinais, transicoes, exigir_estado_final: bool = True):
    apn = APN()
    apn.alfabetoPilha = alfabetoPilha
    apn.alfabetoEntrada = alfabetoEntrada

    for nome in nomesEstados:
        criaEstadoAPN(apn, nome)
    
    for estado in estadosIniciais:
        defineEstadoInicial(apn, estado)
    if exigir_estado_final == True:
        defineEstadosFinais(apn, estadosFinais)

    for origem, destino, simboloLido, desempilha, empilha in transicoes:
        criaTransicaoAPN(apn, origem, destino, simboloLido, desempilha, empilha)

    return apn


def marcarEstadosIniciais(apn):
    estadosIniciais = []
    for estado in APN.estados.values():
        if estado.inicial:
            estadosIniciais.append(estado)
    return estadosIniciais


def aplicaTransicao(transicao, palavra,indice, pilha):
    novo_indice = indice

    # Verifica símbolo da entrada.
    if transicao.entrada != LAMBDA:
        if indice >= len(palavra):
            return None
        if palavra[indice] != transicao.entrada:
            return None
        novo_indice += 1

    # Copia a pilha
    nova_pilha = pilha.copy()

    # Verifica e executa desempilhamento.
    if transicao.desempilha != LAMBDA:
        if not nova_pilha:
            return None
        if nova_pilha[-1] != transicao.desempilha:
            return None
        nova_pilha.pop()

    # Executa empilhamento. O topo da pilha é o fim da lista, assim invertemos a ordem de inserção.
    for simbolo in reversed(transicao.empilha):
        nova_pilha.append(simbolo)

    return novo_indice, nova_pilha

# Boa parte da lógica de manter o controle da pilha foi feita com auxilio do chatGPT, 
# por isso tem umas funções e lógicas diferentes do resto do arquivo e está bem mais comentado, 
# pois fui adicionando informações para eu mesmo entender =D
# Outro detalhe, essa maquina permite o reconhecimento padrão (palavra consumida, pilha vazia e em um estado final)
# Mas também permite que seja reconhecida por pilha vazia (palavra consumida e pilha vazia)
# Por padrão, se não for especificado, ela executa considerando o reconhecimento padrão.
def reconhecerPalavraAPN(apn, palavra, exigir_estado_final: bool = True):
    estados_iniciais = marcarEstadosIniciais(apn)

    if len(estados_iniciais) == 0:
        print("O automato não possui estado inicial")
        return False

    # Cada item é uma configuração: (estado_atual, índice_lido, pilha_atual).
        #Em qual estado estou?
        #Qual posição da palavra eu já li?
        #Como está a pilha neste caminho?
    # A pilha de cada configuração é independente.
    fronteira: list[tuple[Estado, int, list[str]]] = [
        (estado, 0, []) for estado in estados_iniciais
    ]

    visitados: set[tuple[str, int, tuple[str, ...]]] = set()
    configuracoes_testadas = 0

    # percorre enquanto houver diferentes configurações (caminhos) possiveis nao testados.
    while fronteira:

        # escolhe uma configuração e remove da lista
        # cada pilha pertence a apenas uma configuração
        estado_atual, indice, pilha = fronteira.pop()
        configuracoes_testadas += 1

        if configuracoes_testadas > LIMITE_COMPUTACOES:
            # Evita loop infinito em APNs.
            return False

        chave = (estado_atual.nome, indice, tuple(pilha))
        #Se uma configuração já foi testada antes, não precisa testar de novo.
        if chave in visitados:
            continue
        visitados.add(chave)

        # Verifica se a configuração atual levou ao reconhecimento da palavra
        palavra_lida = indice == len(palavra)
        pilha_vazia = len(pilha) == 0
        estado_final_ok = (not exigir_estado_final) or estado_atual.final

        if palavra_lida and pilha_vazia and estado_final_ok:
            return True

        # Coloca as próximas configurações na pilha de busca.
        # reversed preserva a ordem das transições quando usamos pop().
        for transicao in reversed(estado_atual.transicoes):
            resultado = aplicaTransicao(transicao, palavra, indice, pilha)
            if resultado is None:
                continue

            novo_indice, nova_pilha = resultado
            novo_estado = apn.estados[transicao.destino]
            fronteira.append((novo_estado, novo_indice, nova_pilha))

    return False


def processaPalavrasAPN(palavras, apn):
    for palavra in palavras:
        if reconhecerPalavraAPN(apn, palavra):
            print("OK")
        else:
            print("X")

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

#OBS: field(default_factory=list) É USADO PARA EVITAR QUE AS INSTÂNCIAS COMPARTILHEM O MESMO OBJETO

#estrutura que define o APD
class APD:
    def __init__(self):
        self.estados: dict[str, Estado] = {}
        self.alfabetoEntrada: list[str] = []
        self.alfabetoPilha: list[str] = []
        self.pilha: list[str] = []

        
    #Cria um estado
    def criaEstadoAPD(self, nome):
        estado=Estado(nome=nome)
        self.estados[nome] = estado

    #Define o estado inicial do apd
    def defineEstadoInicial(self, nomeEstado):
        self.estados[nomeEstado].inicial = True

    #Define os estados finais do apd
    def defineEstadosFinais(self, estadosFinais):
        for nome in estadosFinais:
            self.estados[nome].final=True

    def criaTransicaoAPD(self, origem, destino, simboloLido, desempilha, empilha):

        if origem not in self.estados:
            print(f"estado de origem '{origem}' não existe")
            return
        if destino not in self.estados:
            print(f"estado de destino '{destino}' não existe")
            return

        estadoOrigem = self.estados[origem]

        # verifica se a nova transição é compatível com alguma transição já existente. Se for, nao cria a nova transicao
        for transicaoExistente in estadoOrigem.transicoes:

            #se entrou aqui, entao o estado ja contem ao menos uma transição
            
            #duas transicoes com mesma entrada,ou duas transicoes sendo uma delas com entrada lambda
            conflitoEntrada = (simboloLido == transicaoExistente.entrada or simboloLido == LAMBDA or transicaoExistente.entrada == LAMBDA)
            
            #desempilham a mesma coisa, ou alguma desempilha lambda
            conflitoPilha = (desempilha == transicaoExistente.desempilha or desempilha == LAMBDA or transicaoExistente.desempilha == LAMBDA)
            
            if conflitoEntrada and conflitoPilha:
                print("erro: transicoes compativeis")
                return

        if empilha == LAMBDA or empilha == [LAMBDA]:
            empilha = []
        elif isinstance(empilha, list):
            empilha = empilha
        else:
            empilha = list(empilha)

        #cria a transição
        transicao = Transicao(origem=origem, destino=destino, entrada=simboloLido, desempilha=desempilha, empilha=empilha)

        #associa transição ao estado de origem
        estadoOrigem.transicoes.append(transicao)


    def inicializaAPD(self, nomesEstados, alfabetoPilha, alfabetoEntrada, estadoInicial, estadosFinais, transicoes):

        #atribui alfabetos da pilha e de entrada
        self.alfabetoPilha = alfabetoPilha
        self.alfabetoEntrada= alfabetoEntrada

        #cria os estados com seus respectivos nomes
        for nome in nomesEstados:
            self.criaEstadoAPD(nome)

        #define os estados iniciais e finais
        self.defineEstadoInicial(estadoInicial)
        self.defineEstadosFinais(estadosFinais)

        #cria as transições
        for t in transicoes:

            origem = t[0]
            destino = t[1]
            simboloLido = t[2]
            desempilha = t[3]
            empilha = t[4]

            self.criaTransicaoAPD(origem, destino, simboloLido, desempilha, empilha)

    def reconhecerPalavraAPD(self, palavra):

        # limpa a pilha
        pilha = []

        # procura estado inicial
        estadoAtual = None
        for estado in self.estados.values():
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

                if t.desempilha != LAMBDA: #se o símbolo a desempilhar não é palavra vazia, precisa desempilhar um simbolo

                    #se a pilha esta vazia ou o topo não é o símbolo a ser desempilhado, vai pra próxima transição
                    if not pilha:
                        continue 
                    if pilha[-1] != t.desempilha:
                        continue
                        

                #se chegou aqui, significa que a transicao pode acontecer
                # consome o simbolo de entrada(avança na palavra)
                if t.entrada != LAMBDA:
                    i += 1

                # desempilha
                if t.desempilha != LAMBDA:
                    pilha.pop()

                # empilha
                for simbolo in reversed(t.empilha):
                    pilha.append(simbolo)

                # avança para o próximo estado
                estadoAtual = self.estados[t.destino]

                encontrouTransicaoValida=True
                break

            if not encontrouTransicaoValida:
                break

        # se consumiu a palavra toda, o estado é final e a pilha está vazia, reconhece a palavra
        return (i == len(palavra) and len(pilha) == 0 and estadoAtual.final)

    def processaPalavras(self, palavra):
        if self.reconhecerPalavraAPD(palavra):
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

#     apd = APD()
#     apd.inicializaAPD(
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
#     apd.processaPalavras(palavras)



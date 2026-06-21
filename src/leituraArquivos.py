from .AFD import AFD
from .apd import APD
from .turing import *
from .AFN import AFN
from .apn import APN

from .AFN import inicializaAFN
from .apn import inicializaAPN

def estadosTemNomesIguais(estados)->bool:
    return len(estados) != len(set(estados))

def leEstados(arquivo):
    #pega os estados
    linhaEstados = arquivo.readline().rstrip('\n')
    estados = linhaEstados.split()[1:]
    for i in estados:
        if len(i) >7:
            print("O TAMANHO MAXIMO DO NOME DOS ESTADOS EH 7")
            return None
    if(estadosTemNomesIguais(estados)):
        print("OS NOMES DOS ESTADOS DEVEM SER DIFERENTES")
        return None 
    return estados

def leAlfabeto(arquivo, naoPodePalavraVazia: bool, ehMaquinaDeTuring: bool): 

    #pega o alfabeto
    arquivo.read(3)
    alfabeto = []
    while(True):
        c = arquivo.read(1)
        if(c == '\n'):
            break
        if(c == '\\' and naoPodePalavraVazia):
            print(" \\ NAO EH UM CARACTERE VALIDO")
            return None
        if(c == '_' or c == '<' or c == '>')and(ehMaquinaDeTuring):
           print(f"{c} NAO EH UM CARACTERE VALIDO")
           return None
        alfabeto.append(c)

    if len(alfabeto) == 0:
        print("ALFABETO NAO PODE ESTAR VAZIO")
        return None
    return alfabeto

def leEstadoInicial(arquivo, estados: list):
    #pega o estado inicial

    linhaInicial = arquivo.readline().rstrip('\n')
    inicial = linhaInicial.split()[1]
    if inicial in estados:
        return inicial
    
    print(f"ESTADO INICIAL {inicial} ESTA FORA DA LISTA DE ESTADOS")
    return None

def leEstadosFinais(arquivo, estados: list):
    #pega os estados finais
    linhaFinais = arquivo.readline().rstrip('\n')
    finais = linhaFinais.split()[1:]
    falhou = False
    for i in finais:
        if i not in estados:
            print(f"ESTADO FINAL {i} FORA DA LISTA DE ESTADOS")
            falhou = True
    
    if falhou:
        return None
    return finais

def leEstadosIniciais(arquivo, estados: list):
    #pega os estados finais
    linhaIniciais = arquivo.readline().rstrip('\n')
    iniciais = linhaIniciais.split()[1:]
    falhou = False
    for i in iniciais:
        if i not in estados:
            print(f"ESTADO INICIAL {i} FORA DA LISTA DE ESTADOS")
            falhou = True
    
    if falhou:
        return None
    return iniciais

def leEntrada(arquivo, alfabeto):
    entradas = []
    while(True):
        entrada = arquivo.readline().rstrip('\n')
        if(entrada == ""):
            break
        valido = True
        for i in entrada:
            if i not in alfabeto:
                valido = False
        
        if valido:
            entradas.append(entrada)
        else:
            print(f"ENTRADA '{entrada}' INVALIDA")
            return None
    return entradas

def leEstadosOrigemEDestino(arquivo, estados: list):

    nomeEstadoOrigem = ""
    nomeEstadoDestino = ""
    FimDasTransicoes = False

    while(True):
        c = arquivo.read(1)
        if(c == ' '):
            break
        elif(c == '-'):
            FimDasTransicoes = True
            break
        nomeEstadoOrigem += c

    if(FimDasTransicoes):
        arquivo.readline() # Limpa o resto dos "---" e a quebra de linha
        return "", "", True

    if(nomeEstadoOrigem not in estados):
        print(f"ESTADO DE ORIGEM {nomeEstadoOrigem} NAO ESTA NA LISTA DE ESTADOS")
        return None, None, None


    if(nomeEstadoOrigem not in estados):
        print(f"ESTADO DE ORIGEM '{nomeEstadoOrigem}' NAO ESTA NA LISTA DE ESTADOS")
        return None, None, None

    arquivo.read(3)

    while(True):
        c = arquivo.read(1)
        if(c == ' '):
            break
        nomeEstadoDestino += c

    if(nomeEstadoDestino not in estados):
        print(f"ESTADO DE DESTINO {nomeEstadoDestino} NAO ESTA NA LISTA DE ESTADOS")
        return None,None,None   
    arquivo.read(2)

    return nomeEstadoOrigem, nomeEstadoDestino, FimDasTransicoes

def leMaquinaDeTuring(arquivo, EhALL: bool):

    estados = leEstados(arquivo)
    if(estados is None):
        return None, None

    alfabeto = leAlfabeto(arquivo,True,True)
    if(alfabeto is None):
        return None, None
            
    alfabetoFita = leAlfabeto(arquivo,True,True)
    if(alfabetoFita is None):
        return None, None
    for i in alfabetoFita:
        if(i in alfabeto):
            print(f"{i} JA ESTA NO ALFABETO DE ENTRADA, O ALFABETO DE FITA DEVE SER EXCLUSIVO PARA A FITA")
            return
            
    inicial = leEstadoInicial(arquivo, estados)
    if(inicial is None):
        return None, None
            
    finais = leEstadosFinais(arquivo, estados)
    if(finais is None):
        return None, None
            
    #pega transicoes
    transicoes = []
    transicao = ['a','b','d','e','f'] # lido, escrito, sentido, estado destino, estado origem
    while(True):

        nomeEstadoOrigem, nomeEstadoDestino, FimDasTransicoes = leEstadosOrigemEDestino(arquivo, estados)
        if(nomeEstadoOrigem is None)or(nomeEstadoDestino is None)or(FimDasTransicoes is None):
            return None, None
        elif(FimDasTransicoes is True):
            break

        transicao[4] = nomeEstadoOrigem
        transicao[3] = nomeEstadoDestino

        while(True):
            c = arquivo.read(1)
            if(c == '\n'):
                break
            elif(c in alfabeto)or(c in alfabetoFita)or(c == '<')or(c == '>')or(c == '_'):
                transicao[0] = c
            else:
                print("UMA DAS TRANSICOES NAO EH VALIDA POIS CONTEM CARACTERE FORA DO ALFABETO")
                return
                    
            c = arquivo.read(1)
            if(c != "/"):
                print("AS TRANSICOES DEVEM TER O FORMATO (lido)/(escrito)(direcao)")
                return
                    
            c = arquivo.read(1)
            if(c in alfabeto)or(c in alfabetoFita)or(c == '<')or(c == '>')or(c == '_'):
                transicao[1] = c
            else:
                print("UMA DAS TRANSICOES NAO EH VALIDA POIS CONTEM CARACTERE FORA DO ALFABETO")
                return
                    
            c = arquivo.read(1)
            if(c == 'D'):
                transicao[2] = c
            elif(c == 'E'):
                transicao[2] = c
            else:
                print(f"{c} NAO EH ACEITO COMO DIRECAO PARA A MAQUINA, SAO ACEITOS APENAS: E , D")
                return
                    
            transicoes.append(transicao.copy())

            c = arquivo.read(1)
            if(c == '\n'):
                break
            elif(c == ' '):
                continue
            else:
                print("O ARQUIVO DE ENTRADA ESTA ERRADO")
            
    estadosInstanciados = []
    for i in estados:
        transicoesEstadoI = []
        for j in transicoes:
            if j[4] == i:
                transicaoEstadoI = [j[0],j[1],j[2],j[3]]
                transicoesEstadoI.append(transicaoEstadoI.copy())

        if(i in finais):
            novo_estado = estado(i, transicoesEstadoI, True)
        else:
            novo_estado = estado(i, transicoesEstadoI)
        estadosInstanciados.append(novo_estado)
    
    if(EhALL):
        mt = turing(alfabeto,estadosInstanciados,inicial,alfabetoFita,finais,True)
    else:   
        mt = turing(alfabeto,estadosInstanciados,inicial,alfabetoFita,finais)

    entradas = leEntrada(arquivo,alfabeto)
    if (entradas is None):
        return None, None
    for i in entradas:
        if len(i) > 10**9:
            print(f"ENTRADA {i} EH MUITO LONGA, O MAXIMO DE CARACTERES PERMITIDOS PARA UMA ENTRADA EH 10^9")
            return None, None
            
    return mt, entradas

def leAPD(arquivo):
    estados = leEstados(arquivo)
    if(estados is None):
        return None, None
            
    alfabeto = leAlfabeto(arquivo,True,False)
    if(alfabeto is None):
        return None, None
            
    alfabetoPilha = leAlfabeto(arquivo,True,False)
    if(alfabetoPilha is None):
        return None, None
            
    inicial = leEstadoInicial(arquivo, estados)
    if(inicial is None):
        return None, None
            
    finais = leEstadosFinais(arquivo, estados)
    if(finais is None):
        return None, None
            

    #pega transicoes
    transicoes = []
    transicao = ['a','b','c','d','e'] #origem, destino, simbolo, desempilha, empilha
            
    while(True):
                

        nomeEstadoOrigem, nomeEstadoDestino, FimDasTransicoes = leEstadosOrigemEDestino(arquivo, estados)
        if(nomeEstadoOrigem is None)or(nomeEstadoDestino is None)or(FimDasTransicoes is None):
            return None, None
        elif(FimDasTransicoes is True):
            break
        transicao[0] = nomeEstadoOrigem
        transicao[1] = nomeEstadoDestino

        while(True):
            c = arquivo.read(1)
            
            if(c in alfabeto):
                transicao[2] = c
            else:
                print(f"UMA DAS TRANSICOES NAO EH VALIDA POIS {c} NAO PERTENCE AO ALFABETO")
                print(f"alfabeto: {alfabeto}")
                print(f"transicao: {transicao}")
                return None, None
                    
            c = arquivo.read(1)
            if(c != ","):
                print("AS TRANSICOES DEVEM TER O FORMATO (simbolo),(desempilha)/(empilha)")
                return None, None
                    
            c = arquivo.read(1)
            if(c in alfabetoPilha)or(c == '\\'):
                transicao[3] = c
            else:
                print(f"{c} NAO ESTA NO ALFABETO DE PILHA")
                return None, None
                    
            c = arquivo.read(1)
            if(c != "/"):
                print("AS TRANSICOES DEVEM TER O FORMATO (simbolo),(desempilha)/(empilha)")
                return None, None

            empilha = []
            c = arquivo.read(1)
            while(c != ' ')and(c != '\n'):
                if(c in alfabetoPilha)or(c == '\\'):
                    empilha.append(c)
                else:
                    print(f"{c} NAO ESTA NO ALFABETO DE PILHA")
                    return None, None
                c = arquivo.read(1)
            transicao[4] = empilha
            print(f"transicao adicionada: {transicao}")
            transicoes.append(transicao.copy())
            if(c == '\n'):
                break
            
                    
    print(f"transicoes: {transicoes}")
    apd = APD()
    apd.inicializaAPD(estados,alfabetoPilha,alfabeto,inicial,finais,transicoes)
    
                    
    entradas = leEntrada(arquivo,alfabeto)
    if (entradas is None):
        return None, None
            
    return apd, entradas

def leAFD(arquivo):
    estados = leEstados(arquivo)
    if(estados is None):
        return None, None

    alfabeto = leAlfabeto(arquivo,False,False)
    if(alfabeto is None):
        return None, None
            
    inicial = leEstadoInicial(arquivo, estados)
    if(inicial is None):
        return None, None
            
    finais = leEstadosFinais(arquivo, estados)
    if(finais is None):
        return None, None
            
    afd = AFD(set(estados),inicial,finais)
    afd.criaEstados()

    #pega transicoes
    while(True):
        nomeEstadoOrigem, nomeEstadoDestino, FimDasTransicoes = leEstadosOrigemEDestino(arquivo, estados)
        if(nomeEstadoOrigem is None)or(nomeEstadoDestino is None)or(FimDasTransicoes is None):
            return None, None
        elif(FimDasTransicoes is True):
            break

        while(True):
            c = arquivo.read(1)
            if(c == '\n'):
                break
            elif(c in alfabeto):
                simbolo = c
            else:
                print(f"{c} ESTA FORA DO ALFABETO")
                return
            afd.adicionaTransicao(nomeEstadoOrigem, simbolo ,nomeEstadoDestino)
            c = arquivo.read(1)
            if(c == '\n'):
                break
            elif(c == ' '):
                continue
            else:
                print("OS SIMBOLOS DE ENTRADA DE UMA TRANSICAO DEVEM SER SEPARADOS POR ESPACO")
                        
                
    entradas = leEntrada(arquivo,alfabeto)
    if (entradas is None):
        return None, None
            
    return afd, entradas

def leAFN(arquivo):
    
    estados = leEstados(arquivo)
    if(estados is None):
        return None, None
    
    alfabeto = leAlfabeto(arquivo, True, False)
    if(alfabeto is None):
        return None, None
    
    iniciais = leEstadosIniciais(arquivo, estados)
    if(iniciais is None):
        return None, None
    
    finais = leEstadosFinais(arquivo, finais)
    if(finais is None):
        return None, None
    
    transicoes= []
    transicao = ['a', 'b', 'c'] #origem, destino, simbolo lido
    while(True):
        nomeEstadoOrigem, nomeEstadoDestino, FimDasTransicoes = leEstadosOrigemEDestino(arquivo, estados)
        if(nomeEstadoOrigem is None)or(nomeEstadoDestino is None)or(FimDasTransicoes is None):
            return None, None
        elif(FimDasTransicoes is True):
            break
        transicao[0] = nomeEstadoOrigem
        transicao[1] = nomeEstadoDestino
        
        while(True):
            c = arquivo.read(1)
            if(c == '\n'):
                break
            elif(c in alfabeto):
                transicao[2] = c
                transicoes.append(transicao.copy())
            else:
                print(f"{c} ESTA FORA DO ALFABETO")
                return
            
            c = arquivo.read(1)
            if(c == '\n'):
                break
            elif(c == ' '):
                continue
            else:
                print("OS SIMBOLOS DE ENTRADA DE UMA TRANSICAO DEVEM SER SEPARADOS POR ESPACO")
    
    afn = inicializaAFN(estados,alfabeto,iniciais,finais,transicoes)
    
    entradas = leEntrada(arquivo,alfabeto)
    if (entradas is None):
        return None, None
    
    return afn, entradas

def leAPN(arquivo, ReconhecePorPilhaVazia):
    
    estados = leEstados(arquivo)
    if(estados is None):
        return None, None
            
    alfabeto = leAlfabeto(arquivo,True,False)
    if(alfabeto is None):
        return None, None
            
    alfabetoPilha = leAlfabeto(arquivo,True,False)
    if(alfabetoPilha is None):
        return None, None
            
    iniciais = leEstadosIniciais(arquivo,estados)
    if(iniciais is None):
        return None, None
            
    finais = leEstadosFinais(arquivo, estados)
    if(finais is None):
        return None, None
            

    #pega transicoes
    transicoes = []
    transicao = ['a','b','c','d','e'] #origem, destino, simbolo, desempilha, empilha
            
    while(True):
                

        nomeEstadoOrigem, nomeEstadoDestino, FimDasTransicoes = leEstadosOrigemEDestino(arquivo, estados)
        if(nomeEstadoOrigem is None)or(nomeEstadoDestino is None)or(FimDasTransicoes is None):
            return None, None
        elif(FimDasTransicoes is True):
            break
        transicao[0] = nomeEstadoOrigem
        transicao[1] = nomeEstadoDestino

        while(True):
            c = arquivo.read(1)
            if(c == '\n'):
                break
            elif(c in alfabeto):
                transicao[2] = c
            else:
                print(f"UMA DAS TRANSICOES NAO EH VALIDA POIS {c} NAO PERTENCE AO ALFABETO")
                return None, None
                    
            c = arquivo.read(1)
            if(c != ","):
                print("AS TRANSICOES DEVEM TER O FORMATO (simbolo),(desempilha)/(empilha)")
                return None, None
                    
            c = arquivo.read(1)
            if(c in alfabetoPilha)or(c == '\\'):
                transicao[3] = c
            else:
                print(f"{c} NAO ESTA NO ALFABETO DE PILHA")
                return None, None
                    
            c = arquivo.read(1)
            if(c != "/"):
                print("AS TRANSICOES DEVEM TER O FORMATO (simbolo),(desempilha)/(empilha)")
                return None, None

            empilha= []
            c = arquivo.read(1)
            while(c != ' ')and(c != '\n'):
                if(c in alfabetoPilha)or(c == '\\'):
                    empilha.append(c)
                else:
                    print(f"{c} NAO ESTA NO ALFABETO DE PILHA")
                    return None, None
                c = arquivo.read(1)
            transicao[4] = empilha
            transicoes.append(transicao.copy())
            if(c == '\n'):
                break
                    
    if(ReconhecePorPilhaVazia):
        apn = inicializaAPN(estados,alfabetoPilha,alfabeto,iniciais,finais,transicoes,False)
    else:      
        apn = inicializaAPN(estados,alfabetoPilha,alfabeto,iniciais,finais,transicoes)
                    
    entradas = leEntrada(arquivo,alfabeto)
    if (entradas is None):
        return None, None
            
    return apn, entradas
 
def leArquivo(caminho: str, maquina= "nada") -> str:
    
    arquivo = open(caminho, "r")
    # identifica a maquina
    if(maquina == "nada"):
        maquina = arquivo.readline()
    
    match maquina:
        case "@AFD":

            afd, entradas = leAFD(arquivo)
            if(afd is None)or(entradas is None):
                return None
            return afd, entradas, "@AFD"

        case "@APD":
            
            apd, entradas = leAPD(arquivo)
            if(apd is None)or(entradas is None):
                return None
            return apd, entradas, "@APD"

        case "@MT":
            
            mt, entradas = leMaquinaDeTuring(arquivo,False)
            if(mt is None)or(entradas is None):
                return None
            
            return mt, entradas, "@MT"

        case "@ALL":
            
            mt, entradas = leMaquinaDeTuring(arquivo,True)
            if(mt is None)or(entradas is None):
                return None

            return mt, entradas, "@ALL"

        case "@AFN":
            afn, entradas = leAFN(arquivo)
            if(afn is None)or(entradas is None):
                return None
            return afn, entradas, "@AFN"
                
        case "@APNP":
            apnp, entradas = leAPN(arquivo,False)
            if(apnp is None)or(entradas is None):
                return None
            return apnp, entradas, "@APNP"
        
        case "@APNPV":
            apnpv, entradas = leAPN(arquivo,True)
            if(apnpv is None)or(entradas is None):
                return None, None, None
            return apnpv, entradas, "@APNPV"

    
    return
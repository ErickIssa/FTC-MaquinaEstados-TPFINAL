from .AFD import AFD
from .apd import APD
from .turing import turing
from .estado import *

def estadosTemNomesIguais(estados)->bool:
    return len(estados) != len(set(estados))

def leArquivo(caminho: str, maquina= "nada") -> str:
    arquivo = open(caminho, "r")
    # identifica a maquina
    if(maquina == "nada"):
        maquina = arquivo.readline()
    
    match maquina:
        case "@AFD":

            #pega os estados

            linhaEstados = arquivo.readline().rstrip('\n')
            estados = linhaEstados.split()[1:]
            for i in estados:
                if len(i) >7:
                    print("O TAMANHO MAXIMO DO NOME DOS ESTADOS EH 7")
                    return 
            if(estadosTemNomesIguais(estados)):
                print("OS NOMES DOS ESTADOS DEVEM SER DIFERENTES")
                return 


            #pega o alfabeto
            arquivo.read(3)
            alfabeto: list
            while(True):
                c = arquivo.read(1)
                if(c == '\n'):
                    break
                alfabeto.append(c)
            
            #pega o estado inicial

            linhaInicial = arquivo.readline().rstrip('\n')
            inicial = linhaInicial.split()[1]
            
            #pega os estados finais

            linhaFinais = arquivo.readline().rstrip('\n')
            finais = linhaFinais.split()[1:]
            
            afd = AFD(set(estados),inicial,finais)
            afd.criaEstados()

            #pega transicoes
            while(True):
                nomeEstadoOrigem = ""
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
                    arquivo.read(3)
                    break

                arquivo.read(3)

                nomeEstadoDestino = ""
                while(True):
                    c = arquivo.read(1)
                    if(c == ' '):
                        break
                    nomeEstadoDestino += c
                
                arquivo.read(2)

                while(True):
                    c = arquivo.read(1)
                    if(c == '\n'):
                        break
                    elif(c in alfabeto):
                        simbolo = c
                    else:
                        print("UMA DAS TRANSICOES NAO EH VALIDA POIS CONTEM CARACTERE FORA DO ALFABETO")
                        return
                    afd.adicionaTransicao(nomeEstadoOrigem, simbolo ,nomeEstadoDestino)
                    c = arquivo.read(1)
                    if(c == '\n'):
                        break
                    elif(c == ' '):
                        continue
                    else:
                        print("OS SIMBOLOS DE ENTRADA DE UMA TRANSICAO DEVEM SER SEPARADOS POR ESPACO")
                        
                
                
            
            entradas: list
            while(True):
                entrada = arquivo.readline()
                if(entrada == ""):
                    break
                valido = True
                for i in entrada:
                    if i not in alfabeto:
                        valido = False
                
                if valido:
                    entradas.append(entrada)
            
            return afd, entradas

        case "@APD":

            apd = APD()
            #pega os estados

            linhaEstados = arquivo.readline().rstrip('\n')
            estados = linhaEstados.split()[1:]
            for i in estados:
                if len(i) >7:
                    print(f" {i} POSSUI {len(i)} CARACTERES, PORTANTO EXCEDE O MAXIMO DE 7")
                    return 
            if(estadosTemNomesIguais(estados)):
                print("OS NOMES DOS ESTADOS DEVEM SER DIFERENTES")
                return 
            
            #coloca os estados no automato
            for i in estados:
                apd.criaEstadoAPD(i)

            #pega o alfabeto
            arquivo.read(3)
            alfabeto: list
            while(True):
                c = arquivo.read(1)
                if(c == '\n'):
                    break
                if(c == '\\'):
                   print(" \\ NAO EH UM CARACTERE VALIDO")
                   return
                alfabeto.append(c)
            
            #pega o alfabeto da pilha
            arquivo.read(3)
            alfabetoPilha: list
            while(True):
                c = arquivo.read(1)
                if(c == '\n'):
                    break
                if(c == '\\'):
                   print(" \\ NAO EH UM CARACTERE VALIDO")
                   return
                alfabetoPilha.append(c)
            
            #pega o estado inicial
            
            linhaInicial = arquivo.readline().rstrip('\n')
            inicial = linhaInicial.split()[1]
            
            if(inicial in estados):
                apd.defineEstadoInicial(inicial)
            else:
                print(f"ESTADO INICIAL {inicial} NAO ESTA NA LISTA DE ESTADOS")
                return
            
            #pega os estados finais
            
            linhaFinais = arquivo.readline().rstrip('\n')
            finais = linhaFinais.split()[1:]

            falhou = False
            for i in finais:
                if(i not in estados):
                    print(f"ESTADO FINAL {i} NAO ESTA NA LISTA DE ESTADOS")
                    falhou = True
            
            if(falhou):
                return

            apd.defineEstadosFinais(finais)

            #pega transicoes
            while(True):
                nomeEstadoOrigem = ""
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
                    arquivo.read(3)
                    break

                arquivo.read(3)

                nomeEstadoDestino = ""
                while(True):
                    c = arquivo.read(1)
                    if(c == ' '):
                        break
                    nomeEstadoDestino += c
                
                arquivo.read(2)

                while(True):
                    c = arquivo.read(1)
                    if(c == '\n'):
                        break
                    elif(c in alfabeto):
                        simbolo = c
                    else:
                        print("UMA DAS TRANSICOES NAO EH VALIDA POIS CONTEM CARACTERE FORA DO ALFABETO")
                        return
                    
                    c = arquivo.read(1)
                    if(c != ","):
                        print("AS TRANSICOES DEVEM TER O FORMATO (simbolo),(desempilha)/(empilha)")
                        return
                    
                    c = arquivo.read(1)
                    if(c in alfabetoPilha):
                        desempilha = c
                    else:
                        print(f"{c} NAO ESTA NO ALFABETO DE PILHA")
                        return
                    
                    c = arquivo.read(1)
                    if(c != "/"):
                        print("AS TRANSICOES DEVEM TER O FORMATO (simbolo),(desempilha)/(empilha)")
                        return

                    empilha:list
                    c = arquivo.read(1)
                    while(c != '\n'):
                        if(c in alfabetoPilha):
                            empilha.append(c)
                        else:
                            print(f"{c} NAO ESTA NO ALFABETO DE PILHA")
                            return
                        c = arquivo.read(1)
                    
                    apd.criaTransicaoAPD(nomeEstadoOrigem,nomeEstadoDestino,simbolo,desempilha,empilha)

            # pega as entradas
            entradas: list
            while(True):
                entrada = arquivo.readline()
                if(entrada == ""):
                    break
                valido = True
                for i in entrada:
                    if i not in alfabeto:
                        valido = False
                
                if valido:
                    entradas.append(entrada)
            
            return apd, entradas

        case "@MT":
            
            #pega os estados

            linhaEstados = arquivo.readline().rstrip('\n')
            estados = linhaEstados.split()[1:]
            for i in estados:
                if len(i) >7:
                    print(f" {i} POSSUI {len(i)} CARACTERES, PORTANTO EXCEDE O MAXIMO DE 7")
                    return 
            if(estadosTemNomesIguais(estados)):
                print("OS NOMES DOS ESTADOS DEVEM SER DIFERENTES")
                return 
            

            #pega o alfabeto
            arquivo.read(3)
            alfabeto: list
            while(True):
                c = arquivo.read(1)
                if(c == '\n'):
                    break
                if(c == '\\' or c == '_' or c == '<' or c == '>'):
                   print(f"{c} NAO EH UM CARACTERE VALIDO")
                   return

                
                alfabeto.append(c)
            
            #pega o alfabeto da fita
            arquivo.read(3)
            alfabetoFita: list
            while(True):
                c = arquivo.read(1)
                if(c == '\n'):
                    break
                if(c == '\\' or c == '_' or c == '<' or c == '>'):
                   print(f"{c} NAO EH UM CARACTERE VALIDO")
                   return
                if(c in alfabeto):
                    print(f"{c} JA ESTA NO ALFABETO DE ENTRADA, O ALFABETO DE FITA DEVE SER EXCLUSIVO PARA A FITA")
                    return
                alfabetoFita.append(c)
            
            #pega o estado inicial
            
            linhaInicial = arquivo.readline().rstrip('\n')
            inicial = linhaInicial.split()[1]
            
            if(inicial not in estados):
                print(f"ESTADO INICIAL {inicial} NAO ESTA NA LISTA DE ESTADOS")
                return
            
            
            #pega os estados finais
            
            linhaFinais = arquivo.readline().rstrip('\n')
            finais = linhaFinais.split()[1:]

            falhou = False
            for i in finais:
                if(i not in estados):
                    print(f"ESTADO FINAL {i} NAO ESTA NA LISTA DE ESTADOS")
                    falhou = True
            
            if(falhou):
                return


            
            #pega transicoes
            transicoes:list 
            transicao = ['a','b','d','e','f'] # lido, escrito, sentido, estado destino, estado origem
            counter = 0
            while(True):
                nomeEstadoOrigem = ""
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
                    arquivo.read(3)
                    break
                transicao[3] = nomeEstadoOrigem
                arquivo.read(3)

                nomeEstadoDestino = ""
                while(True):
                    c = arquivo.read(1)
                    if(c == ' '):
                        break
                    nomeEstadoDestino += c
                transicao[3] = nomeEstadoDestino
                arquivo.read(2)

                while(True):
                    c = arquivo.read(1)
                    if(c == '\n'):
                        break
                    elif(c in alfabeto)or(c in alfabetoFita):
                        transicao[0] = c
                    else:
                        print("UMA DAS TRANSICOES NAO EH VALIDA POIS CONTEM CARACTERE FORA DO ALFABETO")
                        return
                    
                    c = arquivo.read(1)
                    if(c != "/"):
                        print("AS TRANSICOES DEVEM TER O FORMATO (lido)/(escrito)(direcao)")
                        return
                    
                    c = arquivo.read(1)
                    if(c in alfabeto)or(c in alfabetoFita):
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
                    
                    transicoes[counter] = transicao
                    counter += 1

                    c = arquivo.read(1)
                    if(c == '\n'):
                        break
                    elif(c == ' '):
                        continue
                    else:
                        print("O ARQUIVO DE ENTRADA ESTA ERRADO")
            
            estadosInstanciados:list
            for i in estados:
                transicoesEstadoI:list
                counter = 0
                for j in transicoes:
                    if j[4] == i:
                        transicaoEstadoI = [j[0],j[1],j[2],j[3]]
                        transicoesEstadoI[counter] = transicaoEstadoI
                        counter += 1

                if(i in finais):
                    estado = estado(i, transicoesEstadoI, True)
                else:
                    estado = estado(i, transicoesEstadoI)
                estadosInstanciados.append(estado)
            
            mt = turing(alfabeto,estadosInstanciados,inicial,alfabetoFita,finais)

            # pega as entradas
            entradas: list
            while(True):
                entrada = arquivo.readline()
                if(entrada == ""):
                    break
                elif(len(entradas) > 10**9):
                    print("O MAXIMO DE CARACTERES PERMITIDOS PARA UMA ENTRADA EH 10^9")
                    return
                valido = True
                for i in entrada:
                    if i not in alfabeto:
                        valido = False
                
                if valido:
                    entradas.append(entrada)
            
            return mt, entradas    

        case "@ALL":
            
            #pega os estados

            linhaEstados = arquivo.readline().rstrip('\n')
            estados = linhaEstados.split()[1:]
            for i in estados:
                if len(i) >7:
                    print(f" {i} POSSUI {len(i)} CARACTERES, PORTANTO EXCEDE O MAXIMO DE 7")
                    return 
            if(estadosTemNomesIguais(estados)):
                print("OS NOMES DOS ESTADOS DEVEM SER DIFERENTES")
                return 
            

            #pega o alfabeto
            arquivo.read(3)
            alfabeto: list
            while(True):
                c = arquivo.read(1)
                if(c == '\n'):
                    break
                if(c == '\\' or c == '_' or c == '<' or c == '>'):
                   print(f"{c} NAO EH UM CARACTERE VALIDO")
                   return

                
                alfabeto.append(c)
            
            #pega o alfabeto da fita
            arquivo.read(3)
            alfabetoFita: list
            while(True):
                c = arquivo.read(1)
                if(c == '\n'):
                    break
                if(c == '\\' or c == '_' or c == '<' or c == '>'):
                   print(f"{c} NAO EH UM CARACTERE VALIDO")
                   return
                if(c in alfabeto):
                    print(f"{c} JA ESTA NO ALFABETO DE ENTRADA, O ALFABETO DE FITA DEVE SER EXCLUSIVO PARA A FITA")
                    return
                alfabetoFita.append(c)
            
            #pega o estado inicial
            
            linhaInicial = arquivo.readline().rstrip('\n')
            inicial = linhaInicial.split()[1]
            
            if(inicial not in estados):
                print(f"ESTADO INICIAL {inicial} NAO ESTA NA LISTA DE ESTADOS")
                return
            
            
            #pega os estados finais
            
            linhaFinais = arquivo.readline().rstrip('\n')
            finais = linhaFinais.split()[1:]

            falhou = False
            for i in finais:
                if(i not in estados):
                    print(f"ESTADO FINAL {i} NAO ESTA NA LISTA DE ESTADOS")
                    falhou = True
            
            if(falhou):
                return


            
            #pega transicoes
            transicoes:list 
            transicao = ['a','b','d','e','f'] # lido, escrito, sentido, estado destino, estado origem
            counter = 0
            while(True):
                nomeEstadoOrigem = ""
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
                    arquivo.read(3)
                    break
                transicao[3] = nomeEstadoOrigem
                arquivo.read(3)

                nomeEstadoDestino = ""
                while(True):
                    c = arquivo.read(1)
                    if(c == ' '):
                        break
                    nomeEstadoDestino += c
                transicao[3] = nomeEstadoDestino
                arquivo.read(2)

                while(True):
                    c = arquivo.read(1)
                    if(c == '\n'):
                        break
                    elif(c in alfabeto)or(c in alfabetoFita):
                        transicao[0] = c
                    else:
                        print("UMA DAS TRANSICOES NAO EH VALIDA POIS CONTEM CARACTERE FORA DO ALFABETO")
                        return
                    
                    c = arquivo.read(1)
                    if(c != "/"):
                        print("AS TRANSICOES DEVEM TER O FORMATO (lido)/(escrito)(direcao)")
                        return
                    
                    c = arquivo.read(1)
                    if(c in alfabeto)or(c in alfabetoFita):
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
                    
                    transicoes[counter] = transicao
                    counter += 1

                    c = arquivo.read(1)
                    if(c == '\n'):
                        break
                    elif(c == ' '):
                        continue
                    else:
                        print("O ARQUIVO DE ENTRADA ESTA ERRADO")
            
            estadosInstanciados:list
            for i in estados:
                transicoesEstadoI:list
                counter = 0
                for j in transicoes:
                    if j[4] == i:
                        transicaoEstadoI = [j[0],j[1],j[2],j[3]]
                        transicoesEstadoI[counter] = transicaoEstadoI
                        counter += 1

                if(i in finais):
                    estado = estado(i, transicoesEstadoI, True)
                else:
                    estado = estado(i, transicoesEstadoI)
                estadosInstanciados.append(estado)
            
            all = turing(alfabeto,estadosInstanciados,inicial,alfabetoFita,finais, True)

            # pega as entradas
            entradas: list
            while(True):
                entrada = arquivo.readline()
                if(entrada == ""):
                    break
                elif(len(entradas) > 10**9):
                    print("O MAXIMO DE CARACTERES PERMITIDOS PARA UMA ENTRADA EH 10^9")
                    return
                valido = True
                for i in entrada:
                    if i not in alfabeto:
                        valido = False
                
                if valido:
                    entradas.append(entrada)
            
            return all, entradas



    return
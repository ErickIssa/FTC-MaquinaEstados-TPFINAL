"""convencoes para dar certo:

sempre passar ou dict ou set, depende do que for pedido
sempre passar o nome do estado, e nao o objeto do estado, para facilitar a busca no dicionario de estados
se tiver transição com 0 ou com 1, chamar adicionaTransicao 2x uma pa cada simbolo

*talvz dps criar um estado de erro pra toda afd.

"""



class EstadoAFD:
    def __init__(self,nome: str):
        self.nome = nome
        self.transicoes: dict[str, str] = {} # dicionario de transições no formato (simbolo : estadoDestino)
        #esse dicionario depois pode guardar uma tupla que tem mais informações


class AFD:
    def __init__(self,estadoNomes: set[str], estadoInicial: str, estadosFinais: set[str]):
        self.estadoNomes = estadoNomes #so recebe set, para nao repetir estados
        self.estadoInicial = estadoInicial #so recebe string, para nao repetir estados
        self.estadosFinais = estadosFinais #so recebe set, para nao repetir estados
        self.estados = {} #dicionario de estados, onde a chave é o nome do estado e o valor é um objeto do tipo Estado

        self.criaEstados() 

    def criaEstados(self): #adiciona os estados que estão em estadoNomes ao dicionário de estados 
        for nome in self.estadoNomes:
            self.estados[nome] = EstadoAFD(nome) #objeto estados[chave de busca no dict] = typecast para Estado(nomeDoEstado)
        return
    
    def adicionaTransicao(self, estadoOrigem: str, simbolo: str, estadoDestino: str):
        if estadoOrigem not in self.estadoNomes:
            print(f"Estado de origem '{estadoOrigem}' não existe.")
            return
        if estadoDestino not in self.estadoNomes:
           print(f"Estado de destino '{estadoDestino}' não existe.")
           return
        else:
            self.estados[estadoOrigem].transicoes[simbolo] = estadoDestino #adiciona a transição ao dicionário de transições do estado de origem
    
    def imprimeMaquina(self):
        print("===== AFD =====")
        print(f"Estados: {self.estadoNomes}")
        print(f"Estado inicial: {self.estadoInicial}")
        print(f"Estados finais: {self.estadosFinais}")

        print("\nTransições:")
        for nomeEstado, estado in self.estados.items():
            print(f"\nEstado {nomeEstado}:")

            if not estado.transicoes:
                print("  Sem transições")
                continue

            for simbolo, destino in estado.transicoes.items():
                print(f"  δ({nomeEstado}, {simbolo}) = {destino}")

        print("================")
        return
    
    def processaEntrada(self, entrada: str) -> bool:
        estadoAtual = self.estadoInicial

        if self.estadoInicial == "" or estadoAtual not in self.estadoNomes or estadoAtual not in self.estados:
            print(f"X") 
            return False #estado inicial invalido
        

        for simbolo in entrada:
            if simbolo not in self.estados[estadoAtual].transicoes:
                print(f"X") 
                return False #simbolo nao tem transicao, palavra rejeitada, vai pro estado de "erro"
            else:
                estadoAtual = self.estados[estadoAtual].transicoes[simbolo]
        #palavra totalmente processada, verificacao estado final
        if(estadoAtual in self.estadosFinais):
            print(f"OK")
            return True
        else:
            print(f"X")
            return False